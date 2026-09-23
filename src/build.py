#!/usr/bin/env python3
"""plugreports.com static site generator.
Reads src/data_*.py and emits the full SEO-hardened site into public/."""
import datetime, html, json, os, sys
from email.utils import format_datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_drugs import DRUGS
from data_categories import CATEGORIES
from data_content import (BUSTS, NEWS, HOTLINES, PHARMACIES, REHABS,
                          SENTENCING, SETTINGS, QUIT_SPECS, TOPICS)
from data_related import RELATED_OVERRIDES
from data_sources import AGENCY_LINKS, DEEP_LINKS, QUOTES
try:
    from data_formulas import FORMULAS
except Exception:
    FORMULAS = {}
try:
    from data_mix import MIX
except Exception:
    MIX = []
try:
    from data_vs import VS, VS_CATS
except Exception:
    VS, VS_CATS = [], {}

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
TODAY = datetime.date.today().isoformat()  # actual build date — used for sitemap/lastmod fallback
LANG_LIST = ("de", "hi", "no", "pl", "fr")

def esc(s): return html.escape(str(s), quote=True)
def clip(s, n=155):
    """Trim a meta description to <=n chars at a word boundary."""
    s = " ".join(str(s or "").split())
    if len(s) <= n: return s
    return s[:n-1].rsplit(" ", 1)[0].rstrip(" ,;:.—-") + "…"
def rfc822(iso):
    try: dt = datetime.datetime.strptime(str(iso)[:10], "%Y-%m-%d").replace(hour=12, tzinfo=datetime.timezone.utc)
    except Exception: dt = datetime.datetime.now(datetime.timezone.utc)
    return format_datetime(dt)
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
        chips += rel_link(r)
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

def rel_link(entry, es=False):
    target, _, label = str(entry).partition("|")
    target = target.strip()
    if target.startswith("http"):
        lab = (label or target.replace("https://", "").replace("http://", "").strip("/").split("/")[0])
        return f'<a href="{esc(target)}" target="_blank" rel="noopener"><span class="mini" style="background:#667085">&#8599;</span><span>{esc(lab)}</span></a>'
    href = "/" + resolve_slug(target) + "/"
    if es and target in DRUG_BY_SLUG:
        from data_es import ES_DRUGS as _ESD2
        if target in _ESD2:
            href = f"/es/drugs/{target}/"
    return f'<a href="{href}">{rel_card(target)}</a>'

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
 ("/quit/", "Quitting", "quit"), ("/mix/", "Mixing", "mix"), ("/vs/", "Vs", "vs"), ("/data/", "Data", "data"), ("/hotlines/", "Hotlines", "hotline"),
 ("/sentencing/", "Sentencing", "sentencing"), ("/pharmacies/", "Pharmacies", "pharmacies"),
 ("/rehabs/", "Rehabs", "rehabs"), ("/about/", "About", "about"),
]

def _alt_set(en_url, **locales):
    """Build an hreflang set: en + any locale URLs that really exist + x-default -> EN."""
    a = {"en": en_url}
    a.update({k: v for k, v in locales.items() if v})
    a["x-default"] = en_url
    return a

def home_alts():  return _alt_set(f"{SITE}/", es=f"{SITE}/es/", **{ln: f"{SITE}/{ln}/" for ln in LANG_LIST})
def hotline_alts(): return _alt_set(f"{SITE}/hotlines/", es=f"{SITE}/es/hotlines/", **{ln: f"{SITE}/{ln}/hotlines/" for ln in LANG_LIST})

def drug_alts(slug):
    from data_es import ES_DRUGS
    from data_i18n import LANGS
    loc = {}
    if slug in ES_DRUGS: loc["es"] = f"{SITE}/es/drugs/{slug}/"
    for ln in LANG_LIST:
        if slug in LANGS[ln]["drugs"]: loc[ln] = f"{SITE}/{ln}/drugs/{slug}/"
    return _alt_set(f"{SITE}/drugs/{slug}/", **loc)

def cat_alts(k):
    from data_es import ES_DRUGS
    from data_i18n import LANGS
    loc = {}
    if any(d["slug"] in ES_DRUGS for d in DRUGS if d["category"] == k):
        loc["es"] = f"{SITE}/es/categories/{k}/"
    for ln in LANG_LIST:
        if any(DRUG_BY_SLUG[sl]["category"] == k for sl in LANGS[ln]["drugs"] if sl in DRUG_BY_SLUG):
            loc[ln] = f"{SITE}/{ln}/categories/{k}/"
    return _alt_set(f"{SITE}/categories/{k}/", **loc)

ORG_LD = {"@context":"https://schema.org","@type":"Organization","name":"plugreports",
          "url":"https://plugreports.com",
          "logo":{"@type":"ImageObject","url":"https://plugreports.com/assets/img/logo.svg"},
          "sameAs":[u for u in (SETTINGS.get("reddit"), SETTINGS.get("quora")) if u]}
PUBLISHER_LD = {"@type":"Organization","name":"plugreports",
                "logo":{"@type":"ImageObject","url":SITE + "/assets/img/logo.svg"}}

