/* render.js — client-side page builder for admin-created (KV-only) items.
   Served inside /_dynamic.html by Functions at /drugs|busts|news|topics/<slug>/
   when no static page exists yet. Static pages take precedence automatically. */
(function () {
  var seg = location.pathname.split('/').filter(Boolean);
  if (seg.length !== 2) return;
  var type = seg[0], slug = seg[1];
  var CATS = {opioids:['Opioids','#dc2626'], stimulants:['Stimulants','#d97706'],
    benzodiazepines:['Benzodiazepines','#7c3aed'], sedatives:['Sedatives & Hypnotics','#0f766e'],
    depressants:['GHB / GBL','#1d4ed8'], dissociatives:['Dissociatives','#0891b2'],
    empathogens:['Empathogens','#be185d'], psychedelics:['Psychedelics','#4d7c0f'],
    cannabinoids:['Synthetic Cannabinoids','#57534e'], performance:['Performance & Grey-Market Pharma','#b45309'],
    hazardous:['Hazardous Substances','#111827']};
  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function chip(t, cls) { return '<span class="chip ' + (cls || '') + '">' + esc(t) + '</span>'; }
  function ticks(arr, cls) { return '<ul class="ticks ' + (cls || '') + '">' + (arr || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'; }

  fetch('/api/public/content?type=' + type).then(function (r) { return r.json(); }).then(function (d) {
    var it = (d.items || []).find(function (x) { return x.slug === slug; });
    var box = document.getElementById('dyn');
    if (!it) { box.innerHTML = '<h1>Not found</h1><p>This item may have been removed. <a href="/">Back to home</a>.</p>'; return; }
    document.title = (it.seoTitle || (it.name || it.title) + ' | plugreports');
    var md = it.seoDesc || it.summary || it.desc;
    if (md) { var m = document.querySelector('meta[name="description"]'); if (m) m.setAttribute('content', md); }
    var html = '';
    if (type === 'drugs') html = drugPage(it);
    else if (type === 'busts') html = bustPage(it);
    else if (type === 'news') html = newsPage(it);
    else if (type === 'topics') html = topicPage(it);
    box.innerHTML = html;
    window.scrollTo(0, 0);
  }).catch(function () {
    document.getElementById('dyn').innerHTML = '<h1>Error loading content</h1><p><a href="/">Back to home</a></p>';
  });

  function drugPage(it) {
    var c = CATS[it.category] || ['Other', '#667085'];
    return '<section class="phead"><span class="glyph" style="background:' + c[1] + '">' + esc((it.name || '?')[0]) + '</span>' +
      '<div><span class="kicker" style="background:' + c[1] + ';color:#fff;border:0">' + esc(c[0]) + '</span>' +
      '<h1 style="margin-top:10px">' + esc(it.name) + '</h1>' +
      '<p class="alias">Street names: <b>' + esc((it.aliases || []).join(', ')) + '</b></p></div></section>' +
      (it.image ? '<img src="' + esc(it.image) + '" alt="' + esc(it.name) + '" style="width:100%;max-height:300px;object-fit:cover;border-radius:18px;border:1px solid #e4e7ec">' : '') +
      '<div class="callout red"><b>Overdose? Act now.</b> Call emergency services. Give naloxone for opioid-like signs. <a href="/hotlines/">Hotlines</a></div>' +
      '<div class="profile-grid"><div class="panel"><h2>What it does</h2>' + ticks(it.effects) +
      '<h2 style="margin-top:22px">Key risks</h2>' + ticks(it.risks, 'red') +
      '<h2 style="margin-top:22px">Overdose signs</h2>' + ticks(it.overdoseSigns, 'red') + '</div>' +
      '<div class="panel"><h2>Quick facts</h2>' +
      fact('Also known as', (it.aliases || []).join(', ')) + fact('Category', c[0]) +
      fact('Schedule / class', it.schedule) + fact('Appearance', it.appearance) +
      fact('Street price', it.streetPrice) + fact('Legal status', it.legalStatus) +
      fact('Last updated', it.lastUpdated) + fact('Sources', (it.sources || []).join(', ')) + '</div></div>' +
      '<div class="related"><h2>You may also want to know about</h2><div class="rel-grid">' +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>' +
      '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a></div></div>';
  }
  function fact(k, v) { return '<div class="fact"><b>' + esc(k) + '</b><span>' + esc(v || '—') + '</span></div>'; }

  function bustPage(it) {
    return '<span class="kicker">' + (it.confirmed ? 'CONFIRMED' : 'PENDING VERIFICATION') + '</span>' +
      '<h1 style="margin-top:12px">' + esc(it.title) + '</h1>' +
      '<div class="byline"><span>' + esc(it.date) + '</span><span>' + esc(it.location) + '</span><span>Agency: ' + esc(it.agency) + '</span></div>' +
      '<div class="figure"><table class="tbl"><tbody>' +
      '<tr><th style="width:160px">Date</th><td>' + esc(it.date) + '</td></tr>' +
      '<tr><th>Location</th><td>' + esc(it.location) + '</td></tr>' +
      '<tr><th>Agency</th><td>' + esc(it.agency) + '</td></tr>' +
      '<tr><th>Sentencing exposure</th><td>' + esc(it.sentencing) + '</td></tr></tbody></table></div>' +
      '<p>' + esc(it.summary) + '</p>' +
      (it.sourceUrl ? '<p><b>Source:</b> <a href="' + esc(it.sourceUrl) + '" rel="nofollow noopener">' + esc(it.sourceUrl) + '</a></p>' : '') +
      '<div class="callout amber"><b>Why busts matter for safety</b>Major seizures destabilize local supply — potency swings for weeks afterwards.</div>';
  }

  function newsPage(it) {
    return '<span class="kicker">' + esc(it.tag || 'NEWS') + '</span><h1 style="margin-top:12px">' + esc(it.title) + '</h1>' +
      '<div class="byline"><span>' + esc(it.date) + '</span><span>Sources: ' + esc((it.sources || []).join(', ')) + '</span></div>' +
      '<p class="lede">' + esc(it.summary) + '</p>' +
      (it.body || []).map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('') +
      '<div class="related"><h2>More</h2><div class="rel-grid"><a href="/news/"><span class="mini" style="background:#dc2626">N</span><span>All news</span></a></div></div>';
  }

  function topicPage(it) {
    return '<span class="kicker amber">GUIDE' + (it.read ? ' · ' + esc(it.read) + ' read' : '') + '</span>' +
      '<h1 style="margin-top:12px">' + esc(it.title) + '</h1>' +
      '<div class="byline"><span>Updated ' + esc(it.date || '') + '</span></div><p class="lede">' + esc(it.desc || '') + '</p>' +
      (it.blocks || []).map(function (b) {
        var t = b[0];
        if (t === 'p') return '<p>' + b[1] + '</p>';
        if (t === 'h2') return '<h2>' + esc(b[1]) + '</h2>';
        if (t === 'h3') return '<h3>' + esc(b[1]) + '</h3>';
        if (t === 'ul') return '<ul>' + b[1].map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>';
        if (t === 'quote') return '<blockquote>&ldquo;' + b[1] + '&rdquo;</blockquote>';
        if (t === 'callout') return '<div class="callout ' + b[1][0] + '"><b>' + esc(b[1][1]) + '</b>' + b[1][2] + '</div>';
        if (t === 'stats') return '<div class="stat-grid">' + b[1].map(function (s, i) { return '<div class="stat' + (i === 0 ? ' red' : '') + '"><b>' + esc(s[0]) + '</b><span>' + esc(s[1]) + '</span></div>'; }).join('') + '</div>';
        if (t === 'table') return '<div class="figure"><table class="tbl"><tbody>' + b[1].map(function (r, ri) {
          return '<tr>' + r.map(function (c, ci) { return (ri === 0 ? '<th>' : '<td>') + (ri === 0 ? esc(c) : c) + (ri === 0 ? '</th>' : '</td>'); }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
        if (t === 'checklist') return '<ul class="checklist">' + b[1].map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>';
        if (t === 'timeline') return '<div class="timeline">' + b[1].map(function (x, i) { return '<div class="tl-item' + (i === 1 ? ' red' : '') + '"><h4>' + esc(x[0]) + ' — ' + esc(x[1]) + '</h4><p>' + esc(x[2]) + '</p></div>'; }).join('') + '</div>';
        return '';
      }).join('');
  }
})();
