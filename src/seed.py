#!/usr/bin/env python3
"""Merge-safe KV seeder — NEVER wipes admin edits.
Rule: seed values win on keys the seed defines; KV-only keys (admin-added
images, markdown, fields we don't seed) are preserved. Admin-created items
(slugs not in seed) are kept. Usage: python3 src/seed.py [type ...]"""
import json, os, sys, urllib.request

ACCT = "ae600dad34caf146bfd16ce840a2808f"
NS   = "4bf215d251e940ed9f97ea2811f6ebce"
CF   = os.environ.get("CF_TOKEN", "")  # never commit tokens — pass via env
BASE = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/storage/kv/namespaces/{NS}/values/"

def kv_get(key):
    req = urllib.request.Request(BASE + key, headers={"Authorization": "Bearer " + CF})
    try: return json.load(urllib.request.urlopen(req))
    except Exception: return None

def kv_put(key, obj):
    req = urllib.request.Request(BASE + key, data=json.dumps(obj).encode(),
        headers={"Authorization": "Bearer " + CF, "Content-Type": "application/json"}, method="PUT")
    return json.load(urllib.request.urlopen(req)).get("success")

def merge(seed_items, kv_items):
    kv_by_slug = {x.get("slug"): x for x in (kv_items or []) if x.get("slug")}
    seen = set()
    out = []
    for item in seed_items:
        slug = item.get("slug")
        seen.add(slug)
        if slug in kv_by_slug:
            merged = dict(kv_by_slug[slug])   # KV first: keeps admin-only keys
            merged.update(item)               # seed wins on keys it defines
            out.append(merged)
        else:
            out.append(item)
    for slug, item in kv_by_slug.items():     # admin-created items survive
        if slug not in seen:
            out.append(item)
    return out

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_drugs import DRUGS
    from data_categories import CATEGORIES
    from data_content import BUSTS, NEWS, TOPICS, QUIT_SPECS
    from data_related import RELATED_OVERRIDES
    for d in DRUGS: d.update(RELATED_OVERRIDES.get("drugs", {}).get(d["slug"], {}))
    for b in BUSTS: b.update(RELATED_OVERRIDES.get("busts", {}).get(b["slug"], {}))
    for n in NEWS: n.update(RELATED_OVERRIDES.get("news", {}).get(n["slug"], {}))
    for t in TOPICS: t.update(RELATED_OVERRIDES.get("topics", {}).get(t["slug"], {}))
    seeds = {
        "drugs": DRUGS,
        "categories": [dict(slug=k, name=v["name"], color=v["color"], grad=v["grad"], tagline=v["tagline"], blurb=v["blurb"]) for k, v in CATEGORIES.items()],
        "busts": BUSTS, "news": NEWS, "topics": TOPICS,
        "quit": [dict(slug=k, **v) for k, v in QUIT_SPECS.items()],
    }
    types = sys.argv[1:] or list(seeds.keys())
    for t in types:
        kv = kv_get("content:" + t)
        merged = merge(seeds[t], kv if isinstance(kv, list) else [])
        ok = kv_put("content:" + t, merged)
        print(f"{t}: {len(merged)} items merged-seeded (success={ok})")
