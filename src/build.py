#!/usr/bin/env python3
"""plugreports.com static site generator.
Reads src/data_*.py and emits the full SEO-hardened site into public/."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_drugs import DRUGS
from data_categories import CATEGORIES
from data_content import (BUSTS, NEWS, HOTLINES, PHARMACIES, REHABS,
                          SENTENCING, SETTINGS, QUIT_SPECS, TOPICS)
from data_related import RELATED_OVERRIDES
from data_sources import AGENCY_LINKS, DEEP_LINKS, QUOTES

def _apply_overrides():
    for d in DRUGS: d.update(RELATED_OVERRIDES.get("drugs", {}).get(d["slug"], {}))
    for b in BUSTS: b.update(RELATED_OVERRIDES.get("busts", {}).get(b["slug"], {}))
    for n in NEWS: n.update(RELATED_OVERRIDES.get("news", {}).get(n["slug"], {}))
    for t in TOPICS: t.update(RELATED_OVERRIDES.get("topics", {}).get(t["slug"], {}))
    for k, v in QUIT_SPECS.items(): v.update(RELATED_OVERRIDES.get("quit", {}).get(k, {}))
_apply_overrides()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB  = os.path.join(ROOT, "public")
SITE = "https://plugreports.com"
TODAY = "2026-09-14"

def esc(s): return html.escape(str(s), quote=True)
def w(path, content):
    fp = os.path.join(PUB, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f: f.write(content)
    return path

def slugify(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# ---------------------------------------------------------------- blocks ----
def render_blocks(blocks, resolve):
    out = []
    for b in blocks:
        t = b[0]
        if t == "p": out.append(f"<p>{b[1]}</p>")
        elif t == "h2": out.append(f"<h2>{esc(b[1])}</h2>")
        elif t == "h3": out.append(f"<h3>{esc(b[1])}</h3>")
        elif t == "ul": out.append("<ul>" + "".join(f"<li>{x}</li>" for x in b[1]) + "</ul>")
        elif t == "ol": out.append("<ol>" + "".join(f"<li>{x}</li>" for x in b[1]) + "</ol>")
        elif t == "quote": out.append(f"<blockquote>&ldquo;{b[1]}&rdquo;<br><small>&mdash; {esc(b[2])}</small></blockquote>")
        elif t == "callout":
            color, title, text = b[1]
            out.append(f'<div class="callout {color}"><b>{esc(title)}</b>{text}</div>')
        elif t == "stats":
            out.append('<div class="stat-grid">' + "".join(
                f'<div class="stat{" red" if i==0 else ""}"><b>{esc(n)}</b><span>{esc(l)}</span></div>'
                for i, (n, l) in enumerate(b[1])) + "</div>")
        elif t == "table":
            rows = b[1]; head, body = rows[0], rows[1:]
            h = "".join(f"<th>{esc(c)}</th>" for c in head)
            r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in body)
            out.append(f'<div class="figure"><table class="tbl"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>')
        elif t == "figure": out.append(f'<figure class="figure">{b[1]}<figcaption>{esc(b[2])}</figcaption></figure>')
        elif t == "timeline":
            items = "".join(f'<div class="tl-item {cls}"><h4>{esc(ti)}</h4><p>{esc(tx)}</p></div>' for cls, ti, tx in b[1])
            out.append(f'<div class="timeline">{items}</div>')
        elif t == "checklist":
            out.append('<ul class="checklist">' + "".join(f"<li>{x}</li>" for x in b[1]) + "</ul>")
        elif t == "related":
            cards = "".join(f'<a href="/{resolve(s)}/">{rel_card(s)}</a>' for s in b[1])
            out.append(f'<div class="related print-hide"><h2>You may also want to know about</h2><div class="rel-grid">{cards}</div></div>')
        elif t == "links":
            cards = "".join(f'<a href="/{u}/">{rel_card(u.split("/")[-1])}</a>' for u in b[1])
            out.append(f'<div class="related print-hide"><h2>Full day-by-day guides</h2><div class="rel-grid">{cards}</div></div>')
    return "\n".join(out)

DRUG_BY_SLUG = {d["slug"]: d for d in DRUGS}
TOPIC_BY_SLUG = {t["slug"]: t for t in TOPICS}
NEWS_BY_SLUG = {n["slug"]: n for n in NEWS}

def help_links(drugs=None, extra=None, related=None):
    known = {x["slug"] for x in DRUGS}
    chips = "".join(f'<a href="/drugs/{d}/">{rel_card(d)}</a>' for d in (drugs or []) if d in known)
    for r in (related or []):
        chips += f'<a href="/{resolve_slug(r)}/">{rel_card(r)}</a>'
    chips += '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines — help now</span></a>'
    chips += '<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Find a verified pharmacy</span></a>'
    chips += '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>'
    for label, href, col in (extra or []):
        chips += f'<a href="{href}"><span class="mini" style="background:{col}">&#128218;</span><span>{esc(label)}</span></a>'
    return f'<div class="related print-hide"><h2>Drugs mentioned &amp; help</h2><div class="rel-grid">{chips}</div></div>'

def resolve_slug(s):
    if ":" in s:
        t, sl = s.split(":", 1)
        if t in ("drugs","busts","news","topics","quit","categories","hotlines","pharmacies","rehabs","sentencing"):
            return f"{t}/{sl}"
        return s
    if s in DRUG_BY_SLUG: return f"drugs/{s}"
    if s in TOPIC_BY_SLUG: return f"topics/{s}"
    if s in NEWS_BY_SLUG: return f"news/{s}"
    if s in QUIT_SPECS: return f"quit/{s}"
    return s  # section pages: busts, hotlines, sentencing...

def rel_card(slug):
    if ":" in slug:
        sl = slug.split(":", 1)[1]
        return f'<span class="mini" style="background:#667085">&#8250;</span><span>{esc(sl.replace("-", " ").title())}</span>'
    d = DRUG_BY_SLUG.get(slug)
    if d:
        c = CATEGORIES[d["category"]]
        return (f'<span class="mini" style="background:{c["color"]}">{esc(d["name"][0])}</span>'
                f'<span>{esc(d["name"])}</span>')
    t = TOPIC_BY_SLUG.get(slug)
    if t: return f'<span class="mini" style="background:#b45309">&#128218;</span><span>{esc(t["title"])}</span>'
    n = NEWS_BY_SLUG.get(slug)
    if n: return f'<span class="mini" style="background:#dc2626">N</span><span>{esc(n["title"])}</span>'
    if slug in QUIT_SPECS: return f'<span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting {esc(QUIT_SPECS[slug]["name"])} — day by day</span>'
    return f'<span class="mini" style="background:#667085">&#8250;</span><span>{esc(slug.replace("-", " ").title())}</span>'

# ------------------------------------------------------------ page shell ----
NAV = [
 ("/", "Home", "home"), ("/categories/opioids/", "Drug Library", "drugs"),
 ("/news/", "News", "news"), ("/busts/", "Busts", "busts"), ("/topics/", "Guides", "topics"),
 ("/quit/", "Quitting", "quit"), ("/hotlines/", "Hotlines", "hotline"),
 ("/sentencing/", "Sentencing", "sentencing"), ("/pharmacies/", "Pharmacies", "pharmacies"),
 ("/rehabs/", "Rehabs", "rehabs"), ("/about/", "About", "about"),
]

def shell(path, title, desc, body, jsonld=None, canonical=None, extra_head="", ogimage=None, lang="en", es_url=None, en_url=None):
    canon = canonical or (SITE + ("/" if path == "index.html" else "/" + path.replace("index.html", "")))
    alt = ""
    if es_url: alt += f'<link rel="alternate" hreflang="es" href="{es_url}">'
    if lang == "es" and en_url: alt += f'<link rel="alternate" hreflang="en" href="{en_url}">'
    crumbs = ""
    parts = [p for p in path.split("/") if p and p != "index.html"]
    if parts:
        acc, links = [], []
        for p in parts[:-1]:
            acc.append(p)
            if os.path.isfile(os.path.join(PUB, *acc, "index.html")):
                links.append(f'<a href="/{"/".join(acc)}/">{esc(p.replace("-"," ").title())}</a>')
            else:
                links.append(f'<span>{esc(p.replace("-"," ").title())}</span>')
        crumbs = ('<div class="wrap"><nav class="crumbs print-hide"><a href="/">Home</a> / '
                  + " / ".join(links) + f' / <span>{esc(title.split("—")[0].strip())}</span></nav></div>')
    langlinks = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{canon}?lang={l}">' for l in
        ["en","es","zh","hi","ar","pt","ru","ja","de","fr"])
    navlinks = "".join(
        f'<a href="{u}" class="{"hot" if k=="hotline" else ""}">{t}</a>' for u, t, k in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    if SETTINGS.get("gsc"): ld += f'<meta name="google-site-verification" content="{esc(SETTINGS["gsc"])}">'
    if SETTINGS.get("bing"): ld += f'<meta name="msvalidate.01" content="{esc(SETTINGS["bing"])}">'
    if SETTINGS.get("clarity"): ld += '<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,"clarity","script","' + esc(SETTINGS["clarity"]) + '")</script>'
    if SETTINGS.get("ga"): ld += '<script async src="https://www.googletagmanager.com/gtag/js?id=' + esc(SETTINGS["ga"]) + '"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","' + esc(SETTINGS["ga"]) + '")</script>' 
    if path.split("/")[0] in ("busts","news","drugs","topics","quit","hotlines","pharmacies","rehabs","sentencing","index.html"):
        ld += '<script src="/assets/js/hydrate.js?v=6" defer></script>' 
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{langlinks}{alt}<link rel="alternate" hreflang="x-default" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="plugreports">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ogimage or (SITE + "/assets/img/og.png")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#f59e0b">
<meta name="robots" content="max-image-preview:large">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/assets/img/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
{extra_head}{ld}
</head>
<body>
<div class="crisis"><div class="wrap"><span class="pulse"></span>
<strong data-i18n="crisis">Overdose or emergency? Call now</strong>
<span class="hide-s"><a href="/hotlines/" data-i18n="hotline">Hotlines</a> ·
<a href="tel:911">US 911</a> · <a href="tel:112">EU 112</a> ·
<a href="tel:000">AU 000</a> · <a href="tel:988">988 (US crisis)</a></span>
<a href="/hotlines/" style="margin-left:auto" data-i18n="hotline">Hotlines</a></div></div>
<header class="nav"><div class="wrap">
<a class="logo" href="/"><img src="/assets/img/logo.svg" alt="plugreports logo" width="34" height="34"><span>plug<em>reports</em></span></a>
<button class="burger" aria-label="Menu">&#9776;</button>
<nav class="nav-links">{navlinks}</nav></div></header>
{crumbs}
<main>{body}</main>
<footer><div class="wrap">
<div class="f-grid">
<div><a class="logo" href="/" style="color:#fff"><img src="/assets/img/logo.svg" alt="" width="30" height="30"><span>plug<em>reports</em></span></a>
<p style="font-size:13.5px;margin-top:12px;max-width:40ch">{esc(SETTINGS["tagline"])} Independent harm-reduction information — USA · Canada · Europe · Australia · Africa.</p>
<div class="lang-switch" id="langswitch">
<button data-lang="en">EN</button><button data-lang="es">ES</button><button data-lang="zh">中文</button>
<button data-lang="hi">हिन्दी</button><button data-lang="ar">عربي</button><button data-lang="pt">PT</button>
<button data-lang="ru">RU</button><button data-lang="ja">日本語</button><button data-lang="de">DE</button><button data-lang="fr">FR</button></div></div>
<div><h4>Library</h4><a href="/categories/opioids/">Opioids</a><a href="/categories/stimulants/">Stimulants</a><a href="/categories/benzodiazepines/">Benzodiazepines</a><a href="/categories/psychedelics/">Psychedelics</a><a href="/categories/empathogens/">Empathogens</a><a href="/categories/cannabinoids/">Synthetic cannabinoids</a></div>
<div><h4>Help</h4><a href="/hotlines/">Hotlines</a><a href="/rehabs/">Rehab centers</a><a href="/pharmacies/">Verified pharmacies</a><a href="/quit/">Quitting, day by day</a><a href="/sentencing/">Sentencing explained</a></div>
<div><h4>Updates</h4><a href="/news/">Drug news</a><a href="/busts/">Busts & seizures</a><a href="/topics/">Guides</a><a href="/suggest/">Suggest a correction</a><a href="/rss.xml">RSS feed</a><a href="/about/">About & editorial policy</a></div>
</div>
<div class="disclaimer"><b>DISCLAIMER.</b> plugreports.com is an independent harm-reduction information project. Content is compiled from public sources (NIDA, DEA, EMCDDA, WHO, CDC and peer-reviewed literature) for education and overdose prevention. It is <b>not medical advice, not legal advice, and not encouragement to use any substance</b>. Street prices, legal statuses and availability vary by region and change quickly — verify locally. If you or someone else may be overdosing, call your local emergency number immediately.
<div style="margin-top:10px">Primary data sources: <a href="https://nida.nih.gov" style="display:inline;color:#fbbf24" rel="noopener">NIDA</a> · <a href="https://www.dea.gov" style="display:inline;color:#fbbf24" rel="noopener">DEA</a> · <a href="https://www.cdc.gov" style="display:inline;color:#fbbf24" rel="noopener">CDC</a> · <a href="https://www.euda.europa.eu" style="display:inline;color:#fbbf24" rel="noopener">EMCDDA/EUDA</a> · <a href="https://www.who.int" style="display:inline;color:#fbbf24" rel="noopener">WHO</a> · <a href="https://www.samhsa.gov" style="display:inline;color:#fbbf24" rel="noopener">SAMHSA</a></div> If you are in crisis, contact a helpline on our <a href="/hotlines/" style="display:inline;color:#fbbf24">Hotlines</a> page. {esc(SETTINGS["crisisNote"])}</div>
<div class="f-bottom"><span>&copy; {TODAY[:4]} plugreports.com — harm reduction saves lives.</span><span>Built for fast, clear, life-saving information.</span></div>
</div></footer>
<div class="gate" id="agegate" hidden><div class="gate-card">
<img src="/assets/img/logo.svg" alt="" width="54" height="54" style="margin:0 auto">
<h2 data-i18n="ageTitle">Before you continue</h2>
<p data-i18n="ageBody">This site contains educational information about drugs and harm reduction. It is not medical or legal advice. You must be of legal age or accessing with intent to help yourself or someone else.</p>
<div class="row"><button class="btn btn-red" data-gate-yes data-i18n="ageYes">I understand — enter</button>
<a class="btn btn-ghost" href="https://www.google.com" data-i18n="ageNo">Leave</a></div></div></div>
<script src="/assets/js/app.js?v=6"></script>
</body></html>"""

