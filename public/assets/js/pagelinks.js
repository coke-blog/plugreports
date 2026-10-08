/* Page support links — admin-attached per-page footer links (any language page).
   Fetches the (usually tiny) pagelinks collection, matches the current path,
   and renders a support box at the end of <main>, just before the footer. */
(function () {
  var path = location.pathname;
  if (!path.endsWith('/')) path += '/';
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
      function esc(s) {
        return String(s == null ? '' : s)
          .replace(/&/g, '&amp;').replace(/</g, '&lt;')
          .replace(/"/g, '&quot;');
      }
      var box = document.createElement('div');
      box.className = 'wrap';
      box.innerHTML =
        '<div style="max-width:960px;margin:6px auto 30px;background:#fffbeb;border:1px solid #fcd34d;' +
        'border-radius:16px;padding:16px 20px">' +
        '<b style="font-size:14.5px;color:#92400e">' + esc(hit.heading || 'Support & help for this page') + '</b>' +
        '<div style="display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:8px">' +
        hit.links.map(function (l) {
          var ext = /^https?:\/\//i.test(l.url || '');
          return '<a href="' + esc(l.url) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') +
            ' style="font-size:14px;font-weight:600;color:#b45309;text-decoration:underline">' +
            esc(l.label || l.url) + '</a>';
        }).join('') + '</div></div>';
      var footer = document.querySelector('footer');
      if (footer && footer.parentNode) footer.parentNode.insertBefore(box, footer);
      else document.body.appendChild(box);
    })
    .catch(function () { /* no links — stay silent */ });
})();
