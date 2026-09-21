# plugreports.com — Project Resume
> Snapshot: 2026-09-21 (round-2 review complete + hub h1 fix, CF deploy 9e5408c2) · Read this first in any new session before touching anything.

## One-paragraph summary
plugreports.com is a multilingual harm-reduction library (430 drug profiles, 26 guides, 61 mixing-dangers pages, 9 hotline regions, 9 sentencing regions, verified directories) built as a Python-generated static site on Cloudflare Pages + Pages Functions + KV. Content is fully editable through a PIN-protected `/admin` CMS backed by KV (all 11 collections seeded + editable), with live hydration overlaying admin edits onto static pages. Runs on Cloudflare's free tier; repo at github.com/coke-blog/plugreports (public, main branch).

## Stack & architecture
- **Static generator:** `src/build.py` (Python 3, no deps) — reads `src/data_*.py`, emits all HTML to `public/` with JSON-LD (MedicalWebPage/FAQPage/NewsArticle/Article/ItemList/MedicalBusiness/Organization/BreadcrumbList), REAL bidirectional hreflang clusters (path-based only — never `?lang=` alternates; `?lang=` is client-side UI strings only), sitemap.xml (truthful per-item lastmod, no /admin/), RFC-822 rss.xml, full llms.txt + llms-full.txt, _static.json manifest, _headers, 404.html, robots.txt. Also builds the **/mix/ section** (`build_mix()`: hub with 3 data-tier grids + 61 detail pages with level badges) and **formula placeholders** (`drug_placeholder_panel()` + `pimg_html()` — molecular formula panel shown until a photo is mapped; `src/data_formulas.py`, 303 slug→formula entries). Drug profile top = `.ptop` two-column grid (main + right rail: image above Quick facts — no floats).
- **Backend:** Cloudflare Pages Functions (`functions/`) — admin API (PIN auth via HMAC token), public content API, view counter, media upload (KV storage, R2-ready), translate endpoint (Workers AI m2m100), suggestions GET+DELETE.
- **Storage:** KV namespace `plugreports-content` (binding `CONTENT`, id `4bf215d251e940ed9f97ea2811f6ebce`). Merge-seed only — **KV (admin) values win on conflict**; seed only fills missing fields/items. Never bulk-overwrite.
- **Live layer:** `hydrate.js` overlays KV content on static pages (full-field drug hydration incl. `.pimg-formula`→`<img>` swap when KV gains an image, dir-grid on /pharmacies/ + /rehabs/, hotline/sentencing region append, category hero, 410 notice for unpublished, renderMix for mix pages); `render.js` builds pages client-side for KV-only items (drugs, busts, news, topics, categories, pharmacies, rehabs, quit, **mix** via mixPage; centers via centerPage); dynamic routes consult `_static.json` (60s module-scope cache, fail-open to static) then KV (all routes enforce `!unpublished`). `functions/mix/[slug].js` serves mix detail routes.
- **Media:** uploads to KV (`media:` prefix, per-type path `<type>/<slug>.<ext>`), served via `/media/*` with `max-age=3600, must-revalidate` (re-uploads propagate within the hour). 67 drugs have mapped photos; 17 orphaned KV media files were mapped to drug records live via admin API PUT on 2026-09-21 (cocaine, fentanyl, ketamine, molly, oxycontin…).
- **Caching:** sw.js `pr-v10` — network-first for HTML/API/media, cache-first only `/assets/*`. HTML pins JS with `?v=10` **and CSS with `style.css?v=10`** — bump all three together on every asset change. HARD LESSON (2026-09-21): `_headers` gives `/assets/*` `max-age=604800`, so an **unpinned** stylesheet stays stale at the edge for a week (broke the .ptop grid live until the pin shipped). CSS must be version-pinned exactly like JS.
- **i18n:** full sections `/es` (24 profiles + hubs) and `/de /hi /no /pl /fr` (8 profiles + home/hotlines/categories each). de/hi/no/pl/fr drug pages currently keep EN titles/descriptions (no per-locale meta strings in data_i18n.py — content task).