def breadcrumb_ld(parts):
    return {"@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":f"{SITE}{u}"}
                               for i,(n,u) in enumerate(parts)]}

# ------------------------------------------------------------------ index ----
def build_index(es=False):
    idx = [{"n":d["name"],"a":", ".join(d["aliases"][:3]),"c":CATEGORIES[d["category"]]["name"],
            "u":f"/drugs/{d['slug']}/","col":CATEGORIES[d["category"]]["color"]} for d in DRUGS]
    tiles = []
    for d in DRUGS:
        c = CATEGORIES[d["category"]]
        tiles.append(f'''<a class="tile" href="/drugs/{d['slug']}/">
<span class="sched">{esc(d["schedule"].split("(")[0].strip()[:16])}</span>
<span class="glyph" style="background:{c['grad']}">{esc(d['name'][0])}</span>
<h3>{esc(d['name'])}</h3><span class="cat"><span class="cat-dot" style="background:{c['color']}"></span>{esc(c['name'])}</span></a>''')
    catpills = "".join(f'<a href="/categories/{k}/"><span class="cat-dot" style="background:{v["color"]}"></span>{esc(v["name"])} ({sum(1 for d in DRUGS if d["category"]==k)})</a>' for k,v in CATEGORIES.items())
    def card(href, chips, h, p, foot, img=None):
        thumb = f'<div class="thumb"><img src="{esc(img)}" alt="" loading="lazy"></div>' if img else ''
        return f'<a class="card" href="{href}">{thumb}<div class="meta">{chips}</div><h3>{esc(h)}</h3><p>{esc(p)}</p><div class="foot">{foot} &rarr;</div></a>'
    newscards = "".join(card(f"/news/{n['slug']}/", f'<span class="chip amber">{esc(n["tag"])}</span><span class="chip">{esc(n["date"])}</span>', n["title"], n["summary"], "Read", n.get("image")) for n in NEWS)
    def bust_chip(b):
        if b.get("confirmed"):
            return f'<span class="chip amber">CONFIRMED</span><span class="chip">{esc(b["date"])}</span>'
        return f'<span class="chip red">PENDING VERIFICATION</span><span class="chip">{esc(b["date"])}</span>'
    bustcards = "".join(card(f"/busts/{b['slug']}/", bust_chip(b), b["title"], b["summary"], b["location"] + " · " + b["agency"], b.get("image")) for b in BUSTS)
    important = [t for t in TOPICS if t.get('tag') == 'Important'] or [t for t in TOPICS if 'nasal-spray' in t['slug']]
    importantcards = "".join(card(f"/topics/{t['slug']}/", f'<span class="chip red">&#9888; IMPORTANT</span><span class="chip">{esc(t.get("read",""))}</span>', t["title"], t["desc"], "Read now", t.get("image")) for t in important)
    topiccards = "".join(card(f"/topics/{t['slug']}/", f'<span class="chip red">GUIDE</span><span class="chip">{esc(t["read"])}</span>', t["title"], t["desc"], "Read guide", t.get("image")) for t in TOPICS[:6])
    body = f"""
<section class="hero"><div class="wrap">
<span class="kicker">Harm-reduction library · {len(DRUGS)} substances · 5 regions</span>
<h1>Know the drug.<br>Know the <span class="mark">risk</span>.<br>Know the way out.</h1>
<p class="lede">plugreports is a visual directory of street drugs, adulterants, hotlines, busts and verified help — built so anyone can find clear, fast, life-saving information about any substance.</p>
<div class="hero-cta">
<a class="btn btn-red" href="/hotlines/">Get help now</a>
<a class="btn btn-amber" href="#library">Browse the library</a>
<a class="btn btn-ghost" href="/topics/what-actually-happens-when-you-quit/">Quitting, day by day</a></div>
<div class="hero-stats">
<div class="st"><b>{len(DRUGS)}</b><span>drug profiles</span></div>
<div class="st"><b>11</b><span>categories</span></div>
<div class="st"><b>20+</b><span>verified hotlines</span></div>
<div class="st"><b>{len(TOPICS)+len(QUIT_SPECS)}</b><span>guides & timelines</span></div></div></div></section>

<section class="quotes"><div class="wrap"><div class="quote-grid">
<blockquote class="qcard">&ldquo;The only safe medications are ones prescribed by a trusted medical professional and dispensed by a licensed pharmacist.&rdquo;<cite>&mdash; U.S. Drug Enforcement Administration, &ldquo;One Pill Can Kill&rdquo;</cite></blockquote>
<blockquote class="qcard">&ldquo;Fentanyl is the deadliest drug threat facing this country.&rdquo;<cite>&mdash; U.S. Drug Enforcement Administration</cite></blockquote>
</div></div></section>

<section class="sec" id="library"><div class="wrap">
<div class="sec-head"><div><span class="kicker amber">Drug Library</span>
<h2>Tap a <span class="grad">substance</span></h2><p>Glass tiles, two rows — scroll sideways. Every profile: effects, risks, overdose signs, street price, legal status, sources.</p></div>
<div class="searchbar" style="min-width:280px;flex:1;max-width:420px"><input id="libsearch" type="search" placeholder="Search name, street alias, category…" aria-label="Search drugs"></div></div>
<div id="searchresults" hidden></div>
<div class="pill-nav print-hide">{catpills}</div>
<div class="rail print-hide">{''.join(tiles)}</div>
<div class="notice-strip print-hide" style="margin-top:6px">Images for each substance are being added — profiles currently use clean placeholders. Facts are compiled from NIDA, DEA, EMCDDA and WHO sources.</div>
</div></section>

<section class="sec" style="background:#f9fafb"><div class="wrap" data-tabs>
<div class="sec-head"><div><span class="kicker">Updates</span><h2>News, busts & <span class="grad">guides</span></h2></div></div>
<div class="tabs print-hide">
<button class="tab active" data-tab="news">Drug News</button>
<button class="tab" data-tab="busts">Busts & Seizures</button>
<button class="tab" data-tab="topics">Guides</button>
<button class="tab" data-tab="important">Important</button></div>
<div class="tab-pane" data-pane="news"><div class="sortrow" data-sort="news">Sort: <button class="spill on" data-order="latest">Latest</button><button class="spill" data-order="trending">Trending</button></div><div class="cards">{newscards}</div><p style="margin-top:16px"><a class="btn btn-ghost" href="/news/">All news &rarr;</a></p></div>
<div class="tab-pane" data-pane="busts" hidden><div class="sortrow" data-sort="busts">Sort: <button class="spill on" data-order="latest">Latest</button><button class="spill" data-order="trending">Trending</button></div><div class="cards">{bustcards}</div><p style="margin-top:16px"><a class="btn btn-ghost" href="/busts/">All busts &rarr;</a></p></div>
<div class="tab-pane" data-pane="important" hidden><div class="sortrow" data-sort="important">Sort: <button class="spill on" data-order="latest">Latest</button><button class="spill" data-order="trending">Trending</button></div><div class="cards">{importantcards}</div><p style="margin-top:16px"><a class="btn btn-ghost" href="/topics/">All guides &rarr;</a></p></div>
<div class="tab-pane" data-pane="topics" hidden><div class="sortrow" data-sort="topics">Sort: <button class="spill on" data-order="latest">Latest</button><button class="spill" data-order="trending">Trending</button></div><div class="cards">{topiccards}</div><p style="margin-top:16px"><a class="btn btn-ghost" href="/topics/">All guides &rarr;</a></p></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><span class="kicker amber">Help</span><h2>Hotlines by <span class="grad">region</span></h2><p>Verified numbers across the USA, Canada, Europe, Australia and Africa.</p></div><a class="btn btn-red" href="/hotlines/">Full hotline directory</a></div>
<div class="hl-grid">{''.join(f'<div class="hl-card"><h3>{esc(r)}</h3><div class="num">{esc(v[0][0])}</div><div class="who">{esc(v[0][1])}</div><a class="call-btn" href="tel:{v[0][3]}">Call now</a></div>' for r,v in list(HOTLINES.items())[:4])}
</div></div></section>

<section class="sec" style="background:linear-gradient(180deg,#fff, #fffdf5)"><div class="wrap">
<div class="sec-head"><div><span class="kicker green">Verified directories</span>
<h2>Safe <span class="grad">sources</span></h2>
<p>Counterfeit pills kill thousands every year. These directories are checked against official registries before anything is listed.</p></div></div>
<div class="src-cta">
<div>
<h3>Most &ldquo;online pharmacies&rdquo; are counterfeit pill mills.</h3>
<p>The DEA&rsquo;s own testing shows most fake pills contain fentanyl or meth &mdash; and one wrong pill can kill. We list only sellers verified against official NABP and PharmacyChecker registries, so you never have to guess which site is real.</p>
</div>
<a class="btn-xlb" href="/pharmacies/">Browse verified pharmacies &rarr;</a>
</div></div></section>"""
    if es:
        from data_es import ES_HOME as ESH
        r = [("Harm-reduction library · " + str(len(DRUGS)) + " substances · 5 regions", ESH["kicker"]),
             ("Know the drug.<br>Know the <span class=\"mark\">risk</span>.<br>Know the way out.", ESH["h1"]),
             ("plugreports is a visual directory of street drugs, adulterants, hotlines, busts and verified help — built so anyone can find clear, fast, life-saving information about any substance.", ESH["lede"]),
             (">Get help now<", ">" + ESH["btn1"] + "<"), (">Browse the library<", ">" + ESH["btn2"] + "<"),
             (">Quitting, day by day<", ">" + ESH["btn3"] + "<"),
             (">drug profiles<", ">" + ESH["st1"] + "<"), (">categories<", ">" + ESH["st2"] + "<"),
             (">verified hotlines<", ">" + ESH["st3"] + "<"), (">guides & timelines<", ">" + ESH["st4"] + "<"),
             (">Help<", ">" + ESH["hl_kicker"] + "<"), (">Hotlines by region<", ">" + ESH["hl_h2"] + "<"),
             ("Verified numbers across the USA, Canada, Europe, Australia and Africa.", ESH["hl_p"]),
             (">Full hotline directory<", ">" + ESH["hl_btn"] + "<")]
        for a, b in r: body = body.replace(a, b)
        body = body.replace('href="/hotlines/"', 'href="/es/hotlines/"').replace('href="/topics/what-actually-happens-when-you-quit/"', 'href="/es/hotlines/"')
        w("es/index.html", shell("es/index.html",
            "plugreports — Biblioteca de información sobre drogas de calle: efectos, riesgos, sobredosis, líneas de ayuda",
            f"Biblioteca visual de reducción de riesgos: {len(DRUGS)} perfiles de drogas (efectos, riesgos, signos de sobredosis, precios), noticias, incautaciones y líneas de ayuda verificadas.",
            body, lang="es", canonical=f"{SITE}/es/", en_url=f"{SITE}/",
            extra_head=f"<script>window.DRUG_INDEX={json.dumps(idx, ensure_ascii=False)};</script>"))
        return
    ld = {"@context":"https://schema.org","@type":"WebSite","name":"plugreports","url":SITE,
          "description":"Harm-reduction library of street drug profiles, news, busts, hotlines and verified help."}
    w("index.html", shell("index.html",
        "plugreports — Street Drug Identifier: Effects, Overdose Signs, Street Prices & Hotlines",
        f"Identify street drugs fast: {len(DRUGS)} plain-English profiles with effects, overdose signs, street prices and legal status — plus drug busts, news, quitting day-by-day timelines, 24/7 hotlines and verified rehabs across the USA, Canada, Europe, Australia and Africa.",
        body, jsonld=ld, es_url=f"{SITE}/es/",
        extra_head=f"<script>window.DRUG_INDEX={json.dumps(idx, ensure_ascii=False)};</script>"))

