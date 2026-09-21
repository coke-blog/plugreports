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
    cannabinoids:['Cannabinoids','#57534e'], performance:['Performance & Grey-Market Pharma','#b45309'],
    hazardous:['Hazardous Substances','#111827']};
  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function mdRender(x) {
    if (typeof MD !== 'undefined' && MD && MD.render) return MD.render(x);
    return String(x || '').split(/\n{2,}/).map(function (p) { return '<p>' + esc(p).replace(/\n/g, '<br>') + '</p>'; }).join('');
  }
  function chip(t, cls) { return '<span class="chip ' + (cls || '') + '">' + esc(t) + '</span>'; }
  function ticks(arr, cls) { return '<ul class="ticks ' + (cls || '') + '">' + (arr || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'; }

  fetch('/api/public/content?type=' + type).then(function (r) { return r.json(); }).then(function (d) {
    var box = document.getElementById('dyn');
    if (type === 'categories') {
      var cat = (d.items || []).find(function (x) { return x.slug === slug; });
      if (!cat) { box.innerHTML = '<h1>Category not found</h1><p><a href="/">Back to home</a>.</p>'; return; }
      return fetch('/api/public/content?type=drugs').then(function (r) { return r.json(); }).then(function (dd) {
        var mine = (dd.items || []).filter(function (x) { return x.category === slug; });
        box.innerHTML = '<section class="cat-hero" style="background:' + (cat.grad || cat.color || '#667085') + '">' +
          '<span class="kicker" style="background:rgba(255,255,255,.15);color:#fff;border:0">' + mine.length + ' substances</span>' +
          '<h1>' + esc(cat.name) + '</h1><p>' + esc(cat.tagline || '') + ' ' + esc(cat.blurb || '') + '</p></section>' +
          '<div class="cards">' + mine.map(function (d) {
            return '<a class="card" href="/drugs/' + d.slug + '/"><h3>' + esc(d.name) + '</h3><p>' + esc(d.appearance || '') + '</p><div class="foot">Effects &amp; risks &rarr;</div></a>';
          }).join('') + '</div>';
        document.title = (cat.name || 'Category') + ' | plugreports';
        try { window.scrollTo(0, 0); } catch (e) {}
      });
    }
    var it = (d.items || []).find(function (x) { return x.slug === slug; });
    if (!it || it.unpublished) { box.innerHTML = '<h1>' + (it ? 'This page has been taken offline' : 'Not found') + '</h1><p>This item may have been removed. <a href="/">Back to home</a>.</p>'; return; }
    document.title = (it.seoTitle || (it.name || it.title) + ' | plugreports');
    var md = it.seoDesc || it.summary || it.desc;
    if (md) { var m = document.querySelector('meta[name="description"]'); if (m) m.setAttribute('content', md); }
    if (it.markdown && (type === 'topics' || type === 'news')) {
      document.getElementById('dyn').innerHTML = '<article class="article" style="max-width:820px;margin:0 auto;padding-top:26px">' +
        (type === 'topics' ? '<span class="kicker amber">GUIDE</span>' : '<span class="kicker">' + esc(it.tag || 'NEWS') + '</span>') +
        '<h1 style="margin-top:12px">' + esc(it.title) + '</h1>' +
        '<div class="byline"><span>' + esc(it.date || '') + '</span></div>' +
        (it.image ? '<img class="detail-img" src="' + esc(it.image) + '" loading="lazy">' : '') +
        (it.desc || it.summary ? '<p class="lede">' + esc(it.desc || it.summary) + '</p>' : '') +
        mdRender(it.markdown) + '<div class="related"><h2>Drugs mentioned &amp; help</h2><div class="rel-grid">' +
      ((it.related || []).map(relChip).join('')) + ((it.drugsInvolved || []).map(function (d) { return '<a href="/drugs/' + d + '/"><span class="mini" style="background:#d97706">' + esc((d[0] || '?').toUpperCase()) + '</span><span>' + esc(d.replace(/-/g, ' ')) + '</span></a>'; }).join('')) +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines — help now</span></a></div></div>' + '</article>';
      try { window.scrollTo(0, 0); } catch (e) {} return;
    }
    var html = '';
    if (type === 'drugs') html = drugPage(it);
    else if (type === 'busts') html = bustPage(it);
    else if (type === 'news') html = newsPage(it);
    else if (type === 'topics') html = topicPage(it);
    else if (type === 'pharmacies' || type === 'rehabs') html = centerPage(it, type);
    else if (type === 'quit') html = quitPage(it);
    box.innerHTML = html;
    try { window.scrollTo(0, 0); } catch (e) {}
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
      (it.brands && it.brands.length ? '<div class="panel"><h2>Brand names on the grey market</h2><div class="tagrow">' + it.brands.map(function (b) { return '<span class="chip">' + esc(b) + '</span>'; }).join('') + '</div></div>' : '') +
      '<div class="related"><h2>You may also want to know about</h2><div class="rel-grid">' +
      ((it.related || []).map(relChip).join('')) +
      '<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a>' +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>' +
      '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a></div></div>';
  }
  function relChip(entry) {
    var e2 = String(entry);
    var pipe = e2.split('|');
    var target = pipe[0].trim(), custom = (pipe[1] || '').trim();
    if (/^https?:\/\//.test(target)) {
      var elab = custom || target.replace(/^https?:\/\//, '').split('/')[0];
      return '<a href="' + esc(target) + '" target="_blank" rel="noopener"><span class="mini" style="background:#667085">&#8599;</span><span>' + esc(elab) + '</span></a>';
    }
    var p = target.split(':');
    var href = '/' + (p.length > 1 ? p[0] + '/' + p[1] : 'drugs/' + entry) + '/';
    var lbl = custom || (p.length > 1 ? p[1] : target).replace(/-/g, ' ');
    return '<a href="' + href + '"><span class="mini" style="background:#d97706">' + esc((lbl[0] || '?').toUpperCase()) + '</span><span>' + esc(lbl) + '</span></a>';
  }
  function fact(k, v) { return '<div class="fact"><b>' + esc(k) + '</b><span>' + esc(v || '—') + '</span></div>'; }

  function bustPage(it) {
    return '<span class="kicker">' + (it.confirmed ? 'CONFIRMED' : 'PENDING VERIFICATION') + '</span>' +
      '<h1 style="margin-top:12px">' + esc(it.title) + '</h1>' +
      '<div class="byline"><span>' + esc(it.date) + '</span><span>' + esc(it.location) + '</span><span>Agency: ' + esc(it.agency) + '</span></div>' +
      (it.image ? '<img class="detail-img" src="' + esc(it.image) + '" loading="lazy">' : '') +
      '<div class="figure"><table class="tbl"><tbody>' +
      '<tr><th style="width:160px">Date</th><td>' + esc(it.date) + '</td></tr>' +
      '<tr><th>Location</th><td>' + esc(it.location) + '</td></tr>' +
      '<tr><th>Agency</th><td>' + esc(it.agency) + '</td></tr>' +
      '<tr><th>Sentencing exposure</th><td>' + esc(it.sentencing) + '</td></tr></tbody></table></div>' +
      '<p>' + esc(it.summary) + '</p>' +
      (it.sourceUrl ? '<p><b>Source:</b> <a href="' + esc(it.sourceUrl) + '" rel="nofollow noopener">' + esc(it.sourceUrl) + '</a></p>' : '') +
      '<div class="related"><h2>Drugs mentioned &amp; help</h2><div class="rel-grid">' +
      ((it.related || []).map(relChip).join('')) + ((it.drugsInvolved || []).map(function (d) { return '<a href="/drugs/' + d + '/"><span class="mini" style="background:#d97706">' + esc((d[0] || '?').toUpperCase()) + '</span><span>' + esc(d.replace(/-/g, ' ')) + '</span></a>'; }).join('')) +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines — help now</span></a></div></div>' +
      '<div class="callout amber"><b>Why busts matter for safety</b>Major seizures destabilize local supply — potency swings for weeks afterwards.</div>';
  }

  function newsPage(it) {
    return '<span class="kicker">' + esc(it.tag || 'NEWS') + '</span><h1 style="margin-top:12px">' + esc(it.title) + '</h1>' +
      '<div class="byline"><span>' + esc(it.date) + '</span><span>Sources: ' + esc((it.sources || []).join(', ')) + '</span></div>' +
      (it.image ? '<img class="detail-img" src="' + esc(it.image) + '" loading="lazy">' : '') +
      '<p class="lede">' + esc(it.summary) + '</p>' +
      (it.body || []).map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('') +
      '<div class="related"><h2>Drugs mentioned &amp; help</h2><div class="rel-grid">' +
      ((it.related || []).map(relChip).join('')) + ((it.drugsInvolved || []).map(function (d) { return '<a href="/drugs/' + d + '/"><span class="mini" style="background:#d97706">' + esc((d[0] || '?').toUpperCase()) + '</span><span>' + esc(d.replace(/-/g, ' ')) + '</span></a>'; }).join('')) +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines — help now</span></a></div></div>';
  }

  function topicPage(it) {
    return '<span class="kicker amber">GUIDE' + (it.read ? ' · ' + esc(it.read) + ' read' : '') + '</span>' +
      '<h1 style="margin-top:12px">' + esc(it.title) + '</h1>' +
      '<div class="byline"><span>Updated ' + esc(it.date || '') + '</span></div>' +
      (it.image ? '<img class="detail-img" src="' + esc(it.image) + '" loading="lazy">' : '') +
      '<p class="lede">' + esc(it.desc || '') + '</p>' +
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

  function centerPage(it, type) {
    return '<div style="max-width:760px;padding:26px 0">' +
      (it.verified ? '<span class="kicker green">&#10004; VERIFIED</span>' : '<span class="kicker">DIRECTORY</span>') +
      '<h1 style="font-size:clamp(26px,4vw,38px);margin-top:10px">' + esc(it.name) + '</h1>' +
      (it.region ? '<div class="tagrow"><span class="chip amber">' + esc(it.region) + '</span></div>' : '') +
      '<div class="thumb" style="height:180px;background:linear-gradient(135deg,#fef3c7,#fee2e2);display:grid;place-items:center;font-size:44px;border-radius:16px;margin:16px 0">' +
      (type === 'pharmacies' ? '&#128138;' : '&#10010;') + '</div>' +
      (it.desc ? '<p style="font-size:16.5px">' + esc(it.desc) + '</p>' : '') +
      (it.website ? '<div class="fact" style="margin-top:18px"><b>Website</b><span><a href="' + esc(it.website) + '" rel="noopener">' + esc(it.website) + '</a></span></div>' : '') +
      (it.phone ? '<div class="fact"' + (it.website ? '' : ' style="margin-top:18px"') + '><b>Contact</b><span>' + esc(it.phone) + '</span></div>' : '') +
      '<div class="callout green" style="margin-top:18px"><b>In crisis right now?</b>Skip the directory — call your emergency number or a <a href="/hotlines/">hotline</a> first.</div>' +
      '<div class="related print-hide"><h2>You may also want to know about</h2><div class="rel-grid">' +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>' +
      '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>' +
      '<a href="/rehabs/"><span class="mini" style="background:#16a34a">&#10010;</span><span>All rehab centers</span></a>' +
      '<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a></div></div></div>';
  }

  function mixPage(it) {
    var LV = {deadly: ['DEADLY COMBINATION', 'red', 'red'], dangerous: ['DANGEROUS COMBINATION', 'amber', 'amber'], caution: ['USE WITH CAUTION', '', 'gray']};
    var lv = LV[it.level] || LV.caution;
    function xlinks(sl) {
      if (!sl) return '';
      return '<a href="/drugs/' + esc(sl) + '/"><span class="mini" style="background:#d97706">' + esc((sl[0] || '?').toUpperCase()) + '</span><span>' + esc(sl.replace(/-/g, ' ')) + '</span></a>';
    }
    var cross = (it.aSlug || it.bSlug) ?
      '<div class="related print-hide"><h2>Full substance profiles</h2><div class="rel-grid">' + xlinks(it.aSlug) + xlinks(it.bSlug) + '</div></div>' : '';
    return '<article class="article" style="padding-top:26px">' +
      '<span class="chip lvl-badge ' + lv[1] + '" style="font-size:12px;padding:6px 14px">' + lv[0] + '</span>' +
      '<h1 style="margin-top:12px">' + esc(it.title || ((it.a || '') + ' + ' + (it.b || ''))) + '</h1>' +
      '<div class="byline"><span>Updated ' + esc(it.lastUpdated || '') + '</span><span>Sources: ' + esc(it.sources || '') + '</span></div>' +
      (it.summary ? '<div class="callout ' + lv[2] + '"><b>' + esc(it.a || '') + ' + ' + esc(it.b || '') + ': the short answer</b>' + esc(it.summary) + '</div>' : '') +
      (it.mechanism ? '<h2>Why it&rsquo;s dangerous</h2><p>' + esc(it.mechanism) + '</p>' : '') +
      (it.effects && it.effects.length ? '<h2>What happens</h2>' + ticks(it.effects) : '') +
      (it.signs && it.signs.length ? '<h2>Warning signs</h2>' + ticks(it.signs, 'red') : '') +
      (it.whatToDo && it.whatToDo.length ? '<h2>What to do</h2><ul class="checklist">' + it.whatToDo.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>' : '') +
      cross +
      '<div class="related print-hide"><h2>More mixing dangers</h2><div class="rel-grid">' +
      '<a href="/mix/"><span class="mini" style="background:#dc2626">&#9888;</span><span>All mixing dangers</span></a>' +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a></div></div></article>';
  }

  function quitPage(it) {
    return '<article class="article" style="padding-top:26px">' +
      '<span class="kicker green">DAY-BY-DAY TIMELINE</span>' +
      '<h1 style="margin-top:12px">What happens when you quit ' + esc(it.name) + '</h1>' +
      '<div class="byline"><span>Category: ' + esc(it.cat || '') + '</span></div>' +
      (it.image ? '<img class="detail-img" src="' + esc(it.image) + '" alt="" loading="lazy">' : '') +
      (it.danger ? '<div class="callout amber"><b>Read this first</b>' + esc(it.danger) + '</div>' : '') +
      '<h2>The timeline</h2>' +
      '<div class="timeline">' + (it.days || []).map(function (x, i) {
        return '<div class="tl-item' + (i === 1 ? ' red' : '') + '"><h4>' + esc(x[0]) + ' &mdash; ' + esc(x[1]) + '</h4><p>' + esc(x[2]) + '</p></div>'; }).join('') + '</div>' +
      '<h2>What actually helps</h2>' +
      '<ul class="checklist">' + (it.tips || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>' +
      '<div class="callout green"><b>The relapse rule</b>After even a week clean, your tolerance drops dramatically — an old dose can kill. If you slip: treat it like your first time, never use alone, keep naloxone close.</div>' +
      '<div class="related print-hide"><h2>You may also want to know about</h2><div class="rel-grid">' +
      ((it.related || []).map(relChip).join('')) +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#9742;</span><span>Hotlines</span></a>' +
      '<a href="/rehabs/"><span class="mini" style="background:#16a34a">&#10010;</span><span>Verified rehab centers</span></a></div></div></article>';
  }
})();
