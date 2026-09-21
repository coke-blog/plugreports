# Plan — plugreports.com Complete Site Review & Fix (2026-09-21)

## Context from resume.md + user report + screen recording
User-reported issues:
1. /admin lacks add/edit control for Pharmacies, Rehabs (and possibly other collections)
2. Platform not completely editable
3. Uploaded images don't show on site ("IMAGE PENDING" placeholder on /drugs/numbrino/)
4. Desktop rendering broken: every section of drug page renders TWICE and overlaps (hydration duplication bug) — visible throughout 9:15 AM recording
5. SEO/GEO verification needed
6. Content gap analysis (missing drugs/topics) needed

## Stage 0 — Environment recon (Orchestrator)
- Check git state, Cloudflare/wrangler token availability, build health (`python3 src/build.py`), dup-slug check.

## Stage 1 — Parallel audit (explore subagents, read-only)
- A1: hydrate.js / render.js / dynamic [slug].js — find the double-render/overlap root cause on desktop drug pages; trace image pipeline end-to-end (admin upload → KV media: → /media/* → <img> reference in static + hydrated + dynamic renders). Report exact file/line fixes.
- A2: public/admin/index.html — map every schema tab's CRUD capabilities vs. what functions/api supports; identify missing Add/Edit for pharmacies, rehabs, sentencing, hotlines, categories, quit; check KV key conventions vs seed.py and dynamic routes.
- A3: SEO/GEO audit — sitemap.xml, robots.txt, llms.txt, rss.xml, manifest, hreflang clusters, JSON-LD on each page type, canonical tags, _static.json, meta tags. Report gaps.

## Stage 2 — Fixes (coder subagents, sequential per area to avoid conflicts)
- F1: Fix double-render bug (hydrate/render) — highest priority, breaks all pages.
- F2: Fix image display pipeline end-to-end.
- F3: Complete admin CRUD (add/edit pharmacies, rehabs, any other missing collections) + wire dynamic routes/hydration to match.
- F4: SEO/GEO fixes from A3.

## Stage 3 — Content gap analysis (explore/research subagent)
- Missing high-traffic drugs, uncovered harm-reduction topics, suggested updates.

## Stage 4 — Validate & ship
- Rebuild, run dup-slug check, verify pages locally, commit + push, deploy to Cloudflare Pages if token available (else give user exact deploy commands).
- Update resume.md.

## Stage 5 — Final report to user
- Audit findings, fixes shipped, content gap recommendations.
