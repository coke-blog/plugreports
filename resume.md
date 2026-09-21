# plugreports.com — Project Resume
> Snapshot: 2026-09-21 (post-audit, commit 026464a) · Read this first in any new session before touching anything.

## One-paragraph summary
plugreports.com is a multilingual harm-reduction library (430 drug profiles, 26 guides, 9 hotline regions, 9 sentencing regions, verified directories) built as a Python-generated static site on Cloudflare Pages + Pages Functions + KV. Content is fully editable through a PIN-protected `/admin` CMS backed by KV (all 10 collections seeded + editable), with live hydration overlaying admin edits onto static pages. Runs on Cloudflare's free tier; repo at github.com/coke-blog/plugreports (public, main branch).

## Stack & architecture
- **Static generator:** `src/build.py` (Python 3, no deps) — reads `src/data_*.py`, emits all HTML to `public/` with JSON-LD (MedicalWebPage/FAQPage/NewsArticle/Article/ItemList/MedicalBusiness/Organization/BreadcrumbList), REAL bidirectional hreflang clusters (path-based only — never `?lang=` alternates; `?lang=` is client-side UI strings only), sitemap.xml (truthful per-item lastmod, no /admin/), RFC-822 rss.xml, full llms.txt + llms-full.txt, _static.json manifest, _headers, 404.html, robots.txt.
- **Backend:** Cloudflare Pages Functions (`functions/`) — admin API (PIN auth via HMAC token), public content API, view counter, media upload (KV storage, R2-ready), translate endpoint (Workers AI m2m100), suggestions GET+DELETE.
- **Storage:** KV namespace `plugreports-content` (binding `CONTENT`, id `4bf215d251e940ed9f97ea2811f6ebce`). Merge-seed only — **KV (admin) values win on conflict**; seed only fills missing fields/items. Never bulk-overwrite.
- **Live layer:** `hydrate.js` overlays KV content on static pages (full-field drug hydration, dir-grid on /pharmacies/ + /rehabs/, hotline/sentencing region append, category hero, 410 notice for unpublished); `render.js` builds pages client-side for KV-only items (drugs, busts, news, topics, categories, **pharmacies, rehabs, quit**); dynamic routes consult `_static.json` (60s module-scope cache, fail-open to static) then KV (all routes enforce `!unpublished`).
- **Media:** uploads to KV (`media:` prefix, per-type path `<type>/<slug>.<ext>`), served via `/media/*` with `max-age=3600, must-revalidate` (re-uploads propagate within the hour).
- **Caching:** sw.js `pr-v9` — network-first for HTML/API/media, cache-first only `/assets/*`. HTML pins JS with `?v=9` — **bump both together on every JS change** or returning visitors keep stale assets forever.
- **i18n:** full sections `/es` (24 profiles + hubs) and `/de /hi /no /pl /fr` (8 profiles + home/hotlines/categories each). de/hi/no/pl/fr drug pages currently keep EN titles/descriptions (no per-locale meta strings in data_i18n.py — content task).

## Operating procedures (critical)
1. **Build:** `python3 src/build.py` (must print "Built ... into ..." — a syntax error in data files silently kills the build while old output persists).
2. **Deploy:** `CLOUDFLARE_API_TOKEN=… CLOUDFLARE_ACCOUNT_ID=ae600dad34caf146bfd16ce840a2808f npx wrangler pages deploy public --project-name=plugreports --branch=main`
3. **Seed KV safely:** `CF_TOKEN=… python3 src/seed.py` (KV-wins merge; covers ALL 10 collections: drugs, categories, busts, news, topics, quit, hotlines, pharmacies, rehabs, sentencing). NEVER raw-PUT content keys.
4. **Git sync:** environment periodically wipes `.git` and reverts random files (happened twice on 2026-09-21). Recovery: clone from GitHub, `rsync -a --exclude=.git` workspace → clone, commit, push. Keep `/tmp/*.bak` backups of src files during long edit sessions; md5-check before rebuild.
5. **Duplicate slug `4-fa` watch** — run the dup check after every build.
6. **After any JS change:** bump `?v=` pins in build.py templates AND sw.js cache name together, rebuild, deploy.