# ------------------------------------------------------------- drug pages ----
def related_drugs(d, n=6):
    same = [x for x in DRUGS if x["category"] == d["category"] and x["slug"] != d["slug"]]
    return same[:n]

def drug_image(slug):
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        rel = f"assets/img/drugs/{slug}{ext}"
        if os.path.exists(os.path.join(PUB, rel)):
            return rel
    return "assets/img/drug-placeholder.svg"

def build_drugs(es=False):
    from data_es import ES_DRUGS, ES_CATS
    for d in DRUGS:
        qslug = None; qname = ""
        o = ES_DRUGS.get(d["slug"], {}) if es else {}
        if es and not o: continue
        c = CATEGORIES[d["category"]]
        cat_name = ES_CATS.get(d["category"], c["name"]) if es else c["name"]
        fx = o.get("effects", d["effects"]); rk = o.get("risks", d["risks"]); od = o.get("overdoseSigns", d["overdoseSigns"])
        app_ = o.get("appearance", d["appearance"]); pr = o.get("streetPrice", d["streetPrice"])
        lg = o.get("legalStatus", d["legalStatus"]); sch = o.get("schedule", d["schedule"])
        rel = [DRUG_BY_SLUG[x] for x in (d.get("related") or []) if x in DRUG_BY_SLUG] or related_drugs(d)
        ext_img = (d.get("image") or "").strip()
        img_rel = ext_img if ext_img.startswith("http") else drug_image(d["slug"])
        relhtml = "".join(f'<a href="/{("es/" if es and r["slug"] in ES_DRUGS else "")}drugs/{r["slug"]}/">{rel_card(r["slug"])}</a>' for r in rel)
        rows = "".join(f'<div class="fact"><b>{k}</b><span>{v}</span></div>' for k, v in [
            ("Also known as", ", ".join(d["aliases"])),
            ("Category", f'<span class="cat-dot" style="background:{c["color"]}"></span>{esc(cat_name)}'),
            ("Schedule / class", esc(sch)),
            ("Appearance", esc(app_)),
            ("Street price", esc(pr)),
            ("Legal status", esc(lg)),
            ("Last updated", esc(d["lastUpdated"]))])
        cat_rows = "".join(
            f'<tr><td><a href="/{("es/" if es and x["slug"] in ES_DRUGS else "")}drugs/{x["slug"]}/">{esc(x["name"])}</a></td>'
            f'<td>{esc(x["schedule"].split("(")[0].strip())}</td>'
            f'<td>{"; ".join(esc(e) for e in x["risks"][:2])}</td>'
            f'<td>{esc(x["streetPrice"].split(";")[0].split("(")[0].strip())}</td></tr>'
            for x in [d] + rel[:5])
        # --- FAQ (visible + FAQPage JSON-LD) ---
        od_a = "; ".join(od[:3])
        if d["category"] == "opioids":
            od_a += " Call emergency services immediately and give naloxone if available — it reverses opioid overdoses."
        else:
            od_a += " Call emergency services immediately."
        faqs = [
            (f"What does {d['name']} look like?", app_),
            (f"What are the signs of a {d['name']} overdose?", od_a),
            ("How addictive is it?", rk[0] + (" Withdrawal can be life-threatening — medical tapering is essential." if d["category"] in ("benzodiazepines", "depressants") else " Dependence can develop with regular use.")),
        ]
        faq_html = "".join(f"<details class=\"faq\"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
        # --- sources panel with real outbound authority links ---
        srcs = list(dict.fromkeys(d.get("sources", [])))
        links = [f'<a class="chip" href="{AGENCY_LINKS[x]}" target="_blank" rel="noopener">{esc(x)} &#8599;</a>' for x in srcs if x in AGENCY_LINKS]
        for label, url in DEEP_LINKS.get(d["slug"], []):
            links.append(f'<a class="chip green" href="{url}" target="_blank" rel="noopener">{esc(label)} &#8599;</a>')
        sources_html = f"""<div class="panel" style="margin-top:20px"><h2><span class="ic" style="background:#16a34a;color:#fff">&#128279;</span>Sources &amp; further reading</h2>
<p style="font-size:13.5px;color:var(--muted)">Facts on this page are compiled from these primary sources. External links open in a new tab.</p>
<div class="tagrow">{''.join(links)}</div></div>"""
        faq_panel = f"""<div class="panel" style="margin-top:20px"><h2><span class="ic" style="background:{c['color']};color:#fff">?</span>Frequently asked questions</h2>{faq_html}</div>"""
        brands_html = ""
        if d.get("brands"):
            bli = "".join(f'<span class="chip">{esc(b)}</span>' for b in d["brands"])
            brands_html = f"""<div class="panel" style="margin-top:20px"><h2><span class="ic" style="background:#4338ca;color:#fff">Rx</span>Brand names on the grey market</h2>
<p style="font-size:13.5px;color:var(--muted)">These brands are sold as this compound. Same molecule, different label and supply chain — quality varies enormously between them.</p>
<div class="tagrow">{bli}</div></div>"""
        cmp_head = f"Comparación de categoría — {esc(cat_name)}" if es else f"Category comparison — {esc(cat_name)}"
        body = f"""
<div class="wrap">
<section class="phead">
<span class="glyph" style="background:{c['grad']}">{esc(d['name'][0])}</span>
<div><span class="kicker" style="background:{c['grad']};color:#fff;border:0">{esc(cat_name)}</span>
<h1 style="margin-top:10px">{esc(d['name'])}</h1>
<p class="alias">Street names: <b>{esc(", ".join(d["aliases"]))}</b></p></div></section>

<img src="/{img_rel}" alt="{esc(d['name'])} — {esc(app_)}" style="width:100%;max-height:300px;object-fit:cover;border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow)" loading="lazy">

<div class="callout red print-hide"><b>Overdose? Act now.</b> Call emergency services — say "unresponsive, not breathing". Give naloxone for opioid-like signs. <a href="/hotlines/">Hotlines</a></div>

<div class="profile-grid">
<div class="panel"><h2><span class="ic" style="background:{c['color']};color:#fff">&#9889;</span>What it does</h2>
<ul class="ticks">{''.join(f"<li>{esc(e)}</li>" for e in fx)}</ul>
<h2 style="margin-top:22px"><span class="ic" style="background:#dc2626;color:#fff">&#9888;</span>Key risks</h2>
<ul class="ticks red">{''.join(f"<li>{esc(r)}</li>" for r in rk)}</ul>
<h2 style="margin-top:22px"><span class="ic" style="background:#111827;color:#fff">&#10010;</span>Overdose signs</h2>
<ul class="ticks red">{''.join(f"<li>{esc(o_)}</li>" for o_ in od)}</ul></div>
<div class="panel"><h2><span class="ic" style="background:{c['color']};color:#fff">&#128203;</span>Quick facts</h2>{rows}
<div style="margin-top:14px"><span class="chip green">Sources: {esc(", ".join(d["sources"]))}</span></div></div>
</div>

<div class="panel"><h2>{cmp_head}</h2>
<table class="tbl"><thead><tr><th>Substance</th><th>Class</th><th>Top risks</th><th>Street price</th></tr></thead>
<tbody>{cat_rows}</tbody></table>
<div class="notice-strip">Street prices are regional estimates. Potency and cuts vary constantly.</div></div>

{brands_html}
{faq_panel}
{sources_html}

<div class="related print-hide"><h2>You may also want to know about</h2>
<div class="rel-grid">{relhtml}
<a href="/topics/fentanyl-numbers/"><span class="mini" style="background:#b45309">&#128218;</span><span>Fentanyl: the numbers</span></a>
<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>
{f'<a href="/drugs/{qslug}/"><span class="mini" style="background:#d97706">{esc(qname[0])}</span><span>About {esc(qname)}</span></a>' if qslug else ''}
<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>
<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a></div></div>
</div>"""
        if es:
            title = f"{d['name']}: efectos, riesgos, signos de sobredosis y precio | plugreports"
            desc = f"{d['name']} ({', '.join(d['aliases'][:3])}) — {cat_name}. Efectos: {'; '.join(fx[:2])}. Riesgos: {'; '.join(rk[:2])}. Información de reducción de riesgos actualizada {d['lastUpdated']}."
            out = f"es/drugs/{d['slug']}/index.html"
            w(out, shell(out, title, desc, body, lang="es", canonical=f"{SITE}/es/drugs/{d['slug']}/", en_url=f"{SITE}/drugs/{d['slug']}/"))
        else:
            title = d.get("seoTitle") or f"{d['name']}: Effects, Risks, Overdose Signs, Street Price & Legal Status | plugreports"
            desc = d.get("seoDesc") or f"{d['name']} ({', '.join(d['aliases'][:3])}) — {cat_name}. Effects: {'; '.join(d['effects'][:2])}. Risks: {'; '.join(d['risks'][:2])}. Overdose signs, street price and legal status, updated {d['lastUpdated']}."
            ld = [{"@context":"https://schema.org","@type":"MedicalWebPage",
                   "name":title,"url":f"{SITE}/drugs/{d['slug']}/","lastReviewed":d["lastUpdated"],
                   "about":{"@type":"Drug","name":d["name"],"alternateName":d["aliases"],
                            "drugClass":cat_name,"legalStatus":d["legalStatus"]},
                   "audience":{"@type":"Audience","audienceType":"People seeking harm-reduction information"},
                   "medicalAudience":{"@type":"MedicalAudience","audienceType":"Patient"}},
                  breadcrumb_ld([("Home","/"),(cat_name,f"/categories/{d['category']}/"),(d["name"],"")]),
                  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}]
            es_url = f"{SITE}/es/drugs/{d['slug']}/" if d["slug"] in ES_DRUGS else None
            og = img_rel if img_rel.startswith("http") else (f"{SITE}/{img_rel}" if "drugs/" in img_rel else None)
            w(f"drugs/{d['slug']}/index.html", shell(f"drugs/{d['slug']}/index.html", title, desc, body, jsonld=ld, ogimage=og, es_url=es_url))


