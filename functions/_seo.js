// Server-side SEO injection for KV-rendered (dynamic) pages.
// The _dynamic shell ships generic meta (title "plugreports", canonical to home)
// which tells Google every dynamic page is a duplicate of the homepage — this
// helper rewrites the head per item BEFORE the HTML leaves the edge, so
// crawlers (Google, Bing, AI bots) see real titles, descriptions, canonicals,
// Open Graph/Twitter cards and JSON-LD without executing JavaScript.

const SITE = 'https://plugreports.com';

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function clip(s, n) {
  s = String(s || '').replace(/\s+/g, ' ').trim();
  return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '…' : s;
}

// Strip the shell's generic head tags, then inject item-specific ones.
export async function dynamicResponse(env, origin, type, item) {
  const shell = await env.ASSETS.fetch(new Request(origin + '/_dynamic'));
  if (shell.status !== 200) return null;
  let html = await shell.text();

  const name = item.name || item.title || item.slug;
  const title = item.seoTitle || (name + ' | plugreports');
  const desc = clip(item.seoDesc || item.desc || item.blurb || item.tagline ||
                    (item.markdown ? item.markdown.replace(/[#>*`|]/g, '') : ''), 160);
  const url = SITE + '/' + type + '/' + item.slug + '/';
  const img = item.image || (SITE + '/assets/img/og.png');
  const modified = item.date || item.updated || item.lastUpdated || null;

  // remove generic tags from the shell
  html = html
    .replace(/<title>[\s\S]*?<\/title>/, '')
    .replace(/<meta name="description"[^>]*>/, '')
    .replace(/<link rel="canonical"[^>]*>/, '')
    .replace(/<meta name="robots"[^>]*>/, '')
    .replace(/<meta (property|name)="(og:|twitter:)[^"]*"[^>]*>/g, '');

  const jsonld = {
    '@context': 'https://schema.org',
    '@type': ['news', 'busts', 'topics', 'data'].includes(type) ? 'Article' : 'WebPage',
    'headline': name,
    'description': desc,
    'url': url,
    'image': img,
    'inLanguage': 'en',
    'isAccessibleForFree': true,
    'publisher': { '@type': 'Organization', 'name': 'plugreports', 'url': SITE }
  };
  if (modified) jsonld.dateModified = modified;

  const inj =
    '<title>' + esc(title) + '</title>' +
    '<meta name="description" content="' + esc(desc) + '">' +
    '<link rel="canonical" href="' + esc(url) + '">' +
    '<link rel="alternate" hreflang="en" href="' + esc(url) + '">' +
    '<link rel="alternate" hreflang="x-default" href="' + esc(url) + '">' +
    '<meta name="robots" content="max-image-preview:large">' +
    '<meta property="og:type" content="article">' +
    '<meta property="og:site_name" content="plugreports">' +
    '<meta property="og:title" content="' + esc(title) + '">' +
    '<meta property="og:description" content="' + esc(desc) + '">' +
    '<meta property="og:url" content="' + esc(url) + '">' +
    '<meta property="og:image" content="' + esc(img) + '">' +
    '<meta name="twitter:card" content="summary_large_image">' +
    '<meta name="twitter:title" content="' + esc(title) + '">' +
    '<meta name="twitter:description" content="' + esc(desc) + '">' +
    '<meta name="twitter:image" content="' + esc(img) + '">' +
    '<script type="application/ld+json">' + JSON.stringify(jsonld) + '</script>';

  html = html.replace('</head>', inj + '</head>');
  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache' }
  });
}