def shell(path, title, desc, body, jsonld=None, canonical=None, extra_head="", ogimage=None, lang="en", alts=None, ogtype="website", robots=None):
    canon = canonical or (SITE + ("/" if path == "index.html" else "/" + path.replace("index.html", "")))
    alts = dict(alts) if alts else {"en": canon, "x-default": canon}
    alts.setdefault("x-default", alts.get("en", canon))
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{u}">' for l, u in alts.items())
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
        crumb_mid = " / ".join(links)
        crumbs = ('<div class="wrap"><nav class="crumbs print-hide"><a href="/">Home</a>'
                  + (" / " + crumb_mid if crumb_mid else "")
                  + f' / <span>{esc(title.split("—")[0].strip())}</span></nav></div>')
    navlinks = "".join(
        f'<a href="{u}" class="{"hot" if k=="hotline" else ""}">{t}</a>' for u, t, k in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    if SETTINGS.get("gsc"): ld += f'<meta name="google-site-verification" content="{esc(SETTINGS["gsc"])}">'
    if SETTINGS.get("bing"): ld += f'<meta name="msvalidate.01" content="{esc(SETTINGS["bing"])}">'
    if SETTINGS.get("clarity"): ld += '<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,"clarity","script","' + esc(SETTINGS["clarity"]) + '")</script>'
    if SETTINGS.get("ga"): ld += '<script async src="https://www.googletagmanager.com/gtag/js?id=' + esc(SETTINGS["ga"]) + '"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","' + esc(SETTINGS["ga"]) + '")</script>' 
    if path.split("/")[0] in ("busts","news","drugs","topics","quit","mix","vs","categories","hotlines","pharmacies","rehabs","sentencing","index.html"):
        ld += '<script src="/assets/js/hydrate.js?v=15" defer></script>'
        if path == "index.html":
            ld += '<script src="/assets/js/breaking.js?v=15" defer></script>'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{alt}
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="plugreports">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ogimage or (SITE + "/assets/img/og.png")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#f59e0b">
<meta name="robots" content="{robots or 'max-image-preview:large'}">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/assets/img/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v=15">
{extra_head}{ld}
</head>
<body>
<div class="crisis"><div class="wrap"><span class="pulse"></span>
<strong data-i18n="crisis">Overdose or emergency? Call now</strong>
<span class="hide-s"><a href="/hotlines/" data-i18n="hotline">Hotlines</a> ·
<a href="tel:911">US 911</a> · <a href="tel:999">UK 999</a> · <a href="tel:112">EU 112</a> ·
<a href="tel:000">AU 000</a> · <a href="tel:112">IN 112</a> · <a href="tel:988">988 (US crisis)</a></span>
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
<div><h4>Library</h4><a href="/categories/opioids/">Opioids</a><a href="/categories/stimulants/">Stimulants</a><a href="/categories/benzodiazepines/">Benzodiazepines</a><a href="/categories/psychedelics/">Psychedelics</a><a href="/categories/empathogens/">Empathogens</a><a href="/categories/cannabinoids/">Synthetic cannabinoids</a><a href="/mix/">Mixing dangers</a><a href="/vs/">Vs comparisons</a></div>
<div><h4>Help</h4><a href="/hotlines/">Hotlines</a><a href="/rehabs/">Rehab centers</a><a href="/pharmacies/">Verified pharmacies</a><a href="/quit/">Quitting, day by day</a><a href="/sentencing/">Sentencing explained</a></div>
<div><h4>Updates</h4><a href="/news/">Drug news</a><a href="/busts/">Busts & seizures</a><a href="/topics/">Guides</a><a href="/data/">Data &amp; trackers</a><a href="/suggest/">Suggest a correction</a><a href="/rss.xml">RSS feed</a><a href="/about/">About & editorial policy</a></div>
</div>
<div class="social-row" id="socialrow" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px">
<a id="soc-reddit" href="{esc(SETTINGS.get("reddit",""))}" target="_blank" rel="noopener" class="soc-btn"><span style="color:#ff4500">&#9679;</span> Reddit</a>
<a id="soc-quora" href="{esc(SETTINGS.get("quora",""))}" target="_blank" rel="noopener" class="soc-btn"><span style="color:#b92b27">Q</span> Quora</a>
<a id="soc-email" href="mailto:{esc(SETTINGS.get("email",""))}" class="soc-btn"><span style="color:#fbbf24">&#9993;</span> <span id="soc-email-label">{esc(SETTINGS.get("email",""))}</span></a>
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
<script src="/assets/js/app.js?v=15"></script>
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
    alerts = [dict(n) for n in NEWS if n.get("tag") == "Alert"] + [dict(b) for b in BUSTS if b.get("tag") == "Alert"]
    alerts.sort(key=lambda x: x.get("date",""), reverse=True)
    alerts = alerts[:5] or NEWS[:1]
    breaking = ""
    if alerts:
        slides = []
        for i, al in enumerate(alerts):
            bimg = f'<img src="{esc(al.get("image") or "/assets/img/og.png")}" alt="" loading="lazy">' if al.get("image") else ""
            country = al.get("country", "")
            cchip = f'<span class="b-country">&#127760; {esc(country)}</span>' if country else ""
            slides.append(f"""<div class="b-slide{' on' if i==0 else ''}">{bimg}<div><div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">{cchip}<span class="b-date">{esc(al["date"])}</span></div>
<h2>{esc(al["title"])}</h2>
<p>{esc(al["summary"][:170])}&hellip;</p>
<a class="btn btn-red" href="/news/{al["slug"]}/">Read the full story &rarr;</a></div></div>""")
        dots = "".join(f'<button class="b-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="Slide {i+1}"></button>' for i in range(len(slides)))
        breaking = f"""<section class="breaking" id="breaking"><div class="wrap">
<div class="b-top"><span class="b-chip">&#9889; BREAKING</span><div class="b-dots">{dots}</div></div>
<div class="b-slides">{''.join(slides)}</div>
<button class="b-arrow b-prev" aria-label="Previous">&#8249;</button>
<button class="b-arrow b-next" aria-label="Next">&#8250;</button>
</div></section>"""
    body = f"""
{breaking}
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
<div class="st"><b>{len(CATEGORIES)}</b><span>categories</span></div>
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
            clip("Biblioteca visual de reducción de riesgos: cientos de perfiles de drogas (efectos, riesgos, signos de sobredosis, precios), noticias, incautaciones y líneas de ayuda verificadas."),
            body, lang="es", canonical=f"{SITE}/es/", alts=home_alts(),
            extra_head=f"<script>window.DRUG_INDEX={json.dumps(idx, ensure_ascii=False)};</script>"))
        return
    ld = [{"@context":"https://schema.org","@type":"WebSite","name":"plugreports","url":SITE,
           "description":"Harm-reduction library of street drug profiles, news, busts, hotlines and verified help."},
          ORG_LD]
    w("index.html", shell("index.html",
        "plugreports — Street Drug Identifier: Effects, Overdose Signs, Street Prices & Hotlines",
        clip(f"Identify street drugs fast: {len(DRUGS)} plain-English profiles with effects, overdose signs, street prices and legal status — plus drug news, busts, quitting timelines and 24/7 hotlines."),
        body, jsonld=ld, alts=home_alts(),
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

def drug_placeholder_panel(d, c):
    """CSS-only placeholder shown until a verified photo exists: molecular
    formula from FORMULAS, falling back to the drug's first letter tile."""
    f = FORMULAS.get(d["slug"], "")
    inner = (f'<span class="pf-formula">{esc(f)}</span>' if f else
             f'<span class="pf-letter" style="background:{c["grad"]}">{esc(d["name"][0])}</span>')
    return (f'<div class="pimg pimg-formula" role="img" aria-label="{esc(d["name"])} — verified photo coming soon">'
            f'{inner}<span class="pf-caption">Verified photo coming soon</span></div>')

def pimg_html(d, c, app_):
    """Real photo when one is set, otherwise the formula placeholder panel."""
    ext_img = (d.get("image") or "").strip()
    img_rel = ext_img if ext_img.startswith("http") else drug_image(d["slug"])
    if img_rel == "assets/img/drug-placeholder.svg":
        return drug_placeholder_panel(d, c), img_rel
    img_src = img_rel if img_rel.startswith("http") else "/" + img_rel  # never prefix "/" onto absolute URLs
    return (f'<img class="pimg" src="{img_src}" alt="{esc(d["name"])} — {esc(app_)}" width="510" height="383" '
            f'style="border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow);object-fit:cover;max-height:340px" loading="lazy">'), img_rel

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
        pimg, img_rel = pimg_html(d, c, app_)
        rel = related_drugs(d)
        rel_entries = d.get("related") or []
        if rel_entries:
            relhtml = "".join(rel_link(e, es=es) for e in rel_entries)
        else:
            relhtml = "".join(rel_link(r["slug"], es=es) for r in related_drugs(d))
        defextra = "" if d.get("relatedNoDefaults") else ('<a href="/topics/fentanyl-numbers/"><span class="mini" style="background:#b45309">&#128218;</span><span>Fentanyl: the numbers</span></a>'
            '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>'
            + (f'<a href="/drugs/{qslug}/"><span class="mini" style="background:#d97706">{esc(qname[0])}</span><span>About {esc(qname)}</span></a>' if qslug else '')
            + '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>'
            '<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a>')
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
<div class="ptop">
<div class="ptop-main">
<section class="phead">
<span class="glyph" style="background:{c['grad']}">{esc(d['name'][0])}</span>
<div><span class="kicker" style="background:{c['grad']};color:#fff;border:0">{esc(cat_name)}</span>
<h1 style="margin-top:10px">{esc(d['name'])}</h1>
<p class="alias">Street names: <b>{esc(", ".join(d["aliases"]))}</b></p></div></section>

<div class="callout red print-hide"><b>Overdose? Act now.</b> Call emergency services — say "unresponsive, not breathing". Give naloxone for opioid-like signs. <a href="/hotlines/">Hotlines</a></div>

<div class="panel"><h2><span class="ic" style="background:{c['color']};color:#fff">&#9889;</span>What it does</h2>
<ul class="ticks">{''.join(f"<li>{esc(e)}</li>" for e in fx)}</ul>
<h2 style="margin-top:22px"><span class="ic" style="background:#dc2626;color:#fff">&#9888;</span>Key risks</h2>
<ul class="ticks red">{''.join(f"<li>{esc(r)}</li>" for r in rk)}</ul>
<h2 style="margin-top:22px"><span class="ic" style="background:#111827;color:#fff">&#10010;</span>Overdose signs</h2>
<ul class="ticks red">{''.join(f"<li>{esc(o_)}</li>" for o_ in od)}</ul></div>
</div>
<aside class="ptop-rail">
{pimg}
<div class="panel"><h2><span class="ic" style="background:{c['color']};color:#fff">&#128203;</span>Quick facts</h2>{rows}
<div style="margin-top:14px"><span class="chip green">Sources: {esc(", ".join(d["sources"]))}</span></div></div>
</aside>
</div>

<div class="panel"><h2>{cmp_head}</h2>
<table class="tbl"><thead><tr><th>Substance</th><th>Class</th><th>Top risks</th><th>Street price</th></tr></thead>
<tbody>{cat_rows}</tbody></table>
<div class="notice-strip">Street prices are regional estimates. Potency and cuts vary constantly.</div></div>

{brands_html}
{faq_panel}
{sources_html}

<div class="related print-hide"><h2>You may also want to know about</h2>
<div class="rel-grid">{relhtml}{defextra}</div></div>
</div>"""
        if es:
            title = f"{d['name']}: efectos, riesgos, signos de sobredosis y precio | plugreports"
            desc = clip(f"{d['name']} ({', '.join(d['aliases'][:3])}) — {cat_name}. Efectos: {'; '.join(fx[:2])}. Riesgos: {'; '.join(rk[:2])}. Actualizado {d['lastUpdated']}.")
            out = f"es/drugs/{d['slug']}/index.html"
            w(out, shell(out, title, desc, body, lang="es", canonical=f"{SITE}/es/drugs/{d['slug']}/", alts=drug_alts(d["slug"])))
        else:
            title = d.get("seoTitle") or f"{d['name']}: Effects, Risks & Overdose Signs | plugreports"
            desc = d.get("seoDesc") or clip(f"{d['name']} ({', '.join(d['aliases'][:3])}) — {cat_name}. Effects: {'; '.join(d['effects'][:2])}. Risks: {'; '.join(d['risks'][:2])}. Overdose signs, street price & legal status.")
            ld = [{"@context":"https://schema.org","@type":"MedicalWebPage",
                   "name":title,"url":f"{SITE}/drugs/{d['slug']}/","lastReviewed":d["lastUpdated"],
                   "reviewedBy":{"@type":"Organization","name":"plugreports editorial","url":SITE + "/about/"},
                   "about":{"@type":"Drug","name":d["name"],"alternateName":d["aliases"],
                            "drugClass":cat_name,"legalStatus":d["legalStatus"]},
                   "audience":{"@type":"Audience","audienceType":"People seeking harm-reduction information"},
                   "medicalAudience":{"@type":"MedicalAudience","audienceType":"Patient"}},
                  breadcrumb_ld([("Home","/"),(cat_name,f"/categories/{d['category']}/"),(d["name"],f"/drugs/{d['slug']}/")]),
                  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}]
            og = img_rel if img_rel.startswith("http") else (f"{SITE}/{img_rel}" if "drugs/" in img_rel else None)
            w(f"drugs/{d['slug']}/index.html", shell(f"drugs/{d['slug']}/index.html", title, desc, body, jsonld=ld, ogimage=og, alts=drug_alts(d["slug"])))


def build_categories():
    from data_es import ES_DRUGS
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
        title = f"{c['name']} — Effects, Risks & Street Prices | plugreports"
        desc = clip(f"{c['tagline']} {len(items)} harm-reduction profiles: effects, overdose signs, street prices, legal status.")
        itemlist = {"@context":"https://schema.org","@type":"ItemList","name":f"{c['name']} — drug profiles",
                    "numberOfItems":len(items),
                    "itemListElement":[{"@type":"ListItem","position":i+1,"name":x["name"],"url":f"{SITE}/drugs/{x['slug']}/"} for i,x in enumerate(items)]}
        w(f"categories/{k}/index.html", shell(f"categories/{k}/index.html", title, desc, body,
          jsonld=[{"@context":"https://schema.org","@type":"CollectionPage","name":title}, itemlist,
                  breadcrumb_ld([("Home","/"),(c["name"],f"/categories/{k}/")])], alts=cat_alts(k)))

# ---------------------------------------------------- news / busts/topics ----
def build_news():
    idx_cards = "".join(f'''<a class="card" href="/news/{n['slug']}/">{f'<div class="thumb"><img src="{esc(n["image"])}" alt="" loading="lazy"></div>' if n.get("image") else ''}<div class="meta">
<span class="badge-live">{esc(n["tag"]).upper()}</span><span class="chip">{esc(n["date"])}</span></div>
<h3>{esc(n['title'])}</h3><p>{esc(n['summary'])}</p><div class="foot">Read &rarr;</div></a>''' for n in NEWS)
    w("news/index.html", shell("news/index.html", "Drug News & Supply Alerts | plugreports",
      clip("Drug news, adulterant alerts and supply trends: nitazenes, xylazine, high-dose pills, counterfeit pharmaceuticals — with sources."),
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker">Newsroom</span><h1>Drug news & alerts</h1><p>Sourced from NIDA, DEA, EMCDDA, ONS and drug-checking services. Subscribe via <a href="/rss.xml">RSS</a>.</p></div></div><div class="cards">{idx_cards}</div></div>'))
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
              "image":n.get("image") or f"{SITE}/assets/img/og.png",
              "datePublished":n["date"],"dateModified":n["date"],"author":{"@type":"Organization","name":"plugreports"},
              "publisher":PUBLISHER_LD,"mainEntityOfPage":f"{SITE}/news/{n['slug']}/"}
        w(f"news/{n['slug']}/index.html", shell(f"news/{n['slug']}/index.html", f"{n['title']} | plugreports", clip(n["summary"]), full, jsonld=ld, ogtype="article"))

def build_busts():
    cards = "".join(f'''<a class="card" href="/busts/{b['slug']}/"><div class="meta">
<span class="chip {"red" if not b.get("confirmed") else "amber"}">{"&#9888; PENDING VERIFICATION" if not b.get("confirmed") else "&#10004; CONFIRMED"}</span>
<span class="chip">{esc(b["date"])}</span></div><h3>{esc(b['title'])}</h3><p>{esc(b['summary'])}</p>
<div class="foot">{esc(b["location"])} · {esc(b["agency"])} &rarr;</div></a>''' for b in BUSTS)
    w("busts/index.html", shell("busts/index.html", "Drug Busts & Seizures Tracker | plugreports",
      clip("Recent drug busts and seizures worldwide: location, agency, substances, quantities and sentencing exposure. Pending items are marked until editor-verified."),
      f'''<div class="wrap"><section class="sec-head" style="padding-top:30px"><div>
<span class="kicker">Enforcement tracker</span><h1>Busts & seizures</h1>
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
        ld = {"@context":"https://schema.org","@type":"NewsArticle","headline":b["title"],
              "image":b.get("image") or f"{SITE}/assets/img/og.png",
              "datePublished":b["date"],"dateModified":b["date"],"author":{"@type":"Organization","name":"plugreports"},
              "publisher":PUBLISHER_LD,"mainEntityOfPage":f"{SITE}/busts/{b['slug']}/"}
        robots = "noindex,follow" if b.get("noindex") else None
        w(f"busts/{b['slug']}/index.html", shell(f"busts/{b['slug']}/index.html", f"{b['title']} | plugreports", clip(b["summary"]), body, jsonld=ld, ogtype="article", robots=robots))


import html as _html
import re
def md_inline(x):
    x = _html.escape(str(x), quote=False)
    x = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", x)
    x = re.sub(r"\*([^*\n]+)\*", r"<i>\1</i>", x)
    return x

def md_render(src):
    lines = str(src or "").split("\n"); out = []; i = 0
    CAL = {"warning":"amber","danger":"red","red":"red","tip":"green","success":"green","note":"amber"}
    while i < len(lines):
        L = lines[i]
        if L.startswith("### "): out.append(f"<h3>{md_inline(L[4:])}</h3>"); i += 1
        elif L.startswith("## "): out.append(f"<h2>{md_inline(L[3:])}</h2>"); i += 1
        elif L.startswith("#### "): out.append(f"<h3>{md_inline(L[5:])}</h3>"); i += 1
        elif re.match(r"^\s*[-*]\s+", L):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(f"<li>{md_inline(re.sub(r'^\\s*[-*]\\s+','',lines[i]))}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
        elif re.match(r"^\s*\d+\.\s+", L):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(f"<li>{md_inline(re.sub(r'^\\s*\\d+\\.\\s+','',lines[i]))}</li>"); i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
        elif L.strip().startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            if len(tbl) >= 2:
                head = tbl[0]; body = tbl[2:] if all(set(r) <= set("-: ") for r in tbl[1]) else tbl[1:]
                h = "".join(f"<th>{md_inline(c)}</th>" for c in head)
                b = "".join("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>" for r in body)
                out.append(f'<div class="figure"><table class="tbl"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
        elif L.startswith(":::"):
            m = re.match(r"^:::\s*(\w*)\s*(.*)$", L)
            cls = CAL.get((m.group(1) or "note").lower(), "amber")
            body = []; i += 1
            while i < len(lines) and not lines[i].startswith(":::"):
                if lines[i].strip(): body.append(f"<p>{md_inline(lines[i])}</p>")
                i += 1
            i += 1
            out.append(f'<div class="callout {cls}"><b>{md_inline(m.group(2) or "Note")}</b>' + "".join(body) + "</div>")
        elif L.strip() == "":
            i += 1
        else:
            buf = []
            while i < len(lines) and lines[i].strip() != "" and not re.match(r"^(#{1,3}\s|[-*]\s|\d+\.\s|>|:::|\|)", lines[i]):
                buf.append(lines[i]); i += 1
            out.append(f"<p>{md_inline(' '.join(buf))}</p>")
    return "\n".join(out)

def build_topics():
    cards = "".join(f'''<a class="card" href="/topics/{t['slug']}/"><div class="meta">
<span class="chip red">GUIDE</span><span class="chip">{esc(t["read"])}</span><span class="chip">{esc(t["date"])}</span></div>
<h3>{esc(t['title'])}</h3><p>{esc(t['desc'])}</p><div class="foot">Read guide &rarr;</div></a>''' for t in TOPICS)
    w("topics/index.html", shell("topics/index.html", "Drug Guides & Explainers | plugreports",
      clip("Visual explainers: xylazine, fentanyl numbers, pressed pills, nitazenes, krokodil facts, sentencing, talking to your kids, quitting day by day."),
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker amber">Guides</span><h1>Explainers & deep-dives</h1><p>Written for fast reading: tables, timelines and callouts instead of walls of text.</p></div></div><div class="cards">{cards}</div></div>'))
    for t in TOPICS:
        if t.get("markdown"):
            inner = md_render(t["markdown"])
            mentioned = t.get("drugsInvolved") or []
        else:
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
              "image":t.get("image") or f"{SITE}/assets/img/og.png",
              "datePublished":t["date"],"dateModified":t["date"],
              "author":{"@type":"Organization","name":"plugreports"},
              "publisher":PUBLISHER_LD,"mainEntityOfPage":f"{SITE}/topics/{t['slug']}/"}
        w(f"topics/{t['slug']}/index.html", shell(f"topics/{t['slug']}/index.html", f"{t['title']} | plugreports", clip(t["desc"]), body, jsonld=ld, ogtype="article"))

def build_quit():
    cards = "".join(f'''<a class="card" href="/quit/{k}/"><div class="meta">
<span class="chip green">DAY-BY-DAY</span><span class="chip">{esc(v["cat"])}</span></div>
<h3>Quitting {esc(v['name'])}</h3><p>{esc(v['danger'][:120])}…</p><div class="foot">Full timeline &rarr;</div></a>''' for k, v in QUIT_SPECS.items())
    w("quit/index.html", shell("quit/index.html", "What Happens When You Quit Drugs — Day-by-Day Timelines | plugreports",
      clip("Honest withdrawal timelines: heroin, fentanyl, cocaine, meth, MDMA, Xanax, ketamine, GHB. What's normal, what hurts, when it ends, and when detox must be medical."),
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker green">Recovery</span><h1>Quitting — day by day</h1><p>Start with the <a href="/topics/what-actually-happens-when-you-quit/">master explainer</a>, then pick your substance.</p></div></div><div class="cards">{cards}</div></div>'))
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
        title = f"Quitting {v['name']}: Day-by-Day Withdrawal Timeline | plugreports"
        desc = clip(f"Quitting {v['name']} ({v['cat']}): day-by-day withdrawal timeline, peak symptoms, how long it lasts, and when medical detox is essential.")
        ld = {"@context":"https://schema.org","@type":"MedicalWebPage",
              "name":title,"url":f"{SITE}/quit/{k}/","lastReviewed":TODAY,
              "reviewedBy":{"@type":"Organization","name":"plugreports editorial","url":SITE + "/about/"},
              "about":{"@type":"Drug","name":v["name"]},"audience":{"@type":"Audience","audienceType":"People quitting drugs or supporting someone who is"}}
        w(f"quit/{k}/index.html", shell(f"quit/{k}/index.html", title, desc, body, jsonld=ld))

# ------------------------------------------------- mixing (combinations) ----
MIX_LEVELS = {  # level -> (badge label, chip class, callout class)
    "deadly":    ("DEADLY COMBINATION", "red", "red"),
    "dangerous": ("DANGEROUS COMBINATION", "amber", "amber"),
    "caution":   ("USE WITH CAUTION", "", "gray"),
}

def build_mix():
    if not MIX: return  # stub data — no mix pages until content lands
    def lvl(m): return MIX_LEVELS.get(m.get("level"), MIX_LEVELS["caution"])
    def card(m):
        label, chipcls, _ = lvl(m)
        return (f'<a class="card" href="/mix/{m["slug"]}/"><div class="meta">'
                f'<span class="chip {chipcls}">{label}</span></div>'
                f'<h3>{esc(m["a"])} + {esc(m["b"])}</h3><p>{esc(clip(m["summary"], 140))}</p>'
                f'<div class="foot">Why it&rsquo;s dangerous &rarr;</div></a>')
    TIER_TXT = {
        "deadly":    ("Deadly combinations", "These pairs stop breathing and kill fast — if you're mixing or thinking about it, read this tier first."),
        "dangerous": ("Dangerous combinations", "Serious risk of overdose, seizures, heart problems or blackouts."),
        "caution":   ("Use with caution", "Lower immediate risk, but still unpredictable — dose, timing and health all change the outcome."),
    }
    secs = []
    for tier in ("deadly", "dangerous", "caution"):
        items = [m for m in MIX if m.get("level") == tier]
        if not items: continue
        h, sub = TIER_TXT[tier]
        secs.append(f'<section style="margin-top:32px"><h2 style="font-size:22px">{h}</h2>'
                    f'<p style="color:var(--muted);font-size:14.5px;margin:6px 0 14px">{sub}</p>'
                    f'<div class="cards" data-tier="{tier}">{"".join(card(m) for m in items)}</div></section>')
    hub = ('<div class="wrap"><section class="sec-head" style="padding-top:30px"><div>'
           '<span class="kicker">Mixing dangers</span><h1>Mixing drugs &mdash; why combinations kill more than any single drug</h1>'
           f'<p>Here is the number most people never hear: <b>most fatal overdoses involve more than one substance.</b> Mixing is not additive &mdash; it is multiplicative. '
           'Two depressants together can stop your breathing at doses either one would survive alone. A stimulant masks a downer&rsquo;s warning signs until it is too late. '
           'And medicines mixed without a doctor&rsquo;s oversight &mdash; a friend&rsquo;s prescription, a pill from a stranger, a drink on top of a sleep aid &mdash; are the single most common path into an overdose. '
           f'These {len(MIX)} plain-language guides explain exactly why each combination is dangerous, what the mix does to your body, the warning signs of trouble, and what to do in the first minutes.</p></div></section>'
           '<div class="callout red"><b>If you&rsquo;re mixing or thinking about it, read the deadly tier first.</b>'
           'Those combinations kill quickly — often before help can arrive. If someone is unresponsive or breathing slowly, '
           'call emergency services now, then give naloxone if opioids might be involved. <a href="/hotlines/">Hotlines</a></div>'
           + "".join(secs) + '</div>')
    itemlist = {"@context":"https://schema.org","@type":"ItemList","name":"Mixing dangers",
                "numberOfItems":len(MIX),
                "itemListElement":[{"@type":"ListItem","position":i+1,"name":m["title"],"url":f"{SITE}/mix/{m['slug']}/"} for i,m in enumerate(MIX)]}
    w("mix/index.html", shell("mix/index.html",
        "Mixing Drugs — Why Combinations Kill & the Deadliest Mixes | plugreports",
        clip(f"Most fatal overdoses involve 2+ substances — mixing is multiplicative, not additive. {len(MIX)} plain-language guides: why each combination is dangerous, warning signs, what to do."),
        hub, jsonld=[{"@context":"https://schema.org","@type":"CollectionPage","name":"Mixing dangers"}, itemlist,
                     breadcrumb_ld([("Home","/"),("Mixing","/mix/")])]))
    for m in MIX:
        label, chipcls, calcls = lvl(m)
        cross = ""
        xlinks = [DRUG_BY_SLUG[s] for s in (m.get("aSlug"), m.get("bSlug")) if s and s in DRUG_BY_SLUG]
        if xlinks:
            chips = "".join(f'<a href="/drugs/{x["slug"]}/">{rel_card(x["slug"])}</a>' for x in xlinks)
            cross = f'<div class="related print-hide"><h2>Full substance profiles</h2><div class="rel-grid">{chips}</div></div>'
        same = [x for x in MIX if x is not m and x.get("level") == m.get("level")][:4]
        relchips = ('<a href="/mix/"><span class="mini" style="background:#dc2626">&#9888;</span><span>All mixing dangers</span></a>'
                    + "".join(f'<a href="/mix/{x["slug"]}/"><span class="mini" style="background:#667085">&#9851;</span><span>{esc(x["a"])} + {esc(x["b"])}</span></a>' for x in same))
        faqs = [
            (f"Can you mix {m['a']} and {m['b']}?", m["summary"]),
            (f"What are the warning signs of mixing {m['a']} and {m['b']}?",
             "; ".join(m.get("signs", [])[:3]) or m["summary"]),
            (f"What should you do if someone has mixed {m['a']} and {m['b']}?",
             " ".join(m.get("whatToDo", [])[:2]) or "Call emergency services immediately."),
        ]
        body = f"""<div class="wrap"><article class="article" style="padding-top:26px">
<span class="chip {chipcls} lvl-badge" data-mix="badge" style="font-size:12px;padding:6px 14px">{label}</span>
<h1 style="margin-top:12px">{esc(m['title'])}</h1>
<div class="byline"><span data-mix="updated">Updated {esc(m.get('lastUpdated', TODAY))}</span><span data-mix="sources">Sources: {esc(m.get('sources', ''))}</span></div>
<div class="callout {calcls}"><b>{esc(m['a'])} + {esc(m['b'])}: the short answer</b><span data-mix="summary">{esc(m['summary'])}</span></div>
<h2>Why it&rsquo;s dangerous</h2>
<p data-mix="mechanism">{esc(m['mechanism'])}</p>
<h2>What happens</h2>
<ul class="ticks" data-mix="effects">{''.join(f"<li>{esc(e)}</li>" for e in m.get("effects", []))}</ul>
<h2>Warning signs</h2>
<ul class="ticks red" data-mix="signs">{''.join(f"<li>{esc(s)}</li>" for s in m.get("signs", []))}</ul>
<h2>What to do</h2>
<ul class="checklist" data-mix="whatToDo">{''.join(f"<li>{esc(x)}</li>" for x in m.get("whatToDo", []))}</ul>
{cross}
<div class="related print-hide"><h2>More mixing dangers</h2><div class="rel-grid">{relchips}</div></div>
</article></div>"""
        title = m.get("seoTitle") or clip(f"{m['title']} — dangers, signs & what to do | plugreports", 60)
        desc = m.get("seoDesc") or clip(m["summary"])
        ld = [{"@context":"https://schema.org","@type":"MedicalWebPage",
               "name":title,"url":f"{SITE}/mix/{m['slug']}/","lastReviewed":m.get("lastUpdated", TODAY),
               "reviewedBy":{"@type":"Organization","name":"plugreports editorial","url":SITE + "/about/"},
               "about":{"@type":"Drug","name":f"{m['a']} + {m['b']}"},
               "audience":{"@type":"Audience","audienceType":"People seeking harm-reduction information"}},
              {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
              breadcrumb_ld([("Home","/"),("Mixing","/mix/"),(m["title"],f"/mix/{m['slug']}/")])]
        w(f"mix/{m['slug']}/index.html", shell(f"mix/{m['slug']}/index.html", title, desc, body, jsonld=ld))

# ------------------------------------------------------------- vs pages ----
def vs_media(d):
    """Live drug image when the profile has one, else a formula/letter tile."""
    c = CATEGORIES[d["category"]]
    ext_img = (d.get("image") or "").strip()
    img_rel = ext_img if ext_img.startswith("http") else drug_image(d["slug"])
    if img_rel != "assets/img/drug-placeholder.svg":
        img_src = img_rel if img_rel.startswith("http") else "/" + img_rel
        return f'<img class="vs-img" src="{img_src}" alt="{esc(d["name"])}" loading="lazy">'
    f = FORMULAS.get(d["slug"], "")
    inner = (f'<span class="pf-formula">{esc(f)}</span>' if f else
             f'<span class="pf-letter" style="background:{c["grad"]}">{esc(d["name"][0])}</span>')
    return f'<div class="vs-img vs-ph">{inner}</div>'

def vs_rel_chip(r):
    """Related chip that also supports external links: https://url|Label."""
    if r.startswith("http"):
        url, _, label = r.partition("|")
        label = (label or url.split("//")[-1].split("/")[0]).strip()
        return (f'<a href="{esc(url)}" target="_blank" rel="noopener">'
                f'<span class="mini" style="background:#0f766e">&#8599;</span><span>{esc(label)}</span></a>')
    return f'<a href="/{resolve_slug(r)}/">{rel_card(r)}</a>'

def build_vs():
    if not VS: return
    def pair_card(v):
        a, b = DRUG_BY_SLUG[v["aSlug"]], DRUG_BY_SLUG[v["bSlug"]]
        ca, cb = CATEGORIES[a["category"]], CATEGORIES[b["category"]]
        return (f'<a class="card vs-card" href="/vs/{v["slug"]}/">'
                f'<div class="vs-duo"><span class="vs-dot" style="background:{ca["color"]}">{esc(a["name"][0])}</span>'
                f'<span class="vs-x">vs</span>'
                f'<span class="vs-dot" style="background:{cb["color"]}">{esc(b["name"][0])}</span></div>'
                f'<h3>{esc(v["title"])}</h3><p>{esc(clip(v["intro"], 120))}</p>'
                f'<div class="foot">See the comparison &rarr;</div></a>')
    CAT_SUB = {"benzos": "Anti-anxiety sedatives, side by side.",
               "opioids": "Painkillers and opioid treatments, head to head.",
               "adhd": "Focus medications, compared fairly.",
               "stimulants": "Cocaine, meth, crack and friends.",
               "cannabis": "Weed, delta-8, HHC and the hemp aisle.",
               "psychedelics": "The classic mind-openers, compared.",
               "empathogens": "MDMA and its chemical family.",
               "dissociatives": "Ketamine, PCP and the hole states.",
               "downers": "GHB, sleep aids and nerve-pill cousins.",
               "grey": "Grey-market and lifestyle compounds."}
    CAT_NAME = dict(VS_CATS)
    secs = []
    for key, name in VS_CATS:
        items = [v for v in VS if v["cat"] == key]
        if not items: continue
        secs.append(f'<section class="vs-group" id="{key}"><h2>{esc(name)}</h2>'
                    f'<p class="vs-group-sub">{esc(CAT_SUB.get(key, ""))} {len(items)} comparisons.</p>'
                    f'<div class="cards">{"".join(pair_card(v) for v in items)}</div></section>')
    pills = "".join(f'<a href="#{k}">{esc(n)}</a>' for k, n in VS_CATS
                    if any(v["cat"] == k for v in VS))
    hub_faqs = [
        ("Why should I compare two drugs before taking anything?",
         "Because the risks hide in the differences. A bar pressed to look like Xanax may actually be bromazolam or contain fentanyl. Two painkillers with similar names can differ tenfold in strength. Two party drugs that feel fine alone can stop your breathing together. Comparing first turns a guess into an informed choice."),
        ("Is one drug in a comparison ever 'safe'?",
         "No — and any page that says otherwise is selling something. Every comparison here is harm reduction: both substances carry real risks, and the honest answer is which risks are bigger, how they differ, and how to reduce them. The safest choice is always not to use; the second-safest is to know exactly what you're dealing with."),
        ("Where does this information come from?",
         "Each comparison is compiled from public health sources — NIDA, CDC, FDA, DEA, WHO, EMCDDA and peer-reviewed studies — and every page lists its sources and last-updated date. Nothing here is medical advice; in an emergency, call your local emergency number first."),
    ]
    faq_html = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in hub_faqs)
    hub = ('<div class="wrap"><section class="sec-head" style="padding-top:30px"><div>'
           '<span class="kicker">Head-to-head</span><h1>Compare drugs before you take them &mdash; it can save your life</h1>'
           f'<p>A pill sold as Xanax may be bromazolam. A painkiller with a familiar name may be ten times stronger than the one beside it. '
           'And mixing medicines that were never prescribed together &mdash; an opioid with a benzo, a stimulant with a depressant &mdash; is how most fatal overdoses actually happen. '
           f'These {len(VS)} honest comparisons answer the questions people really search: <b>which is stronger, which is more addictive, what it costs, and which one will hurt you more</b> &mdash; in plain English, with sources.</p></div></section>'
           '<div class="callout red"><b>About to mix something, or holding a pill you can&rsquo;t verify?</b>'
           ' Start with <a href="/mix/">mixing dangers</a> and <a href="/topics/spot-pressed-pills/">how to spot pressed pills</a> &mdash; and keep <a href="/hotlines/">a hotline</a> handy. '
           'Counterfeit pills have killed people who thought they knew what they were taking.</div>'
           f'<div class="pill-nav">{pills}</div>' + "".join(secs) +
           f'<section class="vs-group"><h2>Frequently asked questions</h2><div class="panel" style="margin-top:10px">{faq_html}</div></section></div>')
    itemlist = {"@context":"https://schema.org","@type":"ItemList","name":"Drug comparisons",
                "numberOfItems":len(VS),
                "itemListElement":[{"@type":"ListItem","position":i+1,"name":v["title"],"url":f"{SITE}/vs/{v['slug']}/"} for i,v in enumerate(VS)]}
    w("vs/index.html", shell("vs/index.html",
        f"Vs — {len(VS)} Drug Comparisons: Which Is Stronger, Safer, More Addictive? | plugreports",
        clip(f"Why comparing drugs matters: pressed pills, hidden strength differences, and deadly mixes. {len(VS)} honest head-to-head guides in plain English — which is stronger, which is more addictive, which is more dangerous."),
        hub, jsonld=[{"@context":"https://schema.org","@type":"CollectionPage","name":"Drug comparisons"},
                     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                         {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in hub_faqs]},
                     itemlist,
                     breadcrumb_ld([("Home","/"),("Vs","/vs/")])]))
    for v in VS:
        a = DRUG_BY_SLUG[v["aSlug"]]; b = DRUG_BY_SLUG[v["bSlug"]]
        ca = CATEGORIES[a["category"]]; cb = CATEGORIES[b["category"]]
        hero = (f'<div class="vs-hero"><div class="vs-side" style="--edge:{ca["color"]}">'
                f'{vs_media(a)}<div class="vs-name">{esc(a["name"])}</div>'
                f'<div class="vs-tag">{esc(a["category"].replace("-"," ").title())}</div></div>'
                f'<div class="vs-badge">VS</div>'
                f'<div class="vs-side right" style="--edge:{cb["color"]}">'
                f'{vs_media(b)}<div class="vs-name">{esc(b["name"])}</div>'
                f'<div class="vs-tag">{esc(b["category"].replace("-"," ").title())}</div></div></div>')
        trows = "".join(f'<tr><th scope="row">{esc(label)}</th><td>{esc(x)}</td><td>{esc(y)}</td></tr>'
                        for label, x, y in v["rows"])
        table = (f'<div class="figure"><table class="tbl vs-table"><thead><tr>'
                 f'<th class="vs-corner"></th><th>{esc(v["a"])}</th><th>{esc(v["b"])}</th></tr></thead>'
                 f'<tbody>{trows}</tbody></table></div>')
        faq_html = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(x)}</p></details>' for q, x in v["faqs"])
        relchips = ('<a href="/vs/"><span class="mini" style="background:#0f766e">&#8646;</span><span>All comparisons</span></a>'
                    + "".join(vs_rel_chip(r) for r in v["related"]))
        same = [x for x in VS if x is not v and x["cat"] == v["cat"]][:4]
        more = "".join(f'<a href="/vs/{x["slug"]}/"><span class="mini" style="background:#667085">&#8646;</span>'
                       f'<span>{esc(x["title"])}</span></a>' for x in same)
        body = f"""<div class="wrap"><article class="article" style="padding-top:26px">
<span class="kicker">Head-to-head</span>
<h1 style="margin-top:10px">{esc(v['title'])}</h1>
<div class="byline"><span data-vs="updated">Updated {esc(v.get('lastUpdated', TODAY))}</span><span data-vs="sources">Sources: {esc(", ".join(v.get('sources', [])))}</span></div>
{hero}
<p class="lede" data-vs="intro">{esc(v['intro'])}</p>
<h2>{esc(v['title'])} &mdash; side by side</h2>
{table}
<h2>The verdict</h2>
<div class="callout amber" data-vs="verdict">{esc(v['verdict'])}</div>
<div class="panel" style="margin-top:20px"><h2><span class="ic" style="background:#0f766e;color:#fff">?</span>Frequently asked questions</h2>{faq_html}</div>
<div class="related print-hide"><h2>You may also want to know</h2><div class="rel-grid" data-vs="related">{relchips}</div></div>
{('<div class="related print-hide"><h2>More ' + esc(CAT_NAME.get(v["cat"], "comparisons").lower()) + '</h2><div class="rel-grid">' + more + '</div></div>') if more else ''}
</article></div>"""
        title = clip(f"{v['title']} — honest comparison in plain English | plugreports", 60)
        desc = clip(f"{v['title']}: what each one is, how it feels, addiction risk, price, and which is more dangerous. Simple-English guide with FAQ.", 158)
        ld = [{"@context":"https://schema.org","@type":"MedicalWebPage",
               "name":v["title"],"url":f"{SITE}/vs/{v['slug']}/","lastReviewed":v.get("lastUpdated", TODAY),
               "reviewedBy":{"@type":"Organization","name":"plugreports editorial","url":SITE + "/about/"},
               "about":[{"@type":"Drug","name":a["name"]},{"@type":"Drug","name":b["name"]}],
               "audience":{"@type":"Audience","audienceType":"People comparing two substances"}},
              {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":x}} for q, x in v["faqs"]]},
              breadcrumb_ld([("Home","/"),("Vs","/vs/"),(v["title"],f"/vs/{v['slug']}/")])]
        w(f"vs/{v['slug']}/index.html", shell(f"vs/{v['slug']}/index.html", title, desc, body, jsonld=ld))

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
          body, lang="es", canonical=f"{SITE}/es/hotlines/", alts=hotline_alts()))
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
      clip("Verified 24/7 hotlines: emergency numbers, overdose help, suicide crisis (988/112), treatment referral (SAMHSA, FRANK, Lifeline) for all five regions."),
      body, jsonld=faq, alts=hotline_alts()))