def build_categories():
    qslug = None; qname = ""
    for k, c in CATEGORIES.items():
        items = [d for d in DRUGS if d["category"] == k]
        cards = "".join(f'''<a class="card" href="/drugs/{d['slug']}/">
<div class="meta"><span class="chip" style="border-color:{c['color']}33;color:{c['color']}">{esc(d["schedule"].split("(")[0].strip())}</span></div>
<h3>{esc(d['name'])}</h3><p>{esc(d['appearance'])}</p>
<div class="foot">Effects &amp; risks &rarr;</div></a>''' for d in items)
        body = f"""<div class="wrap">
<section class="cat-hero" style="background:{c['grad']}"><span class="kicker" style="background:rgba(255,255,255,.15);color:#fff;border:0">{len(items)} substances</span>
<h1>{esc(c['name'])}</h1><p>{esc(c['tagline'])} {esc(c['blurb'])}</p>
<div class="catstats"><div><b>{esc(c['stat'][0])}</b><span>{esc(c['stat'][1])}</span></div>
<div><b>{len(items)}</b><span>profiles in this category</span></div></div></section>
<div class="cards">{cards}</div>
<div class="related print-hide"><h2>Related reading</h2><div class="rel-grid">
<a href="/topics/what-is-xylazine/"><span class="mini" style="background:#b45309">&#128218;</span><span>Xylazine (Tranq) explainer</span></a>
<a href="/topics/fentanyl-numbers/"><span class="mini" style="background:#dc2626">&#128218;</span><span>Fentanyl: the numbers</span></a>
<a href="/hotlines/"><span class="mini" style="background:#16a34a">&#9742;</span><span>Hotlines</span></a></div></div></div>"""
        title = f"{c['name']} — Effects, Risks & Street Info ({len(items)} drugs) | plugreports"
        desc = f"{c['tagline']} {len(items)} harm-reduction profiles: effects, overdose signs, street prices, legal status."
        w(f"categories/{k}/index.html", shell(f"categories/{k}/index.html", title, desc, body,
          jsonld=[{"@context":"https://schema.org","@type":"CollectionPage","name":title}, breadcrumb_ld([("Home","/"),(c["name"],"")])]))

