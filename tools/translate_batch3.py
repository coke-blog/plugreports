#!/usr/bin/env python3
"""Translation batch 3 — 25% of remaining untranslated drug profiles per language.
Pattern proven in batches 1-2: dedupe cache, browser UA, batches of 12, 3 workers,
STRICT count assertion per batch with per-text singles fallback (the endpoint can
silently misalign/drop texts). Writes src/data_i18n_expansion3.py.
Usage: python3 tools/translate_batch3.py [--limit N]   (N = profiles per lang)"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
CACHE_PATH = os.path.join(ROOT, "tools", "mt3_cache.json")
OUT_PATH = os.path.join(ROOT, "src", "data_i18n_expansion3.py")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TARGETS = {"es": "spanish", "de": "german", "hi": "hindi", "no": "norwegian",
           "pl": "polish", "fr": "french", "pt": "portuguese", "ar": "arabic"}
FIELDS = ["schedule", "appearance", "streetPrice", "legalStatus"]
LISTS = ["effects", "risks", "overdoseSigns"]

def api_translate(texts, target, retries=4):
    body = json.dumps({"texts": texts, "target": target}).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request("https://plugreports.com/api/translate",
                data=body, headers={"Content-Type": "application/json", "User-Agent": UA})
            j = json.load(urllib.request.urlopen(req, timeout=60))
            r = j.get("results")
            if j.get("ok") and isinstance(r, list):
                return r
        except Exception as e:
            if attempt == retries - 1: raise
            time.sleep(2 + attempt * 2)
    raise RuntimeError("translate failed")

def translate_all(texts, target, cache):
    """Translate list of texts with dedupe cache; strict alignment."""
    out = [None] * len(texts)
    todo = []
    for i, t in enumerate(texts):
        if t in cache: out[i] = cache[t]
        else: todo.append((i, t))
    # dedupe todo preserving first occurrence
    seen, uniq = set(), []
    for i, t in todo:
        if t not in seen: seen.add(t); uniq.append((i, t))
    groups = {}  # text -> [indices]
    for i, t in todo: groups.setdefault(t, []).append(i)

    batches = [uniq[k:k+12] for k in range(0, len(uniq), 12)]
    lock_texts = []
    def work(batch):
        bt = [t for _, t in batch]
        try:
            tr = api_translate(bt, target)
            if len(tr) != len(bt): raise RuntimeError(f"count {len(tr)}!={len(bt)}")
        except Exception:
            tr = [api_translate([t], target)[0] for _, t in batch]  # singles fallback
        return list(zip([t for _, t in batch], tr))
    with ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(work, batches):
            lock_texts.extend(res)
    for src, dst in lock_texts:
        cache[src] = dst
    for i, t in enumerate(texts):
        out[i] = cache[t]
    return out

def main():
    limit = 34
    if "--limit" in sys.argv: limit = int(sys.argv[sys.argv.index("--limit") + 1])
    from data_drugs import DRUGS
    from data_i18n import LANGS
    from data_es import ES_DRUGS
    by_slug = {d["slug"]: d for d in DRUGS}
    order = [d["slug"] for d in DRUGS]

    have = {l: set(p["drugs"].keys()) for l, p in LANGS.items()}
    have["es"] = set(ES_DRUGS.keys())
    todo = {}
    for l in ["es"] + list(LANGS.keys()):
        rem = [s for s in order if s not in have[l]]
        n = limit + 1 if l in ("pt", "ar") else limit  # pt/ar have more remaining
        todo[l] = rem[:n]
        print(f"{l}: {len(have[l])} translated, {len(rem)} remaining, taking {len(todo[l])}")

    cache = json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}
    result = {}
    for l, slugs in todo.items():
        cache.setdefault(l, {})
        lc = cache[l]
        # flatten texts in deterministic order
        flat, layout = [], []
        for s in slugs:
            d = by_slug[s]
            keys = []
            for f in FIELDS:
                keys.append((f, None)); flat.append(d.get(f, "") or "")
            for f in LISTS:
                vals = d.get(f, []) or []
                keys.append((f, len(vals))); flat.extend(vals)
            layout.append((s, keys))
        print(f"[{l}] translating {len(flat)} texts ({len(lc)} cached)...", flush=True)
        tr = translate_all(flat, TARGETS[l], lc)
        # save cache incrementally per lang
        json.dump(cache, open(CACHE_PATH, "w"), ensure_ascii=False)
        pack = {}
        pos = 0
        for s, keys in layout:
            item = {}
            for f, n in keys:
                if n is None:
                    item[f] = tr[pos]; pos += 1
                else:
                    item[f] = tr[pos:pos+n]; pos += n
            pack[s] = item
        result[l] = pack
        print(f"[{l}] done -> {len(pack)} profiles", flush=True)

    es = result.pop("es", {})
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Machine-translated expansion pack 3 (Workers AI m2m100 via /api/translate) - 2026-10-08.\n")
        f.write("# ~25% of previously untranslated profiles per language. Merged at import time\n")
        f.write("# by data_i18n.py / data_es.py. KV/admin edits still win at runtime.\n")
        f.write("LANGS_MT3 = " + repr(result) + "\n\n")
        f.write("ES_DRUGS_MT3 = " + repr(es) + "\n")
    print("WROTE", OUT_PATH)

if __name__ == "__main__":
    main()