def build_sentencing():
    qslug = None; qname = ""
    secs = []
    for s in SENTENCING:
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in s["table"][1:])
        head = "".join(f"<th>{esc(c)}</th>" for c in s["table"][0])
        secs.append(f'''<div class="legal-doc" style="margin-bottom:22px"><span class="seal">INFO<br>ONLY</span>
<h2 style="margin-top:0">{esc(s["region"])}</h2><p style="color:#667085">{esc(s["summary"])}</p>
<table class="tbl"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>''')
    sent_rel, _seen = [], set()
    for s in SENTENCING:
        for r in (s.get("related") or []):
            if r not in _seen:
                _seen.add(r); sent_rel.append(r)
    sent_rel_html = ('<div class="related print-hide"><h2>You may also want to know about</h2><div class="rel-grid" data-sent-rel>'
                     + "".join(rel_link(r) for r in sent_rel) + '</div></div>') if sent_rel else '<div class="rel-grid" data-sent-rel></div>'
    body = f"""<div class="wrap"><div style="padding-top:26px">
<span class="kicker">Legal information</span><h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Drug sentencing, explained</h1>
<p class="lede" style="color:#667085;max-width:68ch">What possession and trafficking actually cost across the USA, Canada, the UK/EU, Australia and Africa — and why <b>calling 911 during an overdose is always worth it</b> (Good Samaritan protections).</p>
<div class="callout amber" style="margin:18px 0 26px"><b>Not legal advice</b>Sentencing law changes constantly and facts decide cases. Consult a licensed lawyer in your jurisdiction. This page exists so no one learns the system the hard way.</div>
{''.join(secs)}
<div class="related print-hide"><h2>Related reading</h2><div class="rel-grid">
<a href="/topics/sentencing-explained/"><span class="mini" style="background:#b45309">&#128218;</span><span>Full sentencing guide</span></a>
<a href="/topics/talk-to-your-kid/"><span class="mini" style="background:#16a34a">&#128218;</span><span>Talking to your kids</span></a>
<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a></div></div>
{sent_rel_html}
</div></div>"""
    w("sentencing/index.html", shell("sentencing/index.html", "Drug Possession Sentences by Country — US, Canada, UK/EU, Australia, Africa | plugreports",
      clip("Drug sentencing tables: possession and trafficking penalties per region, Good Samaritan laws, mandatory minimums, and what to do if arrested."), body))

