/* hydrate.js — live-load admin (KV) content over the static HTML for busts & news.
   Static pages remain the SEO base; edited/added items appear instantly. */
(function () {
  var type = location.pathname.split('/')[1];
  if (!/^(busts|news)$/.test(type)) return;
  fetch('/api/public/content?type=' + type).then(function (r) { return r.json(); }).then(function (d) {
    var items = (d.items || []).filter(function (x) { return x && x.slug; });
    if (!items.length) return;
    var seg = location.pathname.split('/').filter(Boolean);
    if (seg.length === 1) { renderIndex(items, type); }
    else { renderDetail(items.find(function (x) { return x.slug === seg[1]; }), type); }
  }).catch(function () {});

  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function chip(t, cls) { return '<span class="chip ' + (cls || '') + '">' + esc(t) + '</span>'; }

  function renderIndex(items, type) {
    var grid = document.querySelector('.cards'); if (!grid) return;
    grid.innerHTML = items.map(function (it) {
      if (type === 'busts') {
        return '<a class="card" href="/busts/' + it.slug + '/"><div class="meta">' +
          (it.confirmed ? chip('CONFIRMED', 'amber') : chip('PENDING VERIFICATION', 'red')) + chip(it.date || '') + '</div>' +
          '<h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p>' +
          '<div class="foot">' + esc(it.location || '') + ' · ' + esc(it.agency || '') + ' &rarr;</div></a>';
      }
      return '<a class="card" href="/news/' + it.slug + '/"><div class="meta">' +
        '<span class="badge-live">' + esc((it.tag || 'NEWS').toUpperCase()) + '</span>' + chip(it.date || '') + '</div>' +
        '<h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p><div class="foot">Read &rarr;</div></a>';
    }).join('');
  }

  function renderDetail(it, type) {
    if (!it) return;
    var h1 = document.querySelector('article h1'); if (h1) h1.textContent = it.title || h1.textContent;
    var byline = document.querySelector('.byline');
    if (byline) byline.innerHTML =
      (it.date ? '<span>' + esc(it.date) + '</span>' : '') +
      (it.location ? '<span>' + esc(it.location) + '</span>' : '') +
      (it.agency ? '<span>Agency: ' + esc(it.agency) + '</span>' : '') +
      (it.sources ? '<span>Sources: ' + esc(it.sources.join(', ')) + '</span>' : '');
    var lede = document.querySelector('.lede'); if (lede && it.summary) lede.textContent = it.summary;
    if (type === 'busts') {
      var rows = document.querySelectorAll('.tbl tbody tr');
      rows.forEach(function (tr) {
        var th = tr.querySelector('th'), td = tr.querySelector('td');
        if (!th || !td) return;
        var k = th.textContent.trim();
        if (k === 'Date' && it.date) td.textContent = it.date;
        if (k === 'Location' && it.location) td.textContent = it.location;
        if (k === 'Agency' && it.agency) td.textContent = it.agency;
        if (/Sentencing/.test(k) && it.sentencing) td.textContent = it.sentencing;
      });
      var ps = document.querySelectorAll('article p');
      for (var i = 0; i < ps.length; i++) {
        if (ps[i].classList.contains('lede')) continue;
        if (ps[i].querySelector('b') && /Source:/.test(ps[i].textContent)) continue;
        ps[i].textContent = it.summary || ps[i].textContent; break;
      }
    }
    if (type === 'news' && Array.isArray(it.body) && it.body.length) {
      var article = document.querySelector('article.article');
      var olds = article.querySelectorAll('p:not(.lede)');
      var html = it.body.map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('');
      olds.forEach(function (p) { p.remove(); });
      var rel = article.querySelector('.related');
      if (rel) rel.insertAdjacentHTML('beforebegin', html); else article.insertAdjacentHTML('beforeend', html);
    }
    var badge = document.querySelector('article .kicker');
    if (badge && type === 'busts') badge.textContent = it.confirmed ? 'CONFIRMED' : 'PENDING VERIFICATION';
  }
})();