## Operating procedures (critical)
1. **Build:** `python3 src/build.py` (must print "Built ... into ..." — a syntax error in data files silently kills the build while old output persists).
2. **Deploy:** `CLOUDFLARE_API_TOKEN=… CLOUDFLARE_ACCOUNT_ID=ae600dad34caf146bfd16ce840a2808f npx wrangler pages deploy public --project-name=plugreports --branch=main`
3. **Seed KV safely:** `CF_TOKEN=… python3 src/seed.py` (KV-wins merge; covers ALL 11 collections: drugs, categories, busts, news, topics, quit, hotlines, pharmacies, rehabs, sentencing, mix). NEVER raw-PUT content keys.
4. **Git sync:** environment periodically wipes `.git` and reverts random files (3× on 2026-09-21). Recovery: clone from GitHub, `rsync -a --exclude=.git` workspace → clone, commit, push. **github.com:443 is blocked for the git protocol** — use api.github.com instead: download tarball (`/repos/.../tarball/<sha>`), diff, create blobs (base64 POST /git/blobs), create trees in chunks of ≤100 with `base_tree` chaining, commit, PATCH ref. Working script pattern: /tmp/api_push4.py (resumable via /tmp/push_state.json; DELETE state file if sources changed mid-push) (recreate from this recipe if wiped; blob SHA = `sha1("blob <len>\0"+raw)`). Keep `/tmp/*.bak` backups of src files during long edit sessions; md5-check before rebuild.
5. **Duplicate slug `4-fa` watch** — run the dup check after every build.
6. **After any JS or CSS change:** bump the `?v=` pins in build.py templates (JS AND `style.css?v=`) AND the sw.js cache name together, rebuild, deploy. CSS is edge-cached a week — never rely on a purge.

## Admin (plugreports.com/admin)
- PIN login (user-set: `chichon1` as of 2026-09-21). Idle logout 40s with 25s warning; never logs out mid-edit; draft autosave every 8s with auto-restore. **Drafts are keyed per item** (`pr-draft-<type>-<slug>`, legacy per-collection key auto-cleared) — fixed 2026-09-21 after a per-collection draft key made every drug edit form restore numbrino's draft.
- All 11 collections (incl. **mix**, ⚗️ icon): add / edit / unpublish / **restore** (unpublished badge + green restore button). Delete = unpublish; hydrated pages show a 410 notice, KV-only pages 404.
- Suggestions inbox: view + delete per item.
- Uploads: per-type media path; gallery picker searches name/alias/slug.
- Settings: SEO sockets GSC/Bing/Clarity/GA, breaking banner, socials Reddit/Quora/email. NOTE: `crisisNote` setting still saves to KV but is only baked at build time (no runtime wiring — known dead end, low priority).
- REL field formats: `drugslug`, `type:slug`, `https://url`, `https://url|Label`. REL const must stay an OBJECT, not a string.

## Security state
- Cloudflare tokens rotated & scrubbed from git history (Sept 16). Two NEW Cloudflare tokens (`cfut_ZtTTwloq…` KV Worker, `cfut_Z3fS2Mv1…`) were pasted in chat on 2026-09-21 for ops — user must rotate both.
- GitHub token `ghp_7CPoTARs…` is in chat history AND in the local git remote URL — user should rotate it.
- `TOKEN_SECRET` env var: never set (default dev secret in use) — set in Pages → Settings → Variables if hardening.
- Repo is public. No secrets may be committed.

## Content stats
430 drug profiles (67 with photos, 303 with formula placeholders) · 18 categories · 26 topics · 8 quit timelines · 7 busts (3 thin tiktok stubs are noindex) · 5 news · **61 mix pages** (26 deadly / 25 dangerous / 10 caution) · hotlines 9 regions · pharmacies 6 · rehabs 6 · sentencing 9 regions. ES + 5 languages. ~690 sitemap URLs.

## SEO/GEO state (fixed 2026-09-21)
- hreflang: real path-based bidirectional clusters + x-default → EN. No fake alternates.
- Sitemap: truthful lastmod, includes /drugs/ + /categories/, excludes /admin/ + noindex stubs.
- Titles/descriptions clipped (≤~60/≤155); no double-escaped entities.
- JSON-LD on all page types; Article/NewsArticle have image + publisher.logo; mix pages carry MedicalWebPage + FAQPage + BreadcrumbList.
- llms.txt full coverage incl. /mix/; llms-full.txt = whole library in one markdown file for AI ingestion (rebuilt with mix section).
- _headers (nosniff, Referrer-Policy, cache tuning), branded 404.
- Remaining: per-locale translated meta strings, ~490 titles still >60 chars (long drug/topic names — content call), SearchAction omitted (search is client-side), reviewer attribution is Organization-level (no named humans).

## Roadmap (agreed, not done)
- Content gaps report: `content-gaps.md` (P0 missing: bromazolam, medetomidine, 7-OH/MGM-15, PCP, crack; guides: fentanyl test strips, naloxone; quit timelines for alcohol/nicotine; detection-window pages — top SEO opportunity). ~~mixing-danger hub~~ → DONE 2026-09-21 (/mix/, 61 pages).
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
- `src/data_mix.py` — 61 combination pages ({slug, a, b, aSlug, bSlug, level, title, summary, mechanism, effects[], signs[], whatToDo[], sources, lastUpdated}) · `src/data_formulas.py` — 303 slug→Unicode-subscript molecular formulas
- `public/admin/index.html` — CMS (single-file app)
- `public/assets/js/` — app.js, hydrate.js, render.js, breaking.js, markdown.js
- `functions/` — API routes (admin CRUD = unpublish-not-delete; restore via PUT unpublished:false)
- `tools/make_video.py` — explainer video generator