def build_directory(name, items, singular, title, desc, thumb):
    qslug = None; qname = ""
    cards = "".join(f'''<a class="card" href="/{name}/{it['slug']}/">
{f'<div class="thumb" style="height:110px;border-radius:12px;overflow:hidden;margin-bottom:10px"><img src="{esc(it["image"])}" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover"></div>' if it.get("image") else f'<div class="thumb" style="height:110px;background:linear-gradient(135deg,#fef3c7,#fee2e2);display:grid;place-items:center;font-size:34px">{thumb}</div>'}
<h3>{esc(it['name'])}</h3><p>{esc(it['desc'][:130])}…</p>
<div class="foot">{esc(it['region'])} &rarr;</div></a>''' for it in items)
    itemlist = {"@context":"https://schema.org","@type":"ItemList","name":title.split("|")[0].strip(),
                "numberOfItems":len(items),
                "itemListElement":[{"@type":"ListItem","position":i+1,"name":it["name"],"url":f"{SITE}/{name}/{it['slug']}/"} for i,it in enumerate(items)]}
    w(f"{name}/index.html", shell(f"{name}/index.html", title, clip(desc),
      f'<div class="wrap"><section class="sec-head" style="padding-top:30px"><div><span class="kicker green">Verified directory</span><h1>{esc(title.split("|")[0].strip())}</h1><p>Every listing is checked against official accreditation/registries before publishing. <a href="/suggest/">Recommend a facility</a>.</p></div></div><div class="dir-grid">{cards}</div></div>', jsonld=itemlist))
    for it in items:
        body = f"""<div class="wrap"><div style="max-width:760px;padding:26px 0">
<span class="kicker green">{'&#10004; VERIFIED' if it.get('verified') else 'LISTING'}</span>
<h1 style="font-size:clamp(26px,4vw,38px);margin-top:10px">{esc(it['name'])}</h1>
<div class="tagrow"><span class="chip amber">{esc(it['region'])}</span></div>
{(f'<img class="detail-img" src="{esc(it["image"])}" alt="" loading="lazy">' if it.get("image") else f'<div class="thumb" style="height:180px;background:linear-gradient(135deg,#fef3c7,#fee2e2);display:grid;place-items:center;font-size:44px;border-radius:16px;margin:16px 0">{thumb}</div>')}
<p style="font-size:16.5px">{esc(it['desc'])}</p>
<div class="fact" style="margin-top:18px"><b>Website</b><span><a href="{esc(it['website'])}" rel="noopener">{esc(it['website'])}</a></span></div>
{f'<div class="fact"><b>Contact</b><span>{esc(it["phone"])}</span></div>' if it.get('phone') else ''}
<div class="callout green" style="margin-top:18px"><b>In crisis right now?</b>Skip the directory — call your emergency number or a <a href="/hotlines/">hotline</a> first.</div>
<div class="related print-hide"><h2>You may also want to know about</h2><div class="rel-grid">
{f'<a href="/drugs/{qslug}/"><span class="mini" style="background:#d97706">{esc(qname[0])}</span><span>About {esc(qname)}</span></a>' if qslug else ''}
{''.join(rel_link(r) for r in (it.get("related") or []))}
<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>
<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>
<a href="/rehabs/"><span class="mini" style="background:#16a34a">&#10010;</span><span>All rehab centers</span></a>
<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a></div></div>
</div></div>"""
        biz = {"@context":"https://schema.org","@type":"MedicalBusiness","name":it["name"],
               "url":f"{SITE}/{name}/{it['slug']}/","description":clip(it["desc"], 300),
               "areaServed":it["region"]}
        if it.get("website"): biz["sameAs"] = it["website"]
        if it.get("phone"): biz["telephone"] = it["phone"]
        w(f"{name}/{it['slug']}/index.html", shell(f"{name}/{it['slug']}/index.html", f"{it['name']} — {singular} in {it['region']} | plugreports", clip(it["desc"]), body, jsonld=biz))

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
      clip("plugreports is an independent harm-reduction library: visual drug profiles, verified hotlines and rehabs, sourced busts and news for USA, Canada, Europe, Australia and Africa."), body))

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
def build_data():
    """Citable data asset: fentanyl adulterant tracker. Plain numbers + sources, built for journalist citation."""
    tbl_rows = [
        ("Xylazine (&ldquo;tranq&rdquo;)", "18,138", "#6", "Veterinary sedative",
         "Necrotic skin wounds, hours-long blackouts, blood-pressure crashes",
         "No — but give it anyway: fentanyl is almost always present too", "xylazine"),
        ("Medetomidine (&ldquo;rhino tranq&rdquo;)", "8,980", "#10", "Veterinary sedative, 100–200&times; xylazine&rsquo;s potency",
         "ICU-grade withdrawal, profound sedation, dangerously slow heart rate",
         "No — same fentanyl caveat", "medetomidine"),
        ("BTMPS (Tinuvin 770)", "8,138", "#11", "Industrial plastic UV stabilizer",
         "Calcium-channel blocker, no antidote; the &ldquo;bug spray&rdquo; smell tell",
         "No — no antidote exists", "btmps"),
        ("para-Fluorofentanyl", "3,535 <span class='mini'>6,708 all isomers</span>", "#16", "Fentanyl analogue",
         "Full opioid overdose risk; routinely co-detected with the adulterants above",
         "Yes — naloxone works", "para-fluorofentanyl"),
        ("Heroin", "27,286", "#5", "Classic opioid",
         "Still co-reported with fentanyl in thousands of exhibits",
         "Yes", "heroin"),
        ("Cocaine &amp; methamphetamine", "195,317 / 323,404", "#2 / #1", "Stimulants",
         "Not adulterants of fentanyl — but ~1 in 4 cocaine and ~1 in 8 meth exhibits now test positive for it",
         "Yes", "cocaine"),
    ]
    trs = "".join(
        f'<tr><td><b>{name}</b></td><td>{reports}</td><td>{rank}</td><td>{what}</td><td>{why}</td>'
        f'<td>{nal}</td><td><a href="/drugs/{slug}/">Profile &rarr;</a></td></tr>'
        for name, reports, rank, what, why, nal, slug in tbl_rows)
    jsonld = {
      "@context": "https://schema.org", "@type": "Dataset",
      "name": "Fentanyl Adulterant Tracker — substances co-detected with fentanyl in US forensic laboratories",
      "description": "Yearly forensic-laboratory report counts (DEA NFLIS-Drug 2025) for fentanyl and its most common adulterants — xylazine, medetomidine, BTMPS and para-fluorofentanyl — with trend and regional data from CDC and the DEA National Drug Threat Assessment.",
      "creator": {"@type": "Organization", "name": "plugreports", "url": SITE},
      "dateModified": TODAY, "license": "https://plugreports.com/about/",
      "isAccessibleForFree": True,
      "variableMeasured": ["Xylazine", "Medetomidine", "BTMPS", "para-Fluorofentanyl", "Fentanyl"],
      "temporalCoverage": "2023/2025",
      "spatialCoverage": {"@type": "Country", "name": "United States"},
    }
    body = (
      '<div class="wrap"><div style="max-width:960px;padding:26px 0">'
      '<span class="kicker">Data &middot; updated September 2026</span>'
      '<h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Fentanyl Adulterant Tracker</h1>'
      '<p class="lede" style="color:#667085">What is actually being mixed into the US fentanyl supply, in plain numbers. '
      'Every figure below comes from the DEA&rsquo;s NFLIS forensic-laboratory system, the CDC, or peer-reviewed research — '
      'with the source named and dated. Free to cite; please link back.</p>'
      '<div class="callout red"><b>Emergency note first</b>'
      'Xylazine, medetomidine and BTMPS are <b>not opioids</b> — naloxone (Narcan) does not reverse them. '
      'But because fentanyl is almost always present in the same sample, <b>give naloxone anyway, every time</b>, and call emergency services.</div>'
      '<div class="stat-grid">'
      '<div class="stat red"><b>132,210</b><span>fentanyl reports (NFLIS 2025)</span></div>'
      '<div class="stat"><b>18,138</b><span>xylazine reports</span></div>'
      '<div class="stat"><b>8,980</b><span>medetomidine reports</span></div>'
      '<div class="stat"><b>8,138</b><span>BTMPS reports</span></div>'
      '<div class="stat"><b>69,973</b><span>US overdose deaths 2025 (provisional)</span></div>'
      '</div>'
      '<h2>The 2025 numbers</h2>'
      '<p>NFLIS-Drug recorded <b>1,126,178 substance identifications</b> across 666,357 cases in 2025. '
      'These are the substances most often found alongside fentanyl — the adulterants and co-reports that define the modern supply:</p>'
      '<div class="figure"><table class="tbl"><thead><tr><th>Substance</th><th>2025 NFLIS reports</th><th>Rank</th>'
      '<th>What it is</th><th>Why it matters</th><th>Naloxone?</th><th></th></tr></thead><tbody>'
      + trs + '</tbody></table></div>'
      '<h2>The story of 2025–26: medetomidine&rsquo;s takeover</h2>'
      '<div class="callout amber"><b>Xylazine &rarr; medetomidine, in one city&rsquo;s data</b>'
      'In Philadelphia, medetomidine went from <b>29% of street opioid samples (May 2024) to 90% (March 2026)</b> — '
      'while xylazine fell from 97% to 28% over the same period. The same substitution pattern is now appearing in other cities.</div>'
      '<ul class="ticks">'
      '<li><b>Medetomidine NFLIS reports:</b> 247 (2023) &rarr; 2,616 (2024) &rarr; 8,233+ (2025) — a 950% jump, then another tripling.</li>'
      '<li><b>CDC sentinel sites (Jul–Dec 2025):</b> 10 of 20 testing sites found medetomidine in roughly a third of opioid-positive samples; 8 sites found it in more than half. <b>98% of medetomidine-positive samples had fentanyl co-detected.</b></li>'
      '<li><b>Regional split:</b> Northeast 74.2% of opioid-positive samples &middot; Midwest 56.2% &middot; South 30.1% &middot; West 3.8%.</li>'
      '<li><b>New York City deaths:</b> 18 overdose deaths with medetomidine contributing in 2024 &rarr; <b>134 in 2025</b>.</li>'
      '<li><b>BTMPS went from zero to top-12 in 18 months:</b> first detected June 2024 (Portland, Philadelphia); by 2025 it was the 11th most-reported substance in NFLIS — an industrial plastic stabilizer with no antidote.</li>'
      '<li><b>Xylazine baseline:</b> 30% of DEA-seized fentanyl powder in 2023 contained xylazine (25% in 2022); identified in seized samples in every US state, DC and Puerto Rico by 2024.</li>'
      '</ul>'
      '<h2>Context</h2>'
      '<p>US drug overdose deaths fell for a third straight year in 2025 — an estimated <b>69,973 deaths (provisional, &minus;14%)</b>, '
      'with opioid-involved deaths down from 55,296 to <b>44,564</b>. The adulterant problem is the reason these deaths are harder to reverse: '
      'an increasing share of the supply contains sedatives and industrial chemicals that naloxone was never designed to touch.</p>'
      '<h2>Methodology &amp; sources</h2>'
      '<ul class="ticks">'
      '<li><b>DEA NFLIS-Drug</b> — 2025 annual drug-case and report counts (nflis.deadiversion.usdoj.gov).</li>'
      '<li><b>DEA 2025 National Drug Threat Assessment</b> — top-10 substances mixed with fentanyl, 2019 vs 2024; xylazine seizure geography; cocaine/meth co-detection rates.</li>'
      '<li><b>CDC Health Alert Network (April 2026)</b> and CDC Overdose Prevention situation summary — medetomidine sentinel-site data and NFLIS trend counts.</li>'
      '<li><b>CDC NCHS (May 2026)</b> — provisional 2025 overdose death estimates.</li>'
      '<li><b>JAMA research letter (March 2025)</b> — BTMPS in the illicit fentanyl supply across nine US locations.</li>'
      '<li><b>Washington/Baltimore HIDTA bulletin (April 2025)</b> — BTMPS spread and combination patterns.</li>'
      '</ul>'
      '<div class="callout gray"><b>How to cite this page</b>'
      'plugreports.com — &ldquo;Fentanyl Adulterant Tracker&rdquo;, updated September 2026. '
      'Primary sources: DEA NFLIS-Drug 2025, DEA 2025 National Drug Threat Assessment, CDC HAN April 2026, JAMA March 2025. '
      'URL: https://plugreports.com/data/fentanyl-adulterants/</div>'
      '<p style="margin-top:18px">Related: <a href="/topics/fentanyl-numbers/">Fentanyl in numbers — the full guide</a> &middot; '
      '<a href="/drugs/fentanyl/">Fentanyl profile</a> &middot; <a href="/drugs/medetomidine/">Medetomidine profile</a> &middot; '
      '<a href="/drugs/xylazine/">Xylazine profile</a> &middot; <a href="/hotlines/">Overdose hotlines by region</a></p>'
      '</div></div>')
    w("data/fentanyl-adulterants/index.html", shell(
      "data/fentanyl-adulterants/", "Fentanyl Adulterant Tracker — NFLIS 2025 data: xylazine, medetomidine, BTMPS",
      "Live data page: what is being mixed into the US fentanyl supply in 2025–26 — NFLIS report counts for xylazine, medetomidine, BTMPS and para-fluorofentanyl, with CDC and DEA sources, updated September 2026.",
      body, jsonld=jsonld))


