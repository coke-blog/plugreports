# plugreports.com — Project Resume
> Snapshot: 2026-09-21 · Read this first in any new session before touching anything.

## One-paragraph summary
plugreports.com is a multilingual harm-reduction library (430 drug profiles, 27 guides, 9 hotline regions, 8 sentencing regions, verified directories) built as a Python-generated static site on Cloudflare Pages + Pages Functions + KV. Content is fully editable through a PIN-protected `/admin` CMS backed by KV, with live hydration overlaying admin edits onto static pages. Runs on Cloudflare's free tier; repo at github.com/coke-blog/plugreports (public, main branch).

## Stack & architecture
- **Static generator:** `src/build.py` (Python 3, no deps) — reads `src/data_*.py`, emits all HTML to `public/` with JSON-LD (MedicalWebPage/FAQPage/NewsArticle), hreflang clusters, sitemap.xml, rss.xml, llms.txt, _static.json manifest.
- **Backend:** Cloudflare Pages Functions (`functions/`) — admin API (PIN auth via HMAC token), public content API, view counter, media upload (KV storage, R2-ready), translate endpoint (Workers AI m2m100).
- **Storage:** KV namespace `plugreports-content` (binding `CONTENT`, id `4bf215d251e940ed9f97ea2811f6ebce`). Merge-seed only — never bulk-overwrite (admin edits live only in KV).
- **Live layer:** `hydrate.js` overlays KV content on static pages at load; `render.js` builds pages client-side for KV-only items; dynamic routes (`functions/{drugs,busts,news,topics,quit,pharmacies,rehabs,categories}/[slug].js`) consult `_static.json` then KV.
- **Media:** uploads to KV (`media:` prefix), served via `/media/*` function; admin gallery searches by drug name/alias/slug.
- **i18n:** full sections `/es` (24 profiles + hubs) and `/de /hi /no /pl /fr` (8 profiles + home/hotlines/categories each), data in `src/data_es.py`, `src/data_i18n.py`; UI strings + browser-language detection in `app.js`.

## Operating procedures (critical)
1. **Build:** `python3 src/build.py` (must print "Built ... into ..." — check for errors; a syntax error in data files silently kills the build while old output persists).
2. **Deploy:** `CLOUDFLARE_API_TOKEN=… CLOUDFLARE_ACCOUNT_ID=ae600dad34caf146bfd16ce840a2808f npx wrangler pages deploy public --project-name=plugreports --branch=main`
3. **Seed KV safely:** `CF_TOKEN=… python3 src/seed.py` (merge-safe; preserves admin-only keys). NEVER raw-PUT content keys from data files — wipes admin edits.
4. **Git sync:** environment periodically wipes `.git` and reverts random files. Recovery: clone from GitHub, `rsync -a --exclude=.git` workspace → clone, commit, `push --force-with-lease`. Verify remote before editing files.
5. **Duplicate slug `4-fa` has resurrected multiple times** from reverted files — always run the dup check after build.

## Admin (plugreports.com/admin)
- PIN login (user-set: `chichon1` as of 2026-09-21). Idle logout 40s with 25s warning; never logs out mid-edit; draft autosave every 8s with auto-restore.
- Accordion icon menu; inline editors under clicked rows; list search/filter on all tabs.
- Schemas: drugs, categories, busts, news, topics (Markdown editor + toolbar), quit, hotlines, pharmacies, rehabs, sentencing, settings (SEO sockets GSC/Bing/Clarity/GA, breaking-banner toggle + slug override, socials Reddit/Quora/email).
- "You may also want to know about" field formats: `drugslug`, `type:slug`, `https://url`, `https://url|Label`; checkbox hides default cards. (Fixed 2026-09-21: REL const must stay an OBJECT, not a string.)
- Gallery picker searches by name/alias/slug. Images serve at `/media/drugs/<slug>.<ext>` — filenames must match references exactly.

## Security state
- Cloudflare tokens rotated & scrubbed from git history (Sept 16). Tokens used in session were re-created for ops; treat as sensitive.
- GitHub token `ghp_7CPoTARs…` is in chat history — user should rotate it.
- `TOKEN_SECRET` env var: never set (default dev secret in use) — set in Pages → Settings → Variables if hardening.
- Repo is public. No secrets may be committed (push protection will block anyway).

## Content stats
430 drug profiles · 18 categories · 27 guides/topics · 8 quit timelines · 6 busts (Alert-tagged feed the home breaking carousel, 5-slot, swipeable, country chips) · 5 news · hotlines 9 regions · pharmacies 7 · rehabs 6 · sentencing 8 regions (incl. Middle East, Asia, LatAm). ES + 5 languages. ~180 static pages + dynamic layer.

## Known data quirks
- `lastUpdated` field drives "new today" filters; set `views` to boost Trending sort.
- News/bust `tag: "Alert"` + `country` → breaking carousel. Settings `breakingEnabled`/`breakingSlug` control it.
- Busts tagged Alert merge with news into the carousel pool (both static + hydrate).
- Static fallback serves old content if KV missing — hydration masks it; static regen happens on next build.
- Bing URL lists generated per batch on request.

## Roadmap (agreed, not done)
- 70 more profiles → 500 milestone → press release (drafted) + Product Hunt launch (copy drafted).
- Video pipeline `tools/make_video.py` (gTTS + moviepy, 9:16) — 2 videos done (fentanyl, nitrous); YouTube/TikTok channels not yet launched; user declined celebrity-voice cloning (correctly).
- Quora Space posting cadence (copy banked); Reddit plan week 3 (r/harmreduction PSA drafted).
- Backlink queue: AddictionResource, RecoveryConnection, Blunt-Therapy guest posts (drafts ready); Featured/Qwoted expert profiles.
- Sterling sentencing Nov 25 → follow-up alert post.
- Contact mailbox `contact@plugreports.com` — Cloudflare Email Routing not yet set up by user.
- Optional: view-counter-driven Trending (wired), IndexNow, Arabic/Portuguese i18n, R2 bucket (uploads auto-upgrade when bound).

## Key file map
- `src/build.py` — generator (edit with care; f-string heavy)
- `src/data_drugs.py` — all profiles (+ `data_batch100.py`, `data_batch2-3 inline`)
- `src/data_content.py` — news/busts/topics/quit/hotlines/pharmacies/rehabs/sentencing/settings
- `src/data_categories.py` · `src/data_es.py` · `src/data_i18n.py` · `src/data_related.py` · `src/data_sources.py` · `src/seed.py`
- `public/admin/index.html` — CMS (single-file app)
- `public/assets/js/` — app.js (i18n/settings/socials), hydrate.js, render.js, breaking.js, markdown.js
- `functions/` — API routes (admin CRUD = unpublish-not-delete)
- `tools/make_video.py` — explainer video generator
