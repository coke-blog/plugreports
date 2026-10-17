#!/usr/bin/env python3
"""Push fallback: remote tree listing comes from a pre-fetched curl file
(urllib kept dying with truncated gzip on the recursive tree GET).
Usage: GH_TOKEN=... python3 tools/finish_push2.py <message> [tree_json_path]
Reads tree json from /tmp/remote_tree.json by default."""
import base64, hashlib, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "coke-blog/plugreports"
TOKEN = os.environ["GH_TOKEN"]
HDR = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json",
       "User-Agent": "plugreports-push"}

def api(method, path, payload=None, retries=6):
    url = f"https://api.github.com/repos/{REPO}{path}"
    for i in range(retries):
        try:
            data = json.dumps(payload).encode() if payload is not None else None
            req = urllib.request.Request(url, data=data, headers=HDR, method=method)
            return json.load(urllib.request.urlopen(req, timeout=120))
        except Exception as e:
            print(f"  retry {i+1}/{retries} {method} {path}: {e}", flush=True)
            time.sleep(2 + i * 2)
    raise RuntimeError(f"failed {method} {path}")

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()

def main():
    msg = sys.argv[1]
    tree_file = sys.argv[2] if len(sys.argv) > 2 else "/tmp/remote_tree.json"
    head = api("GET", "/git/refs/heads/main")["object"]["sha"]
    commit = api("GET", f"/git/commits/{head}")
    print("remote head:", head[:10], flush=True)

    remote = {}
    tj = json.load(open(tree_file))
    for e in tj["tree"]:
        if e["type"] == "blob":
            remote[e["path"]] = e["sha"]
    print(f"remote files: {len(remote)} | truncated: {tj.get('truncated')}", flush=True)

    changed = []
    for dirpath, _, files in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir.split(os.sep)[0] in (".git", "node_modules", "__pycache__"): continue
        for fn in files:
            p = os.path.join(rel_dir, fn) if rel_dir != "." else fn
            data = open(os.path.join(dirpath, fn), "rb").read()
            if remote.get(p) != blob_sha(data):
                changed.append((p, data))
    print(f"changed/new files: {len(changed)}", flush=True)
    if not changed:
        print("nothing to push"); return

    entries = []
    for p, data in changed:
        b = api("POST", "/git/blobs", {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        entries.append({"path": p, "mode": "100644", "type": "blob", "sha": b["sha"]})
    print(f"blobs uploaded: {len(entries)}", flush=True)

    base = commit["tree"]["sha"]
    CH = 700
    for i in range(0, len(entries), CH):
        chunk = entries[i:i+CH]
        t = api("POST", "/git/trees", {"base_tree": base, "tree": chunk})
        base = t["sha"]
        print(f"  tree chunk {i//CH+1}: +{len(chunk)} -> {base[:10]}", flush=True)

    nc = api("POST", "/git/commits", {"message": msg, "tree": base, "parents": [head]})
    api("PATCH", "/git/refs/heads/main", {"sha": nc["sha"], "force": False})
    print("PUSHED", nc["sha"][:10], "-", msg, flush=True)

if __name__ == "__main__":
    main()