def build_data_top():
    """Citable data asset: top 15 substances in NFLIS 2025 — the demand-side counterpart to the adulterant tracker."""
    TOTAL = 1126178  # NFLIS 2025 total reports
    top15 = [
        (1, "Methamphetamine", 323404, "Stimulant", "The #1 most-identified drug in US drug cases for over a decade; dominates the West and Midwest.", "methamphetamine"),
        (2, "Cocaine", 195317, "Stimulant", "Powder and crack; about 1 in 4 cocaine exhibits now also contains fentanyl.", "cocaine"),
        (3, "Cannabinoids (unspecified)", 143207, "Cannabinoid", "Mostly marijuana — this count reflects how often cannabis appears in drug cases, not danger.", "weed"),
        (4, "Fentanyl", 132210, "Synthetic opioid", "The driver of the overdose crisis; found in ~1 in 8 meth and ~1 in 4 cocaine exhibits.", "fentanyl"),
        (5, "Heroin", 27286, "Opioid", "Largely displaced by fentanyl, but still co-reported in thousands of exhibits.", "heroin"),
        (6, "Xylazine (&ldquo;tranq&rdquo;)", 18138, "Veterinary sedative", "The wound-causing fentanyl adulterant; detected in every US state, DC and Puerto Rico by 2024.", "xylazine"),
        (7, "Fentanyl analogues (unspecified)", 16543, "Synthetic opioid", "Illicit fentanyl variants sold as heroin or pressed into fake pills — part of the fentanyl family.", "fentanyl"),
        (8, "Delta-9-THC", 11580, "Cannabinoid", "The impairing form of THC — counted mostly in driving and impairment cases.", "weed"),
        (9, "Oxycodone", 10128, "Opioid", "The most-counterfeited prescription pill; most &ldquo;oxy&rdquo; bought on the street is fentanyl.", "oxycodone"),
        (10, "Medetomidine", 8980, "Veterinary sedative", "The fastest-rising substance on the list: 247 reports in 2023 &rarr; 8,980 in 2025.", "medetomidine"),
        (11, "BTMPS (Tinuvin 770)", 8138, "Industrial chemical", "An industrial plastic stabilizer with no antidote; first detected in the supply in June 2024.", "btmps"),
        (12, "Buprenorphine", 7632, "Opioid (treatment)", "The leading opioid-addiction medication; also diverted and misused.", "suboxone"),
        (13, "Alprazolam", 7015, "Benzodiazepine", "The most-abused prescription benzo; fake &ldquo;Xanax&rdquo; bars usually contain fentanyl or research-chemical benzos.", "alprazolam"),
        (14, "Hydrocodone", 6956, "Opioid", "Vicodin-type painkiller; commonly counterfeited with fentanyl.", "hydrocodone"),
        (15, "4-ANPP", 6792, "Fentanyl precursor", "A chemical marker of illicit fentanyl production — its presence means clandestine synthesis.", "fentanyl"),
    ]
    trs = "".join(
        f'<tr><td>#{r}</td><td><b>{name}</b></td><td>{n:,}</td><td>{n/TOTAL*100:.2f}%</td>'
        f'<td>{cls}</td><td>{why}</td><td><a href="/drugs/{slug}/">Profile &rarr;</a></td></tr>'
        for r, name, n, cls, why, slug in top15)
    jsonld = {
      "@context": "https://schema.org", "@type": "Dataset",
      "name": "Top 15 substances identified in US forensic laboratories, NFLIS 2025",
      "description": "DEA NFLIS-Drug 2025 annual report counts for the 15 most frequently identified substances in US forensic drug cases, with plain-English context and links to harm-reduction profiles.",
      "creator": {"@type": "Organization", "name": "plugreports", "url": SITE},
      "dateModified": TODAY, "isAccessibleForFree": True,
      "variableMeasured": [t[1] for t in top15], "temporalCoverage": "2025",
      "spatialCoverage": {"@type": "Country", "name": "United States"},
    }
    body = (
      '<div class="wrap"><div style="max-width:960px;padding:26px 0">'
      '<span class="kicker">Data &middot; updated September 2026</span>'
      '<h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Top 15 Substances in US Drug Cases, 2025</h1>'
      '<p class="lede" style="color:#667085">The 15 most frequently identified substances in American forensic laboratories last year, '
      'from the DEA&rsquo;s NFLIS-Drug system — with plain-English context for every entry. Free to cite; please link back.</p>'
      '<div class="stat-grid">'
      '<div class="stat red"><b>1,126,178</b><span>total lab reports (2025)</span></div>'
      '<div class="stat"><b>666,357</b><span>drug cases analyzed</span></div>'
      '<div class="stat"><b>323,404</b><span>#1 methamphetamine reports</span></div>'
      '<div class="stat"><b>148,753</b><span>fentanyl + analogue reports</span></div>'
      '</div>'
      '<div class="callout gray"><b>How to read this list</b>'
      'NFLIS counts laboratory identifications in actual drug cases — seizures, driving stops, overdose deaths. '
      'It measures what is in the supply and in front of law enforcement, <b>not</b> how many people use a drug. '
      'Cannabis ranks high because it is common in cases, not because it is dangerous.</div>'
      '<h2>The 2025 top 15</h2>'
      '<div class="figure"><table class="tbl"><thead><tr><th>#</th><th>Substance</th><th>2025 reports</th>'
      '<th>Share of all reports</th><th>Class</th><th>Why it matters</th><th></th></tr></thead><tbody>'
      + trs + '</tbody></table></div>'
      '<h2>What stands out in 2025</h2>'
      '<ul class="ticks">'
      '<li><b>Stimulants are half the map:</b> methamphetamine + cocaine = 518,721 reports — 46% of everything counted. The stimulant supply is now more fentanyl-contaminated than the opioid supply in some regions.</li>'
      '<li><b>The fentanyl family is 155,515 reports (13.8%)</b> once you add analogues and 4-ANPP — and every member of that family is one overdose away from being in a death case.</li>'
      '<li><b>Two veterinary sedatives and a plastic stabilizer sit in the top 15.</b> Xylazine, medetomidine and BTMPS are not drugs of choice — they are adulterants, and naloxone does not reverse them.</li>'
      '<li><b>Prescription pills on this list are mostly fakes.</b> Most &ldquo;oxycodone&rdquo;, &ldquo;Xanax&rdquo; and &ldquo;hydrocodone&rdquo; bought on the street is pressed fentanyl — which is why those three names appear in overdose data far out of proportion to their prescriptions.</li>'
      '<li><b>Context:</b> US drug overdose deaths fell to an estimated 69,973 in 2025 (&minus;14%), the third straight annual decline — but opioid-involved deaths still killed an estimated 44,564 people.</li>'
      '</ul>'
      '<h2>Methodology &amp; sources</h2>'
      '<ul class="ticks">'
      '<li><b>DEA NFLIS-Drug</b> — 2025 annual top-25 drug counts (nflis.deadiversion.usdoj.gov), retrieved September 2026.</li>'
      '<li><b>DEA 2025 National Drug Threat Assessment</b> — fentanyl co-detection rates in cocaine/methamphetamine exhibits; xylazine geography.</li>'
      '<li><b>CDC NCHS (May 2026)</b> — provisional 2025 overdose death estimates.</li>'
      '<li>Percentages are share of the 1,126,178 total 2025 NFLIS reports. &ldquo;Fentanyl family&rdquo; = fentanyl + unspecified analogues + 4-ANPP.</li>'
      '</ul>'
      '<div class="callout gray"><b>How to cite this page</b>'
      'plugreports.com — &ldquo;Top 15 Substances in US Drug Cases, 2025&rdquo;, updated September 2026. '
      'Primary source: DEA NFLIS-Drug 2025 annual data. URL: https://plugreports.com/data/top-substances-2025/</div>'
      '<p style="margin-top:18px">Related: <a href="/data/fentanyl-adulterants/">Fentanyl Adulterant Tracker</a> &middot; '
      '<a href="/topics/fentanyl-numbers/">Fentanyl in numbers</a> &middot; <a href="/drugs/">Full drug library</a></p>'
      '</div></div>')
    w("data/top-substances-2025/index.html", shell(
      "data/top-substances-2025/", "Top 15 Substances in US Drug Cases 2025 — NFLIS Data | plugreports",
      "The 15 most-identified substances in US forensic labs in 2025 (DEA NFLIS): methamphetamine, cocaine, fentanyl, xylazine, medetomidine, BTMPS and more — with context and sources, updated September 2026.",
      body, jsonld=jsonld))


