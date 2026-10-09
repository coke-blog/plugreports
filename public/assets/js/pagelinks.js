/* Page support links & images — admin-attached per-page content (any language page).
   Fetches the (usually tiny) pagelinks collection, matches the current path, and renders:
     kind "link"   (default) → amber support box just before <footer>
     kind "image"  → figure grid inside the same box (drug photos etc.)
     kind "header" → full-width image inserted at the top of <main> (header/hero images)
   Entries without a kind are auto-detected: image-looking URLs (/media/..., .jpg/.png/…) render as images. */
(function () {
  var path = location.pathname;
  if (!path.endsWith('/')) path += '/';
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/"/g, '&quot;');
  }
  function looksImage(u) {
    return /^\/media\//i.test(u || '') || /\.(jpe?g|png|webp|gif|avif)(\?|#|$)/i.test(u || '');
  }
  function kindOf(l) {
    if (l.kind === 'header' || l.kind === 'image' || l.kind === 'link') return l.kind;
    return looksImage(l.url) ? 'image' : 'link';
  }
  function figure(l, big) {
    var img = '<img src="' + esc(l.url) + '" alt="' + esc(l.label || '') + '" loading="lazy" ' +
      'style="width:100%;' + (big ? 'max-height:420px;' : 'height:180px;') + 'object-fit:cover;display:block">';
    return '<figure style="margin:0;border:1px solid #e5e7eb;border-radius:14px;overflow:hidden;background:#fff">' +
      img +
      (l.label ? '<figcaption style="padding:8px 12px;font-size:13px;color:#6b7280">' + esc(l.label) + '</figcaption>' : '') +
      '</figure>';
  }
  fetch('/api/public/content?type=pagelinks', { credentials: 'omit' })
    .then(function (r) { return r.json(); })
    .then(function (j) {
      var items = (j && j.items) || [];
      var hit = null;
      for (var i = 0; i < items.length; i++) {
        var p = items[i].path || '';
        if (p && !p.endsWith('/')) p += '/';
        if (p === path) { hit = items[i]; break; }
      }
      if (!hit || !hit.links || !hit.links.length) return;

      var links = [], images = [], headers = [];
      hit.links.forEach(function (l) {
        var k = kindOf(l);
        if (k === 'header') headers.push(l);
        else if (k === 'image') images.push(l);
        else links.push(l);
      });

      /* header images: top of <main> */
      if (headers.length) {
        var main = document.querySelector('main') || document.body;
        var hb = document.createElement('div');
        hb.className = 'wrap';
        hb.innerHTML = '<div style="max-width:960px;margin:14px auto 0">' +
          headers.map(function (l) { return figure(l, true); }).join('') + '</div>';
        if (main.firstChild) main.insertBefore(hb, main.firstChild);
        else main.appendChild(hb);
      }

      /* support box: images grid + link row */
      if (!images.length && !links.length) return;
      var inner = '<div style="max-width:960px;margin:6px auto 30px;background:#fffbeb;border:1px solid #fcd34d;' +
        'border-radius:16px;padding:16px 20px">' +
        '<b style="font-size:14.5px;color:#92400e">' + esc(hit.heading || 'Support & help for this page') + '</b>';
      if (images.length) {
        inner += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:10px">' +
          images.map(function (l) { return figure(l, false); }).join('') + '</div>';
      }
      if (links.length) {
        inner += '<div style="display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:10px">' +
          links.map(function (l) {
            var ext = /^https?:\/\//i.test(l.url || '');
            return '<a href="' + esc(l.url) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') +
              ' style="font-size:14px;font-weight:600;color:#b45309;text-decoration:underline">' +
              esc(l.label || l.url) + '</a>';
          }).join('') + '</div>';
      }
      inner += '</div>';
      var box = document.createElement('div');
      box.className = 'wrap';
      box.innerHTML = inner;
      var footer = document.querySelector('footer');
      if (footer && footer.parentNode) footer.parentNode.insertBefore(box, footer);
      else document.body.appendChild(box);
    })
    .catch(function () { /* no links — stay silent */ });
})();
