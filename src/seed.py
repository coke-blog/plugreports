#!/usr/bin/env python3
"""Merge-safe KV seeder — NEVER wipes admin edits.
Merge semantics: if an item (by slug) already exists in KV, the KV item WINS on
every key it holds — reseeding only fills in fields the KV item lacks (e.g. new
structural fields added to the data later). Admin edits (images, rewrites, any
field present in KV) are never reverted by a reseed. Admin-created items (slugs
not in the seed) are kept untouched. The admin API's 409-on-duplicate-slug POST
behavior is unaffected. Usage: python3 src/seed.py [type ...]"""
import json, os, re, sys, urllib.request

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

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")

def merge(seed_items, kv_items):
    kv_by_slug = {x.get("slug"): x for x in (kv_items or []) if x.get("slug")}
    seen = set()
    out = []
    for item in seed_items:
        slug = item.get("slug")
        seen.add(slug)
        if slug in kv_by_slug:
            merged = dict(item)              # seed provides structure + any NEW fields
            merged.update(kv_by_slug[slug])  # KV (admin edits) wins on every key it holds
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
    from data_content import (BUSTS, NEWS, TOPICS, QUIT_SPECS,
                              HOTLINES, PHARMACIES, REHABS, SENTENCING)
    from data_related import RELATED_OVERRIDES
    try:
        from data_mix import MIX
    except Exception:
        MIX = []
    for d in DRUGS: d.update(RELATED_OVERRIDES.get("drugs", {}).get(d["slug"], {}))
    for b in BUSTS: b.update(RELATED_OVERRIDES.get("busts", {}).get(b["slug"], {}))
    for n in NEWS: n.update(RELATED_OVERRIDES.get("news", {}).get(n["slug"], {}))
    for t in TOPICS: t.update(RELATED_OVERRIDES.get("topics", {}).get(t["slug"], {}))
    seeds = {
        "drugs": DRUGS,
        "categories": [dict(slug=k, name=v["name"], color=v["color"], grad=v["grad"], tagline=v["tagline"], blurb=v["blurb"]) for k, v in CATEGORIES.items()],
        "busts": BUSTS, "news": NEWS, "topics": TOPICS,
        "quit": [dict(slug=k, **v) for k, v in QUIT_SPECS.items()],
        # admin SCHEMAS shapes: hotlines -> {region, slug, items[[number,name,desc,tel], ...]}
        "hotlines": [dict(slug=slugify(region), region=region,
                          items=[list(it) for it in items]) for region, items in HOTLINES.items()],
        # pharmacies/rehabs already match the admin shape (slug,name,region,desc,phone,website,verified)
        "pharmacies": PHARMACIES,
        "rehabs": REHABS,
        # every sentencing item needs a slug (derive from region when missing)
        "sentencing": [dict(s, slug=s.get("slug") or slugify(s["region"])) for s in SENTENCING],
        # mix items already match the admin shape (slug,a,b,aSlug,bSlug,level,title,...)
        "mix": MIX,
    }
    types = sys.argv[1:] or list(seeds.keys())
    for t in types:
        kv = kv_get("content:" + t)
        merged = merge(seeds[t], kv if isinstance(kv, list) else [])
        ok = kv_put("content:" + t, merged)
        print(f"{t}: {len(merged)} items merged-seeded (success={ok})")