def build_data_hub():
    body = (
      '<div class="wrap"><div style="max-width:960px;padding:26px 0">'
      '<span class="kicker">Data</span>'
      '<h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">plugreports Data</h1>'
      '<p class="lede" style="color:#667085">Plain-number trackers built for journalists, educators and researchers. '
      'Every figure is sourced and dated. Free to cite — please link back.</p>'
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:24px">'
      '<a class="card" href="/data/fentanyl-adulterants/"><h3>Fentanyl Adulterant Tracker</h3>'
      '<p>What is actually being mixed into the US fentanyl supply in 2025–26 — xylazine, medetomidine, BTMPS and para-fluorofentanyl, with NFLIS and CDC counts.</p>'
      '<div class="foot">Open the tracker &rarr;</div></a>'
      '<a class="card" href="/data/top-substances-2025/"><h3>Top 15 Substances, 2025</h3>'
      '<p>The 15 most-identified substances in US forensic laboratories last year, with share-of-total and plain-English context for each.</p>'
      '<div class="foot">Open the ranking &rarr;</div></a>'
      '</div>'
      '<p style="margin-top:22px;color:#667085;font-size:14px">Using our data? '
      '<a href="/about/">Editorial policy & sources</a> &middot; <a href="/suggest/">Report a correction</a></p>'
      '</div></div>')
    w("data/index.html", shell(
      "data/", "Data & Trackers — Sourced Drug-Supply Numbers | plugreports",
      "Free, citable data trackers from plugreports: the fentanyl adulterant tracker and the NFLIS top-15 substance ranking, with dated DEA/CDC sources.",
      body))