## Admin (plugreports.com/admin)
- PIN login (user-set: `chichon1` as of 2026-09-21). Idle logout 40s with 25s warning; never logs out mid-edit; draft autosave every 8s with auto-restore.
- All 10 collections: add / edit / unpublish / **restore** (unpublished badge + green restore button). Delete = unpublish; hydrated pages show a 410 notice, KV-only pages 404.
- Suggestions inbox: view + delete per item.
- Uploads: per-type media path; gallery picker searches name/alias/slug.
- Settings: SEO sockets GSC/Bing/Clarity/GA, breaking banner, socials Reddit/Quora/email. NOTE: `crisisNote` setting still saves to KV but is only baked at build time (no runtime wiring — known dead end, low priority).
- REL field formats: `drugslug`, `type:slug`, `https://url`, `https://url|Label`. REL const must stay an OBJECT, not a string.

## Security state
- Cloudflare tokens rotated & scrubbed from git history (Sept 16). Tokens used in session were re-created for ops; treat as sensitive.
- GitHub token `ghp_7CPoTARs…` is in chat history AND in the local git remote URL — user should rotate it.
- `TOKEN_SECRET` env var: never set (default dev secret in use) — set in Pages → Settings → Variables if hardening.
- Repo is public. No secrets may be committed.

## Content stats
430 drug profiles · 18 categories · 26 topics · 8 quit timelines · 7 busts (3 thin tiktok stubs are noindex) · 5 news · hotlines 9 regions · pharmacies 6 · rehabs 6 · sentencing 9 regions. ES + 5 languages. 631 sitemap URLs.

## SEO/GEO state (fixed 2026-09-21)
- hreflang: real path-based bidirectional clusters + x-default → EN. No fake alternates.
- Sitemap: truthful lastmod, includes /drugs/ + /categories/, excludes /admin/ + noindex stubs.
- Titles/descriptions clipped (≤~60/≤155); no double-escaped entities.
- JSON-LD on all page types; Article/NewsArticle have image + publisher.logo.
- llms.txt full coverage; llms-full.txt (377 KB) = whole library in one markdown file for AI ingestion.
- _headers (nosniff, Referrer-Policy, cache tuning), branded 404.
- Remaining: per-locale translated meta strings, ~490 titles still >60 chars (long drug/topic names — content call), SearchAction omitted (search is client-side), reviewer attribution is Organization-level (no named humans).

## Roadmap (agreed, not done)
- Content gaps report: `content-gaps.md` (P0 missing: bromazolam, medetomidine, 7-OH/MGM-15, PCP, crack; guides: fentanyl test strips, naloxone, mixing-danger hub; quit timelines for alcohol/nicotine; detection-window pages — top SEO opportunity).
- 70 more profiles → 500 milestone → press release + Product Hunt launch (copy drafted).
- Video pipeline `tools/make_video.py` — 2 done; YouTube/TikTok not launched.
- Quora/Reddit cadence; backlink queue; Sterling sentencing follow-up Nov 25.
- Contact mailbox `contact@plugreports.com` — Cloudflare Email Routing not yet set up by user.
- Optional: IndexNow, Arabic/Portuguese i18n, R2 bucket, per-locale meta translations.

## Key file map
- `src/build.py` — generator (edit with care; f-string heavy; keep /tmp backup while editing)
- `src/data_drugs.py` — all profiles (+ `data_batch100.py`, `data_greymarket.py`)
- `src/data_content.py` — news/busts/topics/quit/hotlines/pharmacies/rehabs/sentencing/settings
- `src/data_categories.py` · `src/data_es.py` · `src/data_i18n.py` · `src/data_related.py` · `src/data_sources.py` · `src/seed.py`
- `public/admin/index.html` — CMS (single-file app)
- `public/assets/js/` — app.js, hydrate.js, render.js, breaking.js, markdown.js
- `functions/` — API routes (admin CRUD = unpublish-not-delete; restore via PUT unpublished:false)
- `tools/make_video.py` — explainer video generator
