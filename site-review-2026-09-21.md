# plugreports.com — Complete Site Review
**Date:** 2026-09-21 · **Commits:** `026464a` (fixes) + `63a809d` (resume) · **Status:** all fixes pushed to GitHub; deployment pending Cloudflare token

---

## 1. Your reported issues — root causes found & fixed

### A. "Pages not well designed on desktop / double overlapping sections"
**Root cause:** Two dead-JS bugs, not a design problem.
1. `hydrate.js` had 3 orphaned lines after its IIFE (left behind by a Sep-19 refactor) containing a top-level `return` → **SyntaxError: the entire hydration layer never executed in production since Sep 19**. No KV overlay, no image patching, no view counter — site was running on static-only fallback.
2. `app.js` age-gate code crashed with a TypeError (`data-gate-no` element missing), which killed settings injection, search, and the translate widget for every first-time visitor.
3. The "double vision" you saw was the age-gate's full-page `backdrop-filter: blur(6px)` smearing all page text behind the modal + a desktop-only image float reflow.

**Fixed:** orphaned lines deleted (hydration fully restored), gate null-guarded + init chain made crash-proof, gate blur reduced to 2px, service worker bumped to `pr-v9` with network-first HTML (returning visitors were permanently stuck with the broken cached JS — this forces the fix out).

### B. "We add images but they don't show on the website"
**Root cause:** Three stacked causes — your uploads were fine all along (all 50 uploaded images verified live and serving correctly, e.g. `/media/drugs/numbrino.webp` = 200 OK):
1. The dead hydration layer (above) was the *only* thing applying uploaded images to static pages.
2. `build.py` emitted broken `src="/https://plugreports.com/media/..."` (slash-prefixed absolute URL) on **32 drug pages** with images in source data.
3. Two disconnected storage conventions (repo folder vs KV).

**Fixed:** hydration restored, build.py URL bug fixed (0 broken image tags remain), image selector hardened (`img.pimg`), media cache changed to 1-hour revalidation so re-uploads actually propagate (previously `immutable` for a year), upload path is now per-type (`busts/`, `news/`… not everything forced into `drugs/`).

### C. "/admin lacks control — can't add/edit Pharmacies, Rehabs; platform not completely editable"
**Root causes found:**
1. **The 6 pharmacies, 6 rehabs, 9 hotline regions, 9 sentencing regions were never seeded to KV** — the admin tabs read from KV, so they showed empty lists while the content existed only baked into static HTML. → `seed.py` now seeds all 10 collections (KV-wins merge, so reseeds can never clobber your admin edits again — previously they did).
2. **Admin-added pharmacies/rehabs/quit guides rendered as BLANK pages** — `render.js` had no renderers for those types. → Added `centerPage()` and `quitPage()` renderers matching the static design.
3. **New directory entries never appeared on /pharmacies/ or /rehabs/ indexes; new hotline/sentencing regions were invisible.** → Hydration now rebuilds directory grids and appends new regions.
4. **Drug body edits (effects, risks, prices, legal status…) saved but never displayed** — hydration only patched the image, H1, and SEO fields. → Full-field hydration now.
5. **"Delete" never took pages offline and could never be undone.** → Unpublished items now show a 410 notice (hydrated) or real 404 (dynamic), admin shows an "unpublished" badge + green **Restore** button.
6. Suggestions inbox was read-only → per-item delete added. Misleading hardcoded placeholders ("Cenforce, Fildena…" on a cocaine page) → generalized. The "undefined" field label you saw was already fixed in a prior commit — hard-refresh the admin if it persists (cached page).

---

## 2. SEO & GEO audit — what was wrong, what's fixed