def build_meta():
    from data_es import ES_DRUGS as _ESD
    ES_DRUG_KEYS = list(_ESD.keys())
    B = TODAY  # build date — lastmod fallback when an item has no date of its own
    urls = [("", B), ("news/", B), ("busts/", B), ("topics/", B), ("quit/", B),
            ("hotlines/", B), ("sentencing/", B), ("pharmacies/", B), ("rehabs/", B),
            ("about/", B), ("suggest/", B), ("drugs/", B), ("categories/", B), ("data/", B), ("data/fentanyl-adulterants/", B), ("data/top-substances-2025/", B)]
    urls += [(f"categories/{k}/", B) for k in CATEGORIES]
    urls += [("es/", B), ("es/hotlines/", B), ("es/categories/", B)]
    urls += [(f"es/drugs/{sl}/", DRUG_BY_SLUG[sl].get("lastUpdated", B)) for sl in ES_DRUG_KEYS if sl in DRUG_BY_SLUG]
    urls += [(f"es/categories/{k}/", B) for k in CATEGORIES if any(d["slug"] in ES_DRUG_KEYS for d in DRUGS if d["category"] == k)]
    from data_i18n import LANGS as _LANGS
    for _L in _LANGS:
        urls += [(f"{_L}/", B), (f"{_L}/hotlines/", B)]
        urls += [(f"{_L}/drugs/{sl}/", DRUG_BY_SLUG[sl].get("lastUpdated", B)) for sl in _LANGS[_L]["drugs"] if sl in DRUG_BY_SLUG]
        _cats = {DRUG_BY_SLUG[sl]["category"] for sl in _LANGS[_L]["drugs"] if sl in DRUG_BY_SLUG}
        urls += [(f"{_L}/categories/{c}/", B) for c in _cats]
    urls += [(f"drugs/{d['slug']}/", d.get("lastUpdated", B)) for d in DRUGS]
    urls += [(f"news/{n['slug']}/", n.get("date", B)) for n in NEWS]
    urls += [(f"busts/{b['slug']}/", b.get("date", B)) for b in BUSTS if not b.get("noindex")]
    urls += [(f"topics/{t['slug']}/", t.get("date", B)) for t in TOPICS]
    urls += [(f"quit/{k}/", B) for k in QUIT_SPECS]
    if MIX:
        urls += [("mix/", B)]
        urls += [(f"mix/{m['slug']}/", m.get("lastUpdated", B)) for m in MIX]
    if VS:
        urls += [("vs/", B)]
        urls += [(f"vs/{v['slug']}/", v.get("lastUpdated", B)) for v in VS]
    urls += [(f"pharmacies/{p['slug']}/", B) for p in PHARMACIES]
    urls += [(f"rehabs/{r['slug']}/", B) for r in REHABS]
    sm = "\n".join(f'<url><loc>{SITE}/{u}</loc><lastmod>{lm}</lastmod></url>' for u, lm in urls)
    w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>')
    w("robots.txt",
      "# plugreports.com crawler policy\n"
      "# AI/LLM crawlers are intentionally ALLOWED: this is a public harm-reduction dataset\n"
      "# and we want it cited. Machine-readable mirrors: /llms.txt (index) and /llms-full.txt\n"
      "# (complete drug records). Only the admin UI is disallowed.\n"
      f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {SITE}/sitemap.xml\n")
    items = "".join(f"<item><title>{esc(n['title'])}</title><link>{SITE}/news/{n['slug']}/</link><guid>{SITE}/news/{n['slug']}/</guid><description>{esc(clip(n['summary'], 300))}</description><pubDate>{rfc822(n['date'])}</pubDate></item>" for n in NEWS)
    w("rss.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>plugreports — Drug News</title><link>{SITE}/news/</link><description>Drug news, adulterant alerts and supply trends from plugreports.com — sourced from NIDA, DEA, EMCDDA, ONS and drug-checking services.</description><language>en</language><atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>{items}</channel></rss>')
    # ---- llms.txt: full-coverage index for LLM crawlers ----
    L = ["# plugreports", "",
         "> Harm-reduction library of street drug profiles, busts, hotlines and verified help. USA, Canada, Europe, Australia, Africa.",
         "",
         f"Complete machine-readable drug records: [llms-full.txt]({SITE}/llms-full.txt)", "",
         "## Key pages",
         f"- [/hotlines/]({SITE}/hotlines/) Verified overdose & crisis hotlines, {len(HOTLINES)} regions",
         f"- [/drugs/]({SITE}/drugs/) A-Z index of all {len(DRUGS)} substance profiles",
         f"- [/categories/]({SITE}/categories/) Browse by category",
         f"- [/news/]({SITE}/news/) Drug news & alerts",
         f"- [/busts/]({SITE}/busts/) Busts & seizures tracker",
         f"- [/topics/]({SITE}/topics/) Guides & explainers",
         f"- [/quit/]({SITE}/quit/) Quitting, day by day",
         f"- [/sentencing/]({SITE}/sentencing/) Drug sentencing by region",
         f"- [/pharmacies/]({SITE}/pharmacies/) Verified online pharmacies",
         f"- [/rehabs/]({SITE}/rehabs/) Verified rehab centers",
         f"- [/about/]({SITE}/about/) Mission & editorial policy", ""]
    L.append(f"## Drug library ({len(DRUGS)} profiles)")
    for k, c in CATEGORIES.items():
        items_k = [d for d in DRUGS if d["category"] == k]
        if not items_k: continue
        L.append(f"### {c['name']}")
        for d in items_k:
            L.append(f"- [/drugs/{d['slug']}/]({SITE}/drugs/{d['slug']}/) {d['name']} — aka {', '.join(d['aliases'][:3])}")
    L += ["", "## Guides & explainers"]
    for t in TOPICS: L.append(f"- [/topics/{t['slug']}/]({SITE}/topics/{t['slug']}/) {t['title']}")
    L += ["", "## Quitting, day by day"]
    for k, v in QUIT_SPECS.items(): L.append(f"- [/quit/{k}/]({SITE}/quit/{k}/) Quitting {v['name']} — day-by-day withdrawal timeline")
    L += ["", "## Hotlines by region"]
    for region, its in HOTLINES.items(): L.append(f"- [/hotlines/]({SITE}/hotlines/) {region} — e.g. {its[0][1]} ({its[0][0]})")
    L += ["", "## Verified pharmacies"]
    for p in PHARMACIES: L.append(f"- [/pharmacies/{p['slug']}/]({SITE}/pharmacies/{p['slug']}/) {p['name']} ({p['region']})")
    L += ["", "## Verified rehabs & recovery programs"]
    for r in REHABS: L.append(f"- [/rehabs/{r['slug']}/]({SITE}/rehabs/{r['slug']}/) {r['name']} ({r['region']})")
    L += ["", "## Sentencing by region"]
    for st in SENTENCING: L.append(f"- [/sentencing/]({SITE}/sentencing/) {st['region']}")
    L += ["", "## News"]
    for n in NEWS: L.append(f"- [/news/{n['slug']}/]({SITE}/news/{n['slug']}/) {n['title']}")
    L += ["", "## Busts & seizures"]
    for b in BUSTS:
        if not b.get("noindex"): L.append(f"- [/busts/{b['slug']}/]({SITE}/busts/{b['slug']}/) {b['title']}")
    if MIX:
        L += ["", "## Mixing dangers"]
        L.append(f"- [/mix/]({SITE}/mix/) Hub — {len(MIX)} drug-combination guides ranked by danger")
        for m in MIX: L.append(f"- [/mix/{m['slug']}/]({SITE}/mix/{m['slug']}/) {m['a']} + {m['b']} — {m.get('level', 'caution')}")
    if VS:
        L += ["", f"## Vs — drug comparisons ({len(VS)})"]
        L.append(f"- [/vs/]({SITE}/vs/) Hub — {len(VS)} head-to-head comparisons in plain English")
        for v in VS: L.append(f"- [/vs/{v['slug']}/]({SITE}/vs/{v['slug']}/) {v['title']}")
    w("llms.txt", "\n".join(L) + "\n")
    # ---- llms-full.txt: complete compact drug records (GEO flagship artifact) ----
    F = ["# plugreports — full drug records",
         f"> {len(DRUGS)} harm-reduction profiles, compiled from NIDA, DEA, EMCDDA, WHO and peer-reviewed literature. "
         "Street prices are regional estimates that change quickly. Educational information only — not medical advice. "
         f"Canonical pages: {SITE}/drugs/<slug>/", ""]
    for d in DRUGS:
        c = CATEGORIES[d["category"]]
        F.append(f"## {d['name']}")
        F.append(f"- url: {SITE}/drugs/{d['slug']}/")
        F.append(f"- aliases: {', '.join(d['aliases'])}")
        F.append(f"- category: {c['name']}")
        F.append(f"- schedule: {d['schedule']}")
        F.append(f"- appearance: {d['appearance']}")
        F.append(f"- effects: {'; '.join(d['effects'])}")
        F.append(f"- risks: {'; '.join(d['risks'])}")
        F.append(f"- overdoseSigns: {'; '.join(d['overdoseSigns'])}")
        F.append(f"- streetPrice: {d['streetPrice']}")
        F.append(f"- legalStatus: {d['legalStatus']}")
        F.append(f"- lastUpdated: {d['lastUpdated']}")
        F.append(f"- sources: {', '.join(d['sources'])}")
        F.append("")
    w("llms-full.txt", "\n".join(F))




def build_categories_es():
    from data_es import ES_DRUGS, ES_CATS
    made = []
    for k, c in CATEGORIES.items():
        items = [d for d in DRUGS if d["category"] == k and d["slug"] in ES_DRUGS]
        if not items: continue
        made.append(k)
        cat_name = ES_CATS.get(k, c["name"])
        cards = "".join(
            "<a class=\"card\" href=\"/es/drugs/" + d["slug"] + "/\"><div class=\"meta\"><span class=\"chip\" style=\"border-color:" + c["color"] + "33;color:" + c["color"] + "\">" + esc((ES_DRUGS[d["slug"]].get("schedule") or d["schedule"]).split("(")[0].strip()[:24]) + "</span></div><h3>" + esc(d["name"]) + "</h3><p>" + esc(ES_DRUGS[d["slug"]].get("appearance", d["appearance"])) + "</p><div class=\"foot\">Efectos y riesgos &rarr;</div></a>"
            for d in items)
        body = """<div class="wrap">
<section class="cat-hero" style="background:@GRAD@"><span class="kicker" style="background:rgba(255,255,255,.15);color:#fff;border:0">@COUNT@ sustancias</span>
<h1>@NAME@</h1><p>@TAG@</p></div>
<div class="cards">@CARDS@</div></div>""".replace("@GRAD@", c["grad"]).replace("@COUNT@", str(len(items))).replace("@NAME@", esc(cat_name)).replace("@TAG@", esc(c["tagline"])).replace("@CARDS@", cards)
        out = f"es/categories/{k}/index.html"
        w(out, shell(out, f"{cat_name} — efectos, riesgos y signos de sobredosis | plugreports",
            f"Perfiles de reducción de riesgos sobre {cat_name}: efectos, riesgos, signos de sobredosis y precios.",
            body, lang="es", canonical=f"{SITE}/es/categories/{k}/", alts=cat_alts(k)))
    if made:
        idx = "".join(
            "<a class=\"card\" href=\"/es/categories/" + k + "/\"><h3>" + esc(ES_CATS.get(k, CATEGORIES[k]["name"])) + "</h3><p>" + esc(CATEGORIES[k]["tagline"]) + "</p><div class=\"foot\">Ver categoría &rarr;</div></a>"
            for k in made)
        w("es/categories/index.html", shell("es/categories/index.html",
            "Categorías de drogas — opioides, estimulantes, benzos y más | plugreports",
            "Todas las categorías de drogas en plugreports: opioides, estimulantes, benzodiacepinas, cannabinoides y más.",
            "<div class=\"wrap\"><section class=\"sec-head\" style=\"padding-top:30px\"><div><span class=\"kicker amber\">Biblioteca de drogas</span><h1>Categorías</h1></div></section><div class=\"cards\">" + idx + "</div></div>",
            lang="es", canonical=f"{SITE}/es/categories/",
            alts=_alt_set(f"{SITE}/categories/", es=f"{SITE}/es/categories/")))



LANG_LIST = ("de", "hi", "no", "pl", "fr")

def build_lang_drug_pages(lang):
    from data_i18n import LANGS
    pack = LANGS[lang]
    TR, CATS_T = pack["drugs"], pack["cats"]
    for slug, o in TR.items():
        d = DRUG_BY_SLUG[slug]
        c = CATEGORIES[d["category"]]
        cat_name = CATS_T.get(d["category"], c["name"])
        pimg, _img_rel = pimg_html(d, c, o.get("appearance", d["appearance"]))
        rel = related_drugs(d)
        relhtml = "".join(f'<a href="/{lang}/drugs/{r["slug"]}/">{rel_card(r["slug"])}</a>' for r in rel[:4] if r["slug"] in TR) or "".join(f'<a href="/drugs/{r["slug"]}/">{rel_card(r["slug"])}</a>' for r in rel[:4])
        rows = "".join(f'<div class="fact"><b>{k}</b><span>{v}</span></div>' for k, v in [
            ("Also known as", esc(", ".join(d["aliases"]))),
            ("Category", f'<span class="cat-dot" style="background:{c["color"]}"></span>{esc(cat_name)}'),
            ("Schedule / class", esc(o.get("schedule", d["schedule"]))),
            ("Appearance", esc(o.get("appearance", d["appearance"]))),
            ("Street price", esc(o.get("streetPrice", d["streetPrice"]))),
            ("Legal status", esc(o.get("legalStatus", d["legalStatus"]))),
            ("Last updated", esc(d["lastUpdated"]))])
        body = f"""
<div class="wrap">
<div class="ptop">
<div class="ptop-main">
<section class="phead">
<span class="glyph" style="background:{c['grad']}">{esc(d['name'][0])}</span>
<div><span class="kicker" style="background:{c['grad']};color:#fff;border:0">{esc(cat_name)}</span>
<h1 style="margin-top:10px">{esc(d['name'])}</h1>
<p class="alias">Street names: <b>{esc(", ".join(d["aliases"]))}</b></p></div></section>
<div class="callout red print-hide"><b>Overdose? Act now.</b> Call emergency services. Give naloxone for opioid-like signs. <a href="/{lang}/hotlines/">Hotlines</a></div>
<div class="panel"><h2><span class="ic" style="background:{c['color']};color:#fff">&#9889;</span>What it does</h2>
<ul class="ticks">{''.join(f"<li>{esc(e)}</li>" for e in o["effects"])}</ul>
<h2 style="margin-top:22px"><span class="ic" style="background:#dc2626;color:#fff">&#9888;</span>Key risks</h2>
<ul class="ticks red">{''.join(f"<li>{esc(r)}</li>" for r in o["risks"])}</ul>
<h2 style="margin-top:22px"><span class="ic" style="background:#111827;color:#fff">&#10010;</span>Overdose signs</h2>
<ul class="ticks red">{''.join(f"<li>{esc(x)}</li>" for x in o["overdoseSigns"])}</ul></div>
</div>
<aside class="ptop-rail">
{pimg}
<div class="panel"><h2><span class="ic" style="background:{c['color']};color:#fff">&#128203;</span>Quick facts</h2>{rows}
<div style="margin-top:14px"><span class="chip green">Sources: {esc(", ".join(d["sources"]))}</span></div></div>
</aside>
</div>
<div class="related print-hide"><h2>You may also want to know about</h2>
<div class="rel-grid">{relhtml}
<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a></div></div>
</div>"""
        title = f"{d['name']}: effects, overdose signs, street price & help | plugreports"
        out = f"{lang}/drugs/{slug}/index.html"
        w(out, shell(out, title, f"{d['name']} — {cat_name}. Effects, overdose signs, street price and harm-reduction info.", body,
                     lang=lang, canonical=f"{SITE}/{lang}/drugs/{slug}/", alts=drug_alts(slug)))

def build_lang_hotlines(lang):
    from data_i18n import LANGS
    pack = LANGS[lang]
    REG_T, HL = pack["regions"], pack["hotlines"]
    secs = []
    for region, items in HL.items():
        rname = REG_T.get(region, region)
        cards = "".join(f"""<div class="hl-card"><h3>{esc(it[1])}</h3>
<div class="num">{esc(it[0])}</div><div class="who">{esc(it[2])}</div>
{f'<a class="call-btn" href="tel:{it[3]}">&#128222; Call</a>' if it[3] else '<span class="chip" style="margin-top:12px">Text / online</span>'}</div>""" for it in items)
        secs.append(f'<section class="hl-region"><span class="kicker amber">{esc(rname)}</span><div class="hl-grid">{cards}</div></section>')
    body = f"""<div class="wrap"><div style="padding-top:26px">
<span class="kicker">Help directory</span><h1 style="font-size:clamp(28px,4vw,42px);margin-top:10px">Hotlines</h1>
{''.join(secs)}
<div class="callout red"><b>Overdose right now?</b>Call your local emergency number FIRST.</div>
</div></div>"""
    out = f"{lang}/hotlines/index.html"
    w(out, shell(out, f"Drug overdose & crisis hotlines | plugreports ({lang})", "Verified overdose and crisis helplines.", body,
                 lang=lang, canonical=f"{SITE}/{lang}/hotlines/", alts=hotline_alts()))

def build_lang_home(lang):
    from data_i18n import LANGS
    H = LANGS[lang]["home"]; CT = LANGS[lang]["cats"]
    rail = "".join(f"""<a class="tile" href="/{lang}/drugs/{sl}/"><span class="glyph" style="background:{CATEGORIES[DRUG_BY_SLUG[sl]['category']]['grad']}">{esc(DRUG_BY_SLUG[sl]['name'][0])}</span><h3>{esc(DRUG_BY_SLUG[sl]['name'])}</h3><span class="cat"><span class="cat-dot" style="background:{CATEGORIES[DRUG_BY_SLUG[sl]['category']]['color']}"></span>{esc(CT.get(DRUG_BY_SLUG[sl]['category'], ''))}</span></a>""" for sl in LANGS[lang]["drugs"])
    body = f"""
<section class="hero"><div class="wrap">
<span class="kicker">{esc(H['kicker'])}</span>
<h1>{H['h1']}</h1>
<p class="lede">{esc(H['lede'])}</p>
<div class="hero-cta"><a class="btn btn-red" href="/{lang}/hotlines/">{esc(H['b1'])}</a><a class="btn btn-amber" href="#library">{esc(H['b2'])}</a></div>
</div></section>
<section class="sec" id="library"><div class="wrap">
<div class="sec-head"><div><h2>{esc(H['b2'])}</h2></div></div>
<div class="rail">{rail}</div>
<div class="pill-nav"><a href="/">English →</a><a href="/es/">Español →</a></div>
</div></section>
<section class="sec" style="background:#f9fafb"><div class="wrap">
<div class="sec-head"><div><span class="kicker">{esc(H['hk'])}</span><h2>{esc(H['hh'])}</h2><p>{esc(H['hp'])}</p></div><a class="btn btn-red" href="/{lang}/hotlines/">{esc(H['hb'])}</a></div>
</div></section>"""
    out = f"{lang}/index.html"
    w(out, shell(out, f"plugreports — drug information library ({lang})", clip(H['lede']), body,
                 lang=lang, canonical=f"{SITE}/{lang}/", alts=home_alts()))

def build_lang_categories(lang):
    from data_i18n import LANGS
    pack = LANGS[lang]
    TR, CT = pack["drugs"], pack["cats"]
    cats = sorted({DRUG_BY_SLUG[sl]["category"] for sl in TR})
    for k in cats:
        c = CATEGORIES[k]
        items = [DRUG_BY_SLUG[sl] for sl in TR if DRUG_BY_SLUG[sl]["category"] == k]
        cards = "".join(f'<a class="card" href="/{lang}/drugs/{d["slug"]}/"><h3>{esc(d["name"])}</h3><div class="foot">{esc(CT.get(k, c["name"]))} &rarr;</div></a>' for d in items)
        body = f'<div class="wrap"><section class="cat-hero" style="background:{c["grad"]}"><span class="kicker" style="background:rgba(255,255,255,.15);color:#fff;border:0">{len(items)}</span><h1>{esc(CT.get(k, c["name"]))}</h1><p>{esc(c["tagline"])}</p></section><div class="cards">{cards}</div></div>'
        out = f"{lang}/categories/{k}/index.html"
        w(out, shell(out, f"{CT.get(k, c['name'])} | plugreports", clip(c["tagline"]), body,
                     lang=lang, canonical=f"{SITE}/{lang}/categories/{k}/", alts=cat_alts(k)))

def build_indexes():
    cards = "".join(
        "<a class=\"card\" href=\"/categories/" + k + "/\"><div class=\"meta\"><span class=\"chip\" style=\"border-color:" + v["color"] + "33;color:" + v["color"] + "\">" + str(sum(1 for d in DRUGS if d["category"] == k)) + " substances</span></div><h3>" + esc(v["name"]) + "</h3><p>" + esc(v["tagline"]) + "</p><div class=\"foot\">Browse category &rarr;</div></a>"
        for k, v in CATEGORIES.items())
    catidx_body = "<div class=\"wrap\"><section class=\"sec-head\" style=\"padding-top:30px\"><div><span class=\"kicker amber\">Drug Library</span><h1 style=\"font-family:var(--font-ed);font-size:clamp(28px,4vw,44px)\">All <span style=\"background:linear-gradient(92deg,#f59e0b,#dc2626);-webkit-background-clip:text;background-clip:text;color:transparent\">categories</span></h1><p>" + str(len(CATEGORIES)) + " categories, " + str(len(DRUGS)) + " substances — every profile covers effects, overdose signs, street prices and legal status.</p></div></section><div class=\"cards\">" + cards + "</div></div>"
    w("categories/index.html", shell("categories/index.html",
        "Drug Categories — Opioids, Stimulants, Benzos, Psychedelics & More | plugreports",
        clip("Browse all drug categories: opioids, stimulants, benzodiazepines, psychedelics, dissociatives, synthetic cannabinoids and more — harm-reduction profiles for every substance."),
        catidx_body, alts=_alt_set(f"{SITE}/categories/", es=f"{SITE}/es/categories/")))
    tiles = "".join(
        "<a class=\"tile\" href=\"/drugs/" + d["slug"] + "/\"><span class=\"glyph\" style=\"background:" + CATEGORIES[d["category"]]["grad"] + "\">" + esc(d["name"][0]) + "</span><h3>" + esc(d["name"]) + "</h3><span class=\"cat\"><span class=\"cat-dot\" style=\"background:" + CATEGORIES[d["category"]]["color"] + "\"></span>" + esc(CATEGORIES[d["category"]]["name"]) + "</span></a>"
        for d in sorted(DRUGS, key=lambda x: x["name"]))
    az = sorted(DRUGS, key=lambda x: x["name"])
    az_ld = {"@context":"https://schema.org","@type":"ItemList","name":"All substances, A to Z",
             "numberOfItems":len(az),
             "itemListElement":[{"@type":"ListItem","position":i+1,"name":x["name"],"url":f"{SITE}/drugs/{x['slug']}/"} for i,x in enumerate(az)]}
    w("drugs/index.html", shell("drugs/index.html",
        "Drugs A–Z — All Substances: Street Names, Effects, Overdose Signs | plugreports",
        clip("Complete A-Z index of street drugs, pharmaceuticals, and grey-market substances: street names, effects, overdose signs, street prices and legal status."),
        "<div class=\"wrap\"><section class=\"sec-head\" style=\"padding-top:30px\"><div><span class=\"kicker amber\">A-Z Index</span><h1 style=\"font-family:var(--font-ed);font-size:clamp(28px,4vw,44px)\">All <span style=\"background:linear-gradient(92deg,#f59e0b,#dc2626);-webkit-background-clip:text;background-clip:text;color:transparent\">" + str(len(DRUGS)) + " substances</span>, A to Z</h1><p>Tap any substance for effects, risks, overdose signs and street info.</p></div></section><div class=\"az-grid\">" + tiles + "</div></div>", jsonld=az_ld))

def main():
    build_index(); build_categories(); build_categories_es(); build_drugs(); build_news(); build_busts()
    build_indexes()
    build_topics(); build_quit(); build_mix(); build_vs(); build_hotlines(); build_sentencing()
    build_directory("pharmacies", PHARMACIES, "verified pharmacy",
        "Verified Online Pharmacies — USA, Canada, UK, EU & Worldwide | plugreports",
        "How to verify a licensed online pharmacy in your country — NABP & PharmacyChecker (US/CA), GPhC (UK), EU safety logo, and how to spot counterfeit pill mills before you buy medication online.", "&#128138;")
    build_directory("rehabs", REHABS, "rehab center",
        "Verified Rehab Centers & Free Recovery Programs | plugreports",
        "Verified addiction treatment: Hazelden Betty Ford, Priory, Narcotics Anonymous, SMART Recovery — with contacts and links.", "&#10010;")
    build_drugs(es=True); build_hotlines(es=True); build_index(es=True)
    for _ln in LANG_LIST:
        build_lang_drug_pages(_ln); build_lang_hotlines(_ln); build_lang_home(_ln); build_lang_categories(_ln)
    build_about(); build_suggest(); build_data(); build_data_top(); build_data_hub(); build_meta()
    manifest = {"drugs":[d["slug"] for d in DRUGS], "news":[n["slug"] for n in NEWS],
                "busts":[b["slug"] for b in BUSTS], "topics":[t["slug"] for t in TOPICS],
                "categories":[k for k in CATEGORIES],
                "pharmacies":[p["slug"] for p in PHARMACIES], "rehabs":[r["slug"] for r in REHABS],
                "quit":[k for k in QUIT_SPECS], "mix":[m["slug"] for m in MIX],
                "vs":[v["slug"] for v in VS]}
    w("_static.json", json.dumps(manifest))
    w("_dynamic.html", shell("_dynamic.html", "plugreports",
      "Live content", '<div class="wrap" id="dyn" style="padding:44px 20px;min-height:50vh"><p>Loading\u2026</p></div>',
      extra_head='<script src="/assets/js/render.js?v=15" defer></script>', canonical=SITE + "/"))
    print(f"Built {len(DRUGS)} drug pages, {len(CATEGORIES)} categories, {len(TOPICS)} topics, "
          f"{len(QUIT_SPECS)} quit pages, {len(NEWS)} news, {len(BUSTS)} busts, {len(MIX)} mix pages into {PUB}")

if __name__ == "__main__":
    main()