# ---------------------------------------------------- news / busts/topics ----
def build_news():
    idx_cards = "".join(f'''<a class="card" href="/news/{n['slug']}/"><div class="meta">
<span class="badge-live">{esc(n["tag"]).upper()}</span><span class="chip">{esc(n["date"])}</span></div>
<h3>{esc(n['title'])}</h3><p>{esc(n['summary'])}</p><div class="foot">Read &rarr;</div></a>''' for n in NEWS)
    w("news/index.html", shell("news/index.html", "Drug News & Supply Alerts | plugreports",
      "Drug news, adulterant alerts and supply trends: nitazenes, xylazine, high-dose pills, counterfeit pharmaceuticals — with sources.",
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker">Newsroom</span><h2>Drug news & alerts</h2><p>Sourced from NIDA, DEA, EMCDDA, ONS and drug-checking services. Subscribe via <a href="/rss.xml">RSS</a>.</p></div></div><div class="cards">{idx_cards}</div></div>'))
    for n in NEWS:
        body = "".join(f"<p>{p}</p>" for p in n["body"])
        rels = "".join(f'<a href="/drugs/{s}/">{rel_card(s)}</a>' for s in n.get("drugsInvolved", []))
        full = f"""<div class="wrap"><article class="article" style="padding-top:26px">
<span class="kicker">{esc(n['tag'])}</span><h1 style="margin-top:12px">{esc(n['title'])}</h1>
<div class="byline"><span>{esc(n['date'])}</span><span>Sources: {esc(', '.join(n['sources']))}</span></div>
{f'<img class="detail-img" src="{esc(n["image"])}" alt="" loading="lazy">' if n.get("image") else ""}
<p class="lede" style="font-size:18px">{esc(n['summary'])}</p>{body}
{help_links(n.get("drugsInvolved", []), [("All drug news", "/news/", "#dc2626")], related=n.get("related"))}</article></div>"""
        ld = {"@context":"https://schema.org","@type":"NewsArticle","headline":n["title"],
              "datePublished":n["date"],"dateModified":n["date"],"author":{"@type":"Organization","name":"plugreports"},
              "publisher":{"@type":"Organization","name":"plugreports"},"mainEntityOfPage":f"{SITE}/news/{n['slug']}/"}
        w(f"news/{n['slug']}/index.html", shell(f"news/{n['slug']}/index.html", f"{n['title']} | plugreports", n["summary"], full, jsonld=ld))

def build_busts():
    cards = "".join(f'''<a class="card" href="/busts/{b['slug']}/"><div class="meta">
<span class="chip {"red" if not b.get("confirmed") else "amber"}">{"&#9888; PENDING VERIFICATION" if not b.get("confirmed") else "&#10004; CONFIRMED"}</span>
<span class="chip">{esc(b["date"])}</span></div><h3>{esc(b['title'])}</h3><p>{esc(b['summary'])}</p>
<div class="foot">{esc(b["location"])} · {esc(b["agency"])} &rarr;</div></a>''' for b in BUSTS)
    w("busts/index.html", shell("busts/index.html", "Drug Busts & Seizures Tracker | plugreports",
      "Recent drug busts and seizures worldwide: location, agency, substances, quantities and sentencing exposure. Pending items are marked until editor-verified.",
      f'''<div class="wrap"><section class="sec-head" style="padding-top:30px"><div>
<span class="kicker">Enforcement tracker</span><h2>Busts & seizures</h2>
<p>Each report lists agency, location, substances involved and potential sentencing. Items marked <b>pending verification</b> are awaiting editor confirmation from source material — we never publish unverified seizure claims as fact.</p></div></div>
<div class="cards">{cards}</div>
<div class="callout amber"><b>Editorial policy</b>Bust entries are only published as fact after verification against an official agency release or credible reporting. Source links are attached to every entry.</div></div>'''))
    for b in BUSTS:
        flag = "PENDING VERIFICATION" if not b.get("confirmed") else "CONFIRMED"
        drugs = "".join(f'<a href="/drugs/{s}/">{rel_card(s)}</a>' for s in b.get("drugsInvolved", []))
        src = f'<p><b>Source:</b> <a href="{esc(b["sourceUrl"])}" rel="nofollow noopener">{esc(b["sourceUrl"])}</a></p>' if b.get("sourceUrl") else ""
        body = f"""<div class="wrap"><article class="article" style="padding-top:26px">
<span class="kicker">{flag}</span><h1 style="margin-top:12px">{esc(b['title'])}</h1>
<div class="byline"><span>{esc(b['date'])}</span><span>{esc(b['location'])}</span><span>Agency: {esc(b['agency'])}</span></div>
{f'<img class="detail-img" src="{esc(b["image"])}" alt="" loading="lazy">' if b.get("image") else ""}
<div class="figure"><table class="tbl"><tbody>
<tr><th style="width:160px">Date</th><td>{esc(b['date'])}</td></tr>
<tr><th>Location</th><td>{esc(b['location'])}</td></tr>
<tr><th>Agency</th><td>{esc(b['agency'])}</td></tr>
<tr><th>Sentencing exposure</th><td>{esc(b['sentencing'])}</td></tr></tbody></table></div>
<p>{esc(b['summary'])}</p>{src}
{help_links(b.get("drugsInvolved", []), [("How to read bust news", "/topics/drug-busts-this-week/", "#b45309")], related=b.get("related"))}
<div class="callout amber"><b>Why busts matter for safety</b>Major seizures destabilize local supply — potency swings for weeks afterwards. See our guide: <a href="/topics/drug-busts-this-week/">how to read bust news</a>.</div>
</article></div>"""
        w(f"busts/{b['slug']}/index.html", shell(f"busts/{b['slug']}/index.html", f"{b['title']} | plugreports", b["summary"][:155], body))

def build_topics():
    cards = "".join(f'''<a class="card" href="/topics/{t['slug']}/"><div class="meta">
<span class="chip red">GUIDE</span><span class="chip">{esc(t["read"])}</span><span class="chip">{esc(t["date"])}</span></div>
<h3>{esc(t['title'])}</h3><p>{esc(t['desc'])}</p><div class="foot">Read guide &rarr;</div></a>''' for t in TOPICS)
    w("topics/index.html", shell("topics/index.html", "Drug Guides & Explainers | plugreports",
      "Visual explainers: xylazine, fentanyl numbers, pressed pills, nitazenes, krokodil facts, sentencing, talking to your kids, quitting day by day.",
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker amber">Guides</span><h2>Explainers & deep-dives</h2><p>Written for fast reading: tables, timelines and callouts instead of walls of text.</p></div></div><div class="cards">{cards}</div></div>'))
    for t in TOPICS:
        inner = render_blocks(t["blocks"], resolve_slug)
        mentioned = t.get("drugsInvolved") or [x for b in t["blocks"] if b[0] == "related" for x in b[1] if x in DRUG_BY_SLUG]
        inner += help_links(mentioned, related=t.get("related"))
        links = t.get("links", [])
        if links:
            inner += '<div class="related print-hide"><h2>Full day-by-day guides</h2><div class="rel-grid">' + "".join(
                f'<a href="/{u}/">{rel_card(u.split("/")[-1])}</a>' for u in links) + "</div></div>"
        body = f"""<div class="wrap"><article class="article" style="padding-top:26px">
<span class="kicker amber">GUIDE · {esc(t['read'])} read</span>
<h1 style="margin-top:12px">{esc(t['title'])}</h1>
<div class="byline"><span>Updated {esc(t['date'])}</span><span>Reviewed against NIDA / DEA / EMCDDA sources</span>
<span><a href="/suggest/">Suggest a correction</a></span></div>{f'<img class="detail-img" src="{esc(t["image"])}" alt="" loading="lazy">' if t.get("image") else ""}</article>
<article class="article">{inner}</article></div>"""
        ld = {"@context":"https://schema.org","@type":"Article","headline":t["title"],
              "datePublished":t["date"],"dateModified":t["date"],
              "author":{"@type":"Organization","name":"plugreports"},
              "publisher":{"@type":"Organization","name":"plugreports"},"mainEntityOfPage":f"{SITE}/topics/{t['slug']}/"}
        w(f"topics/{t['slug']}/index.html", shell(f"topics/{t['slug']}/index.html", f"{t['title']} | plugreports", t["desc"][:155], body, jsonld=ld))

def build_quit():
    cards = "".join(f'''<a class="card" href="/quit/{k}/"><div class="meta">
<span class="chip green">DAY-BY-DAY</span><span class="chip">{esc(v["cat"])}</span></div>
<h3>Quitting {esc(v['name'])}</h3><p>{esc(v['danger'][:120])}…</p><div class="foot">Full timeline &rarr;</div></a>''' for k, v in QUIT_SPECS.items())
    w("quit/index.html", shell("quit/index.html", "What Happens When You Quit Drugs — Day-by-Day Timelines | plugreports",
      "Honest withdrawal timelines: heroin, fentanyl, cocaine, meth, MDMA, Xanax, ketamine, GHB. What's normal, what hurts, when it ends, and when detox must be medical.",
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker green">Recovery</span><h2>Quitting — day by day</h2><p>Start with the <a href="/topics/what-actually-happens-when-you-quit/">master explainer</a>, then pick your substance.</p></div></div><div class="cards">{cards}</div></div>'))
    for k, v in QUIT_SPECS.items():
        qslug = k if k in DRUG_BY_SLUG else ("methamphetamine" if k == "meth" else None)
        qname = DRUG_BY_SLUG[qslug]["name"] if qslug else v["name"]
        tl = "".join(f'<div class="tl-item{" red" if i==1 else ""}"><h4>{esc(when)} — {esc(t_)}</h4><p>{esc(tx)}</p></div>' for i,(when,t_,tx) in enumerate(v["days"]))
        tips = "".join(f"<li>{esc(x)}</li>" for x in v["tips"])
        body = f"""<div class="wrap"><article class="article" style="padding-top:26px">
<span class="kicker green">DAY-BY-DAY TIMELINE</span>
<h1 style="margin-top:12px">What happens when you quit {esc(v['name'])}</h1>
<div class="byline"><span>Category: {esc(v['cat'])}</span><span>Updated {TODAY}</span></div>
{f'<img class="detail-img" src="{esc(v.get("image"))}" alt="" loading="lazy">' if v.get("image") else ""}
<div class="callout {'red' if v['cat'] in ('Benzodiazepine','Depressant') else 'amber'}"><b>Read this first</b>{esc(v['danger'])}</div>
<h2>The timeline</h2>
<div class="timeline">{tl}</div>
<h2>What actually helps</h2>
<ul class="checklist">{tips}</ul>
<div class="callout green"><b>The relapse rule</b>After even a week clean, your tolerance drops dramatically — an old dose can kill. If you slip: treat it like your first time, never use alone, keep naloxone close.</div>
<div class="related print-hide"><h2>You may also want to know about</h2><div class="rel-grid">
<a href="/topics/what-actually-happens-when-you-quit/"><span class="mini" style="background:#b45309">&#128218;</span><span>The master quitting explainer</span></a>
{f'<a href="/drugs/{qslug}/"><span class="mini" style="background:#d97706">{esc(qname[0])}</span><span>About {esc(qname)}</span></a>' if qslug else ''}
{''.join(f'<a href="/{resolve_slug(r)}/">{rel_card(r)}</a>' for r in (v.get("related") or []))}
<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>
<a href="/rehabs/"><span class="mini" style="background:#16a34a">&#10010;</span><span>Verified rehab centers</span></a></div></div>
</article></div>"""
        title = f"What Happens When You Quit {v['name']} — Day-by-Day Withdrawal Timeline | plugreports"
        desc = f"Quitting {v['name']} ({v['cat']}): day-by-day withdrawal timeline, peak symptoms, how long it lasts, and when medical detox is essential."
        w(f"quit/{k}/index.html", shell(f"quit/{k}/index.html", title, desc, body))

# ------------------------------------------------- help / directory pages ----
def build_hotlines(es=False):
    qslug = None; qname = ""
    from data_es import ES_REGIONS, ES_HOTLINES, ES_HOME as ESH
    secs = []
    for region, items in HOTLINES.items():
        rname = ES_REGIONS.get(region, region) if es else region
        trans = ES_HOTLINES.get(region, []) if es else []
        cards = "".join(f'''<div class="hl-card"><h3>{esc(trans[i][0] if es and i < len(trans) else it[1])}</h3>
<div class="num">{esc(it[0])}</div><div class="who">{esc(trans[i][1] if es and i < len(trans) else it[2])}</div>
{f'<a class="call-btn" href="tel:{it[3]}">&#128222; {"Llamar ahora" if es else "Call now"}</a>' if it[3] else '<span class="chip" style="margin-top:12px">Text-based service</span>'}</div>''' for i, it in enumerate(items))
        secs.append(f'<section class="hl-region"><span class="kicker amber">{esc(rname)}</span><div class="hl-grid">{cards}</div></section>')
    if es:
        body = f"""<div class="wrap"><div style="padding-top:26px">
<span class="kicker">Directorio de ayuda</span><h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Líneas de ayuda — ayuda en cualquier lugar</h1>
<p class="lede" style="color:#667085;max-width:64ch">Números verificados de sobredosis, crisis y tratamiento en EE. UU., Canadá, Europa, Australia y África. Verifica siempre antes de depender de un número.</p>
{''.join(secs)}
<div class="callout red"><b>¿Sobredosis ahora?</b>Llama primero a tu número de emergencia local. Luego naloxona si la tienes. Luego respiración de rescate. El orden importa.</div>
</div></div>"""
        w("es/hotlines/index.html", shell("es/hotlines/index.html",
          "Líneas de ayuda para sobredosis y adicción — EE. UU., Canadá, Europa, Australia, África | plugreports",
          "Números verificados 24/7: emergencias, ayuda en sobredosis, crisis (988/112), referencias de tratamiento para las cinco regiones.",
          body, lang="es", canonical=f"{SITE}/es/hotlines/", en_url=f"{SITE}/hotlines/"))
        return
    body = f"""<div class="wrap"><div style="padding-top:26px">
<span class="kicker">Help directory</span><h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Hotlines — help anywhere</h1>
<p class="lede" style="color:#667085;max-width:64ch">Verified overdose, crisis and treatment helplines across the USA, Canada, Europe, Australia and Africa. Numbers verified against official sources; always re-verify before relying on a listing.</p>
{''.join(secs)}
<div class="callout red"><b>Overdose right now?</b>Call your local emergency number FIRST. Then naloxone if you have it. Then rescue breathing. Order matters.</div>
{help_links(["fentanyl", "xylazine", "heroin", "cocaine"], [("Sentencing explained", "/sentencing/", "#111827")])}
<div class="callout green"><b>Found an outdated number?</b><a href="/suggest/">Tell us</a> — hotline listings are reviewed monthly.</div>
</div></div>"""
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":"What number do I call for a drug overdose in the US?",
         "acceptedAnswer":{"@type":"Answer","text":"Call 911 immediately. If naloxone is available, administer it while waiting for help."}},
        {"@type":"Question","name":"Is there a 24/7 drug helpline?",
         "acceptedAnswer":{"@type":"Answer","text":"Yes — SAMHSA's National Helpline (1-800-662-4357) is free, confidential and open 24/7 in the US."}}]}
    w("hotlines/index.html", shell("hotlines/index.html", "Drug Overdose & Addiction Hotlines — USA, Canada, Europe, Australia, Africa | plugreports",
      "Verified 24/7 hotlines: emergency numbers, overdose help, suicide crisis (988/112), treatment referral (SAMHSA, FRANK, Lifeline) for all five regions.",
      body, jsonld=faq, es_url=f"{SITE}/es/hotlines/"))


def build_sentencing():
    qslug = None; qname = ""
    secs = []
    for s in SENTENCING:
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in s["table"][1:])
        head = "".join(f"<th>{esc(c)}</th>" for c in s["table"][0])
        secs.append(f'''<div class="legal-doc" style="margin-bottom:22px"><span class="seal">INFO<br>ONLY</span>
<h2 style="margin-top:0">{esc(s["region"])}</h2><p style="color:#667085">{esc(s["summary"])}</p>
<table class="tbl"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>''')
    body = f"""<div class="wrap"><div style="padding-top:26px">
<span class="kicker">Legal information</span><h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Drug sentencing, explained</h1>
<p class="lede" style="color:#667085;max-width:68ch">What possession and trafficking actually cost across the USA, Canada, the UK/EU, Australia and Africa — and why <b>calling 911 during an overdose is always worth it</b> (Good Samaritan protections).</p>
<div class="callout amber" style="margin:18px 0 26px"><b>Not legal advice</b>Sentencing law changes constantly and facts decide cases. Consult a licensed lawyer in your jurisdiction. This page exists so no one learns the system the hard way.</div>
{''.join(secs)}
<div class="related print-hide"><h2>Related reading</h2><div class="rel-grid">
<a href="/topics/sentencing-explained/"><span class="mini" style="background:#b45309">&#128218;</span><span>Full sentencing guide</span></a>
<a href="/topics/talk-to-your-kid/"><span class="mini" style="background:#16a34a">&#128218;</span><span>Talking to your kids</span></a>
<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a></div></div>
</div></div>"""
    w("sentencing/index.html", shell("sentencing/index.html", "Drug Possession Sentences by Country — US, Canada, UK/EU, Australia, Africa | plugreports",
      "Drug sentencing tables: possession and trafficking penalties per region, Good Samaritan laws, mandatory minimums, and what to do if arrested.", body))

def build_directory(name, items, singular, title, desc, thumb):
    qslug = None; qname = ""
    cards = "".join(f'''<a class="card" href="/{name}/{it['slug']}/">
<div class="thumb" style="height:110px;background:linear-gradient(135deg,#fef3c7,#fee2e2);display:grid;place-items:center;font-size:34px">{thumb}</div>
<h3>{esc(it['name'])}</h3><p>{esc(it['desc'][:130])}…</p>
<div class="foot">{esc(it['region'])} &rarr;</div></a>''' for it in items)
    w(f"{name}/index.html", shell(f"{name}/index.html", title, desc,
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker green">Verified directory</span><h2>{esc(title.split("|")[0].strip())}</h2><p>Every listing is checked against official accreditation/registries before publishing. <a href="/suggest/">Recommend a facility</a>.</p></div></div><div class="dir-grid">{cards}</div></div>'))
    for it in items:
        body = f"""<div class="wrap"><div style="max-width:760px;padding:26px 0">
<span class="kicker green">{'&#10004; VERIFIED' if it.get('verified') else 'LISTING'}</span>
<h1 style="font-size:clamp(26px,4vw,38px);margin-top:10px">{esc(it['name'])}</h1>
<div class="tagrow"><span class="chip amber">{esc(it['region'])}</span></div>
<div class="thumb" style="height:180px;background:linear-gradient(135deg,#fef3c7,#fee2e2);display:grid;place-items:center;font-size:44px;border-radius:16px;margin:16px 0">{thumb}</div>
<p style="font-size:16.5px">{esc(it['desc'])}</p>
<div class="fact" style="margin-top:18px"><b>Website</b><span><a href="{esc(it['website'])}" rel="noopener">{esc(it['website'])}</a></span></div>
{f'<div class="fact"><b>Contact</b><span>{esc(it["phone"])}</span></div>' if it.get('phone') else ''}
<div class="callout green" style="margin-top:18px"><b>In crisis right now?</b>Skip the directory — call your emergency number or a <a href="/hotlines/">hotline</a> first.</div>
<div class="related print-hide"><h2>You may also want to know about</h2><div class="rel-grid">
{f'<a href="/drugs/{qslug}/"><span class="mini" style="background:#d97706">{esc(qname[0])}</span><span>About {esc(qname)}</span></a>' if qslug else ''}
{''.join(f'<a href="/{resolve_slug(r)}/">{rel_card(r)}</a>' for r in (it.get("related") or []))}
<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>
<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>
<a href="/rehabs/"><span class="mini" style="background:#16a34a">&#10010;</span><span>All rehab centers</span></a>
<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a></div></div>
</div></div>"""
        w(f"{name}/{it['slug']}/index.html", shell(f"{name}/{it['slug']}/index.html", f"{it['name']} — {singular} in {it['region']} | plugreports", it["desc"][:155], body))

def build_about():
    body = """<div class="wrap"><div style="max-width:780px;padding:26px 0">
<span class="kicker amber">About us</span>
<h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Why plugreports exists</h1>
<p class="lede" style="color:#667085">People don't die from lack of morals — they die from lack of information. Nobody who took a counterfeit oxycodone pill knew it was fentanyl. plugreports exists to close that gap.</p>
<h2 style="margin-top:28px">What we do</h2>
<ul class="ticks">
<li><b>Visual-first drug profiles</b> — effects, risks, overdose signs and street reality in scannable panels, not paragraphs.</li>
<li><b>Verified help directories</b> — hotlines, rehabs and pharmacies checked against official registries.</li>
<li><b>Sourced news & busts</b> — supply trends and enforcement actions with named sources; nothing published as fact without verification.</li>
<li><b>Five regions</b> — USA, Canada, Europe, Australia and Africa, with localized hotlines and sentencing info.</li></ul>
<h2>Editorial policy</h2>
<ul class="ticks">
<li>Content is compiled from NIDA, DEA, CDC, EMCDDA, WHO and peer-reviewed literature, and reviewed before publication.</li>
<li>We do not publish unverified seizure claims; pending items are visibly marked.</li>
<li>We are not medical or legal professionals. Nothing here is medical or legal advice.</li>
<li>Corrections: <a href="/suggest/">submit one</a> — they go directly to the editorial queue.</li></ul>
<h2>Our stance</h2>
<p>We are a harm-reduction project. We do not encourage drug use of any kind — we recognize that people use drugs, and that accurate information saves lives. Every profile on this site treats the reader as someone who may need help tonight, not as a statistic.</p>
<div class="callout red" style="margin-top:22px"><b>Crisis?</b><a href="/hotlines/">Go to hotlines</a> — or call your local emergency number now.</div>
</div></div>"""
    w("about/index.html", shell("about/index.html", "About plugreports — Harm-Reduction Mission & Editorial Policy",
      "plugreports is an independent harm-reduction library: visual drug profiles, verified hotlines and rehabs, sourced busts and news for USA, Canada, Europe, Australia and Africa.", body))

def build_suggest():
    body = """<div class="wrap"><div style="max-width:640px;padding:26px 0">
<span class="kicker amber">Community input</span>
<h1 style="font-size:clamp(26px,4vw,38px);margin-top:10px">Suggest a correction or update</h1>
<p style="color:#667085">Wrong price? Outdated hotline? A bust we should cover? Submit it — reviewed by a human before anything changes.</p>
<form id="suggestform" style="margin-top:20px;display:flex;flex-direction:column;gap:14px">
<div class="fact" style="grid-template-columns:130px 1fr"><b>Type</b><select name="type" style="padding:10px;border:1px solid #e4e7ec;border-radius:10px;font-family:inherit">
<option>Correction</option><option>Hotline update</option><option>Bust report / source</option><option>New substance</option><option>Pharmacy / rehab listing</option><option>Other</option></select></div>
<input name="name" required placeholder="Your name or alias" style="padding:13px 16px;border:1px solid #e4e7ec;border-radius:12px;font-family:inherit">
<input name="contact" placeholder="Email (optional)" style="padding:13px 16px;border:1px solid #e4e7ec;border-radius:12px;font-family:inherit">
<textarea name="message" required rows="5" placeholder="What's wrong or missing? Include sources if you have them." style="padding:13px 16px;border:1px solid #e4e7ec;border-radius:12px;font-family:inherit"></textarea>
<button class="btn btn-red" type="submit">Submit</button></form>
<div id="suggest-ok" class="callout green" hidden><b>Received.</b>Thank you — it is in the editorial queue.</div>
</div></div>"""
    w("suggest/index.html", shell("suggest/index.html", "Suggest a Correction | plugreports",
      "Help keep plugreports accurate: report wrong info, outdated hotlines, missing busts or new substances.", body))

# ------------------------------------------------------------- meta files ----
def build_meta():
    urls = ["", "news/", "busts/", "topics/", "quit/", "hotlines/", "sentencing/",
            "pharmacies/", "rehabs/", "about/", "suggest/", "admin/"]
    urls += [f"categories/{k}/" for k in CATEGORIES]
    urls += [f"drugs/{d['slug']}/" for d in DRUGS]
    urls += [f"news/{n['slug']}/" for n in NEWS]
    urls += [f"busts/{b['slug']}/" for b in BUSTS]
    urls += [f"topics/{t['slug']}/" for t in TOPICS]
    urls += [f"quit/{k}/" for k in QUIT_SPECS]
    urls += [f"pharmacies/{p['slug']}/" for p in PHARMACIES]
    urls += [f"rehabs/{r['slug']}/" for r in REHABS]
    today = TODAY
    sm = "\n".join(f'<url><loc>{SITE}/{u}</loc><lastmod>{today}</lastmod></url>' for u in urls)
    w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>')
    w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {SITE}/sitemap.xml")
    items = "".join(f"<item><title>{esc(n['title'])}</title><link>{SITE}/news/{n['slug']}/</link><description>{esc(n['summary'])}</description><pubDate>{n['date']}</pubDate></item>" for n in NEWS)
    w("rss.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>plugreports — Drug News</title><link>{SITE}/news/</link>{items}</channel></rss>')
    w("llms.txt", f"# plugreports\n\n> Harm-reduction library of street drug profiles, busts, hotlines and verified help. USA, Canada, Europe, Australia, Africa.\n\n## Key pages\n- [/hotlines/]({SITE}/hotlines/) Verified overdose & crisis hotlines, 5 regions\n- [/drugs/fentanyl/]({SITE}/drugs/fentanyl/) Fentanyl profile\n" + "".join(f"- [/drugs/{d['slug']}/]({SITE}/drugs/{d['slug']}/) {d['name']} ({CATEGORIES[d['category']]['name']})\n" for d in DRUGS[:40]))


def build_indexes():
    cards = "".join(
        "<a class=\"card\" href=\"/categories/" + k + "/\"><div class=\"meta\"><span class=\"chip\" style=\"border-color:" + v["color"] + "33;color:" + v["color"] + "\">" + str(sum(1 for d in DRUGS if d["category"] == k)) + " substances</span></div><h3>" + esc(v["name"]) + "</h3><p>" + esc(v["tagline"]) + "</p><div class=\"foot\">Browse category &rarr;</div></a>"
        for k, v in CATEGORIES.items())
    w("categories/index.html", shell("categories/index.html",
        "Drug Categories — Opioids, Stimulants, Benzos, Psychedelics & More | plugreports",
        "Browse all drug categories: opioids, stimulants, benzodiazepines, psychedelics, dissociatives, synthetic cannabinoids and more — harm-reduction profiles for every substance.",
        "<div class=\"wrap\"><section class=\"sec-head\" style=\"padding-top:30px\"><div><span class=\"kicker amber\">Drug Library</span><h2 style=\"font-family:var(--font-ed);font-size:clamp(28px,4vw,44px)\">All <span style=\"background:linear-gradient(92deg,#f59e0b,#dc2626);-webkit-background-clip:text;background-clip:text;color:transparent\">categories</span></h2><p>" + str(len(CATEGORIES)) + " categories, " + str(len(DRUGS)) + " substances — every profile covers effects, overdose signs, street prices and legal status.</p></div></section><div class=\"cards\">" + cards + "</div></div>"))
    tiles = "".join(
        "<a class=\"tile\" href=\"/drugs/" + d["slug"] + "/\"><span class=\"glyph\" style=\"background:" + CATEGORIES[d["category"]]["grad"] + "\">" + esc(d["name"][0]) + "</span><h3>" + esc(d["name"]) + "</h3><span class=\"cat\"><span class=\"cat-dot\" style=\"background:" + CATEGORIES[d["category"]]["color"] + "\"></span>" + esc(CATEGORIES[d["category"]]["name"]) + "</span></a>"
        for d in sorted(DRUGS, key=lambda x: x["name"]))
    w("drugs/index.html", shell("drugs/index.html",
        "All " + str(len(DRUGS)) + " Drugs A-Z — Street Names, Effects, Overdose Signs | plugreports",
        "Complete A-Z index of " + str(len(DRUGS)) + " street drugs and pharmaceuticals: street names, effects, overdose signs, street prices and legal status.",
        "<div class=\"wrap\"><section class=\"sec-head\" style=\"padding-top:30px\"><div><span class=\"kicker amber\">A-Z Index</span><h2 style=\"font-family:var(--font-ed);font-size:clamp(28px,4vw,44px)\">All <span style=\"background:linear-gradient(92deg,#f59e0b,#dc2626);-webkit-background-clip:text;background-clip:text;color:transparent\">" + str(len(DRUGS)) + " substances</span>, A to Z</h2><p>Tap any substance for effects, risks, overdose signs and street info.</p></div></section><div class=\"rail\" style=\"grid-template-rows:none;overflow:visible\">" + tiles + "</div></div>"))

def main():
    build_index(); build_categories(); build_drugs(); build_news(); build_busts()
    build_indexes()
    build_topics(); build_quit(); build_hotlines(); build_sentencing()
    build_directory("pharmacies", PHARMACIES, "verified pharmacy",
        "Verified Online Pharmacies — Accredited & Safe | plugreports",
        "NABP- and PharmacyChecker-verified online pharmacies. Avoid counterfeit pill mills — verify before you buy medication online.", "&#128138;")
    build_directory("rehabs", REHABS, "rehab center",
        "Verified Rehab Centers & Free Recovery Programs | plugreports",
        "Verified addiction treatment: Hazelden Betty Ford, Priory, Narcotics Anonymous, SMART Recovery — with contacts and links.", "&#10010;")
    build_drugs(es=True); build_hotlines(es=True); build_index(es=True)
    build_about(); build_suggest(); build_meta()
    manifest = {"drugs":[d["slug"] for d in DRUGS], "news":[n["slug"] for n in NEWS],
                "busts":[b["slug"] for b in BUSTS], "topics":[t["slug"] for t in TOPICS],
                "categories":[k for k in CATEGORIES]}
    w("_static.json", json.dumps(manifest))
    w("_dynamic.html", shell("_dynamic.html", "plugreports",
      "Live content", '<div class="wrap" id="dyn" style="padding:44px 20px;min-height:50vh"><p>Loading\u2026</p></div>',
      extra_head='<script src="/assets/js/render.js?v=6" defer></script>', canonical=SITE + "/"))
    print(f"Built {len(DRUGS)} drug pages, {len(CATEGORIES)} categories, {len(TOPICS)} topics, "
          f"{len(QUIT_SPECS)} quit pages, {len(NEWS)} news, {len(BUSTS)} busts into {PUB}")

if __name__ == "__main__":
    main()
