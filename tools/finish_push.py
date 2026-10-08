#!/usr/bin/env python3
"""Finish the push after a full blob upload: rebuild tree entries from locally
computed git-blob SHA1s (blobs are content-addressed and already on GitHub),
create the tree in CHUNKS (a single 4,725-entry tree 502s), commit, move ref.
Usage: python3 tools/finish_push.py "message" [prefixes...]"""
import base64, hashlib, json, os, sys, time, urllib.request

TOKEN = os.environ["GH_TOKEN"]  # read from env — NEVER hardcode tokens (repo is public; GitHub push protection 422s blobs containing valid secrets)
REPO = "coke-blog/plugreports"
API = f"https://api.github.com/repos/{REPO}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gh(method, path, payload=None, retries=8):
    import gzip, http.client
    url = path if path.startswith("http") else API + path
    data = json.dumps(payload).encode() if payload is not None else None
    for a in range(retries):
        try:
            req = urllib.request.Request(url, data=data, method=method, headers={
                "Authorization": "token " + TOKEN, "Accept": "application/vnd.github+json",
                "Accept-Encoding": "gzip", "User-Agent": "plugreports-sync"})
            r = urllib.request.urlopen(req, timeout=120)
            try:
                body = r.read()
            except http.client.IncompleteRead as e:
                body = e.partial
            if r.headers.get("Content-Encoding") == "gzip":
                body = gzip.decompress(body)
            return json.loads(body)
        except Exception as e:
            print(f"  retry {a+1}/{retries} {method} {path}: {e}", flush=True)
            if a == retries - 1: raise
            time.sleep(3 + a * 3)

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()

def main():
    msg = sys.argv[1]
    prefixes = sys.argv[2:] or ["src/", "public/", "resume.md"]
    head = gh("GET", "/branches/main")
    commit_sha = head["commit"]["sha"]
    tree_sha = head["commit"]["commit"]["tree"]["sha"]
    print("remote head:", commit_sha[:10], flush=True)
    remote = {}
    t = gh("GET", f"/git/trees/{tree_sha}?recursive=1")
    for e in t.get("tree", []):
        if e["type"] == "blob": remote[e["path"]] = e["sha"]
    print("remote files:", len(remote), "| truncated:", t.get("truncated"), flush=True)

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
                    cand.append((os.path.relpath(fp, ROOT).replace(os.sep, "/"), fp))
        for rel, fp in cand:
            if "mt3_cache.json" in rel: continue
            data = open(fp, "rb").read()
            if remote.get(rel) != blob_sha(data):
                changed.append((rel, data))
    print("changed/new files:", len(changed), flush=True)
    if not changed:
        print("nothing to push"); return

    # Entries reference locally computed blob SHAs directly — the earlier run
    # already uploaded every blob (ex.map completed), and blob SHAs are
    # content-addressed, so no existence re-check is needed. Set VERIFY=1 to
    # re-check/upload missing blobs via the API (costs one request per file).
    entries = []
    if os.environ.get("VERIFY"):
        def ensure(rel_data):
            rel, data = rel_data
            sha = blob_sha(data)
            try:
                gh("GET", f"/git/blobs/{sha}", retries=2)
                return {"path": rel, "mode": "100644", "type": "blob", "sha": sha}, False
            except Exception:
                b = gh("POST", "/git/blobs", {"content": base64.b64encode(data).decode(), "encoding": "base64"})
                return {"path": rel, "mode": "100644", "type": "blob", "sha": b["sha"]}, True

        from concurrent.futures import ThreadPoolExecutor
        uploaded = 0
        with ThreadPoolExecutor(max_workers=8) as ex:
            for i, (e, was_up) in enumerate(ex.map(ensure, changed)):
                entries.append(e)
                uploaded += 1 if was_up else 0
                if (i + 1) % 500 == 0:
                    print(f"  verified {i+1}/{len(changed)} (re-uploaded {uploaded})", flush=True)
        print(f"blobs ready: {len(entries)} (re-uploaded {uploaded})", flush=True)
    else:
        entries = [{"path": rel, "mode": "100644", "type": "blob", "sha": blob_sha(data)}
                   for rel, data in changed]
        print(f"entries built from local SHAs: {len(entries)} (VERIFY=1 to re-check)", flush=True)

    # Chunked tree creation — a single giant tree POST 502s.
    CHUNK = 700
    base = tree_sha
    for i in range(0, len(entries), CHUNK):
        part = entries[i:i + CHUNK]
        nt = gh("POST", "/git/trees", {"base_tree": base, "tree": part})
        base = nt["sha"]
        print(f"  tree chunk {i//CHUNK + 1}: +{len(part)} -> {base[:10]}", flush=True)

    nc = gh("POST", "/git/commits", {"message": msg, "tree": base, "parents": [commit_sha]})
    gh("PATCH", "/git/refs/heads/main", {"sha": nc["sha"]})
    print("PUSHED", nc["sha"][:10], "-", msg, flush=True)

if __name__ == "__main__":
    main()