| Area | Was | Now |
|---|---|---|
| hreflang | **Completely broken** — 10 fake `?lang=xx` alternates per page (5 languages don't exist), conflicting/duplicate entries, no valid return links; Google almost certainly discarded the whole cluster | Real bidirectional path-based clusters only for pages that actually exist, `x-default` → EN; 0 fake alternates; full-site crawl verified 0 dead targets |
| Sitemap | `/admin/` included (contradicting robots/noindex); missing `/drugs/` + `/categories/`; fake uniform lastmod hardcoded "2026-09-14" | 631 clean URLs, truthful per-item lastmod |
| Images (SEO) | 32 pages with broken hero image URLs | 0 broken; width/height added (CLS fix on ~494 pages) |
| JSON-LD | All 448 BreadcrumbLists pointed their last item to the homepage; Articles missing required `image` + `publisher.logo`; no Organization/ItemList/MedicalBusiness | All fixed; schema on previously bare page types (busts, quit, pharmacies, rehabs, directories) |
| Titles/descriptions | 581/635 titles >60 chars (template alone was 105); descriptions averaged 300 chars (max 808); 11 pages with `&amp;#x27;` double-escape bug | Templates shortened + everything clipped ≤155; 0 escaping bugs |
| Thin content | 3 stub bust pages indexable | `noindex,follow` + excluded from sitemap (still reachable) |
| RSS | Invalid pubDate format, missing channel metadata | RFC-822, description/language/atom:link |
| llms.txt (GEO) | Only 40/430 drugs, fentanyl listed twice | Full library + NEW **llms-full.txt** (377 KB — entire library as one markdown file for AI ingestion) |
| Headers/404 | None | `_headers` (nosniff, Referrer-Policy, cache tuning) + branded 404.html |
| Stale content | Service worker served the cached home page forever | Network-first HTML |

**Still open (deliberate):** de/hi/no/pl/fr drug pages keep English titles/descriptions (needs real translation work, not machine-generated); ~490 titles still >60 chars because drug names themselves are long (your call); SearchAction schema omitted (site search is client-side only); no named human reviewers (E-E-A-T opportunity — see §4).

---

## 3. Content gaps (full report: `content-gaps.md`)

**P0 missing substances:** bromazolam (most-detected novel benzo in the US — absent despite your own fake-Xanax coverage), medetomidine (CDC MMWR Jun 2025; ~37% of opioid samples), 7-OH / MGM-15 (FDA scheduling recommendation Jul 2025 — massive search volume right now), PCP (you profile its analogues but not the parent), crack cocaine.

**P1:** tirzepatide, retatrutide (grey-market boom), phenazolam, N-pyrrolidino etonitazene, para-fluorofentanyl, BTMPS adulterant, O-DSMT, bupropion, an SSRI/SNRI class profile.

**Most-needed guides:** fentanyl test-strip how-to, naloxone access & use, mixing-dangers hub (benzos+opioids, alcohol+GHB, cocaethylene), serotonin syndrome/MAOI page, quit timelines for alcohol & nicotine (you have 8 timelines but not the two most-used drugs), pregnancy & drugs, chemsex, festival safety, counterfeit GLP-1 pens.

**Directory gaps:** no Gulf/Middle East hotlines despite covering the world's harshest sentencing there; LatAm = Brazil only; Asia = India/Thailand only. Report includes a verification rubric (licensing checks, MAT availability, red flags, re-verification cadence) so the "verified" badge means something defensible.

**Top SEO opportunity:** zero detection-window pages ("how long does X stay in your system" is among the highest-volume query families in this niche) and only one comparison page ("Adderall vs Vyvanse", "kratom vs 7-OH", "GHB vs GBL"). Top-20 query list in the report.

---

## 4. Recommended upgrades (not yet done — your decision)

1. **Named medical reviewer** on the About page + `reviewedBy` schema — the single biggest E-E-A-T lever for a YMYL site.
2. **R2 bucket** for media (one click in Cloudflare dashboard; code auto-upgrades when bound) — KV media storage has a 25 MB/key-pair cost profile that will bite as the gallery grows.
3. **Detection-window + comparison page generator** — template once, generate ~40 pages from existing data.
4. **IndexNow** for instant Bing indexing on publish.
5. Set `TOKEN_SECRET` in Pages → Settings → Variables (currently the default dev secret signs admin tokens).
6. **Rotate the GitHub token** (`ghp_7CPoTARs…`) — it's been exposed in chat history.
7. Set up Cloudflare Email Routing for contact@plugreports.com (still pending from last week).

---

## 5. To ship everything live, run these two commands

```bash
# 1. Deploy the site
CLOUDFLARE_API_TOKEN=<your-token> CLOUDFLARE_ACCOUNT_ID=ae600dad34caf146bfd16ce840a2808f \
  npx wrangler pages deploy public --project-name=plugreports --branch=main

# 2. Seed KV (adds the 4 missing collections — pharmacies/rehabs/hotlines/sentencing —
#    to /admin WITHOUT touching any of your existing admin edits)
CF_TOKEN=<your-token> python3 src/seed.py
```

Or paste a token (Pages:Edit + KV:Edit) in chat and I'll run both for you.

**After deploying:** hard-refresh once (Ctrl/Cmd+Shift+R) so the new service worker (`pr-v9`) replaces the broken cached JS — then verify any drug page shows its uploaded image and /admin → Pharmacies lists 6 editable entries.
