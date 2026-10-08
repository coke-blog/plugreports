#!/usr/bin/env python3
"""Push local changes to GitHub via REST API (git protocol is blocked/flaky here).
Computes git blob SHAs locally, diffs against the remote recursive tree,
uploads only changed/new blobs, creates one commit, moves main.
Usage: python3 tools/push_github.py "commit message" [path_prefix ...]
  path_prefix: limit push to these repo-relative prefixes (default: src/, public/, resume.md)
Skips: __pycache__, tools/mt3_cache.json."""
import base64, hashlib, json, os, sys, time, urllib.request

TOKEN = os.environ["GH_TOKEN"]  # read from env — NEVER hardcode tokens (repo is public; GitHub push protection 422s blobs containing valid secrets)
REPO = "coke-blog/plugreports"
API = f"https://api.github.com/repos/{REPO}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gh(method, path, payload=None, raw=False, retries=6):
    import gzip, http.client
    url = path if path.startswith("http") else API + path
    data = json.dumps(payload).encode() if payload is not None else None
    for a in range(retries):
        try:
            req = urllib.request.Request(url, data=data, method=method, headers={
                "Authorization": "token " + TOKEN, "Accept": "application/vnd.github+json",
                "Accept-Encoding": "gzip", "User-Agent": "plugreports-sync"})
            r = urllib.request.urlopen(req, timeout=90)
            try:
                body = r.read()
            except http.client.IncompleteRead as e:
                body = e.partial  # use what we got; json parse will fail if truly truncated
            if r.headers.get("Content-Encoding") == "gzip":
                body = gzip.decompress(body)
            return body if raw else json.loads(body)
        except Exception:
            if a == retries - 1: raise
            time.sleep(2 + a * 2)

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()

def main():
    msg = sys.argv[1]
    prefixes = sys.argv[2:] or ["src/", "public/", "resume.md"]
    head = gh("GET", "/branches/main")
    commit_sha = head["commit"]["sha"]
    tree_sha = head["commit"]["commit"]["tree"]["sha"]
    print("remote head:", commit_sha[:10])
    remote = {}
    t = gh("GET", f"/git/trees/{tree_sha}?recursive=1")
    for e in t.get("tree", []):
        if e["type"] == "blob": remote[e["path"]] = e["sha"]
    print("remote files:", len(remote), "| truncated:", t.get("truncated"))

    changed = []
    for pref in prefixes:
        lp = os.path.join(ROOT, pref.rstrip("/"))
        if os.path.isfile(lp):
            cand = [(pref, lp)]
        else:
            cand = []
            for dp, dn, fn in os.walk(lp):
                dn[:] = [d for d in dn if d != "__pycache__"]
                for f in fn:
                    fp = os.path.join(dp, f)
                    rel = os.path.relpath(fp, ROOT).replace(os.sep, "/")
                    cand.append((rel, fp))
        for rel, fp in cand:
            if "mt3_cache.json" in rel: continue
            data = open(fp, "rb").read()
            if remote.get(rel) != blob_sha(data):
                changed.append((rel, data))
    print("changed/new files:", len(changed))
    if not changed:
        print("nothing to push"); return

    from concurrent.futures import ThreadPoolExecutor
    def up(rel_data):
        rel, data = rel_data
        b = gh("POST", "/git/blobs", {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        return {"path": rel, "mode": "100644", "type": "blob", "sha": b["sha"]}
    entries = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, e in enumerate(ex.map(up, changed)):
            entries.append(e)
            if (i + 1) % 100 == 0: print(f"  uploaded {i+1}/{len(changed)}", flush=True)
    nt = gh("POST", "/git/trees", {"base_tree": tree_sha, "tree": entries})
    nc = gh("POST", "/git/commits", {"message": msg, "tree": nt["sha"], "parents": [commit_sha]})
    gh("PATCH", "/git/refs/heads/main", {"sha": nc["sha"]})
    print("PUSHED", nc["sha"][:10], "-", msg)

if __name__ == "__main__":
    main()
