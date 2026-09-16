/* hydrate.js — live-load admin (KV) content over static HTML.
   Static pages remain the SEO base; admin edits appear instantly. Covers:
   drugs, busts, news, topics, quit, hotlines, pharmacies, rehabs, sentencing. */
(function () {
  var seg = location.pathname.split('/').filter(Boolean);
  if (seg.length === 0) { renderHome(); return; }
  var type = seg[0] || '';
  if (!/^(drugs|busts|news|topics|quit|hotlines|pharmacies|rehabs|sentencing|categories)$/.test(type)) return;
  fetch('/api/public/content?type=' + (type === 'categories' ? 'drugs' : type)).then(function (r) { return r.json(); }).then(function (d) {
    var items = (d.items || []).filter(function (x) { return x && !x.unpublished; });
    if (!items.length) return;
    if (type === 'categories') return renderCategory(items, seg);
    if (type === 'hotlines') return renderHotlines(items);
    if (type === 'sentencing') return renderSentencing(items);
    if (seg.length === 1 || (type === 'sentencing')) return renderIndex(items, type);
    var it = items.find(function (x) { return x.slug === seg[1]; });
    if (!it) return;
    if (type === 'drugs') return renderDrug(it);
    if (type === 'busts' || type === 'news') return renderDetail(it, type);
    if (type === 'topics') return renderTopic(it);
    if (type === 'quit') return renderQuit(it);
    if (type === 'pharmacies' || type === 'rehabs') return renderCenter(it);
  }).catch(function () {});

  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function chipEntry(entry) {
    var p = String(entry).split(':');
    var href = '/' + (p.length > 1 ? p[0] + '/' + p[1] : 'drugs/' + entry) + '/';
    var lbl = (p.length > 1 ? p[1] : entry).replace(/-/g, ' ');
    return '<a href="' + href + '"><span class="mini" style="background:#d97706">' + esc((lbl[0] || '?').toUpperCase()) + '</span><span>' + esc(lbl) + '</span></a>';
  }
  function chip(t, cls) { return '<span class="chip ' + (cls || '') + '">' + esc(t) + '</span>'; }

  /* ---------------- index pages ---------------- */
  function renderIndex(items, type) {
    var grid = document.querySelector('.cards'); if (!grid) return;
    grid.innerHTML = items.map(function (it) {
      if (type === 'busts') return '<a class="card" href="/busts/' + it.slug + '/"><div class="meta">' +
        (it.confirmed ? chip('CONFIRMED', 'amber') : chip('PENDING VERIFICATION', 'red')) + chip(it.date || '') + '</div>' +
        '<h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p>' +
        '<div class="foot">' + esc(it.location || '') + ' &middot; ' + esc(it.agency || '') + ' &rarr;</div></a>';
      if (type === 'news') return '<a class="card" href="/news/' + it.slug + '/"><div class="meta">' +
        '<span class="badge-live">' + esc((it.tag || 'NEWS').toUpperCase()) + '</span>' + chip(it.date || '') + '</div>' +
        '<h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p><div class="foot">Read &rarr;</div></a>';
      if (type === 'topics') return '<a class="card" href="/topics/' + it.slug + '/"><div class="meta">' +
        chip('GUIDE', 'red') + chip(it.read || '') + chip(it.date || '') + '</div><h3>' + esc(it.title) + '</h3>' +
        '<p>' + esc(it.desc || '') + '</p><div class="foot">Read guide &rarr;</div></a>';
      if (type === 'quit') return '<a class="card" href="/quit/' + it.slug + '/"><div class="meta">' +
        chip('DAY-BY-DAY', 'green') + chip(it.cat || '') + '</div><h3>Quitting ' + esc(it.name) + '</h3>' +
        '<p>' + esc((it.danger || '').slice(0, 130)) + '&hellip;</p><div class="foot">Full timeline &rarr;</div></a>';
      return '';
    }).join('');
  }

  /* ---------------- detail pages ---------------- */
  function setH1(t) { var h = document.querySelector('h1'); if (h && t) h.textContent = t; }
  function setDetailImage(src) {
    var img = document.querySelector('article .detail-img');
    if (!img) {
      var h1 = document.querySelector('article h1') || document.querySelector('h1');
      if (!h1) return;
      img = document.createElement('img');
      img.className = 'detail-img'; img.loading = 'lazy';
      h1.parentNode.insertBefore(img, h1.nextSibling);
    }
    img.src = src;
  }

  function renderDrug(it) {
    var im = document.querySelector('img[loading="lazy"]');
    if (im && it.image) im.src = it.image;
    setH1(it.name);
    if (it.seoTitle) document.title = it.seoTitle;
    if (it.seoDesc) { var m = document.querySelector('meta[name="description"]'); if (m) m.setAttribute('content', it.seoDesc); }
    if (it.related && it.related.length) {
      var rg = document.querySelector('.related .rel-grid');
      if (rg) rg.innerHTML = it.related.map(chipEntry).join('') +
        '<a href="/topics/fentanyl-numbers/"><span class="mini" style="background:#b45309">&#128218;</span><span>Fentanyl: the numbers</span></a>' +
        '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>' +
        '<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a>' +
        '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines</span></a>';
    }
  }

  function renderDetail(it, type) {
    setH1(it.title);
    var byline = document.querySelector('.byline');
    if (byline) byline.innerHTML =
      (it.date ? '<span>' + esc(it.date) + '</span>' : '') +
      (it.location ? '<span>' + esc(it.location) + '</span>' : '') +
      (it.agency ? '<span>Agency: ' + esc(it.agency) + '</span>' : '') +
      (it.sources ? '<span>Sources: ' + esc(it.sources.join(', ')) + '</span>' : '');
    var lede = document.querySelector('.lede'); if (lede && it.summary) lede.textContent = it.summary;
    if (it.image) setDetailImage(it.image);
    applyHelpFooter(it);
    if (type === 'busts') {
      document.querySelectorAll('.tbl tbody tr').forEach(function (tr) {
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
        if (/Source:/.test(ps[i].textContent)) continue;
        ps[i].textContent = it.summary || ps[i].textContent; break;
      }
      var badge = document.querySelector('article .kicker');
      if (badge) badge.textContent = it.confirmed ? 'CONFIRMED' : 'PENDING VERIFICATION';
      applyHelpFooter(it);
    }
    function applyHelpFooter(it) {
      var entries = (it.related || []).concat(it.drugsInvolved || []);
      var grid = document.querySelector('article .related .rel-grid');
      if (!grid) return;
      if (!entries.length && !grid.innerHTML) return;
      grid.innerHTML = entries.map(chipEntry).join('') +
        '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines — help now</span></a>' +
        '<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Find a verified pharmacy</span></a>' +
        '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>';
    }
    if (type === 'news' && it.markdown) {
      var article2 = document.querySelector('article.article');
      var olds2 = article2.querySelectorAll('p:not(.lede)');
      var html2 = MD.render(it.markdown);
      olds2.forEach(function (p) { p.remove(); });
      var rel2 = article2.querySelector('.related');
      if (rel2) rel2.insertAdjacentHTML('beforebegin', html2); else article2.insertAdjacentHTML('beforeend', html2);
      return;
    }
    if (type === 'news' && Array.isArray(it.body) && it.body.length) {
      var article = document.querySelector('article.article');
      var olds = article.querySelectorAll('p:not(.lede)');
      var html = it.body.map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('');
      olds.forEach(function (p) { p.remove(); });
      var rel = article.querySelector('.related');
      if (rel) rel.insertAdjacentHTML('beforebegin', html); else article.insertAdjacentHTML('beforeend', html);
    }
  }

  function renderBlocks(blocks) {
    return (blocks || []).map(function (b) {
      var t = b[0];
      if (t === 'p') return '<p>' + b[1] + '</p>';
      if (t === 'h2') return '<h2>' + esc(b[1]) + '</h2>';
      if (t === 'h3') return '<h3>' + esc(b[1]) + '</h3>';
      if (t === 'ul') return '<ul>' + b[1].map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>';
      if (t === 'ol') return '<ol>' + b[1].map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ol>';
      if (t === 'quote') return '<blockquote>&ldquo;' + b[1] + '&rdquo;<br><small>&mdash; ' + esc(b[2]) + '</small></blockquote>';
      if (t === 'callout') return '<div class="callout ' + b[1][0] + '"><b>' + esc(b[1][1]) + '</b>' + b[1][2] + '</div>';
      if (t === 'stats') return '<div class="stat-grid">' + b[1].map(function (s, i) {
        return '<div class="stat' + (i === 0 ? ' red' : '') + '"><b>' + esc(s[0]) + '</b><span>' + esc(s[1]) + '</span></div>'; }).join('') + '</div>';
      if (t === 'table') return '<div class="figure"><table class="tbl"><thead><tr>' +
        b[1][0].map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>' +
        b[1].slice(1).map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
      if (t === 'checklist') return '<ul class="checklist">' + b[1].map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>';
      if (t === 'timeline') return '<div class="timeline">' + b[1].map(function (x, i) {
        return '<div class="tl-item' + (i === 1 ? ' red' : '') + '"><h4>' + esc(x[0]) + ' &mdash; ' + esc(x[1]) + '</h4><p>' + esc(x[2]) + '</p></div>'; }).join('') + '</div>';
      return '';
    }).join('');
  }

  function renderTopic(it) {
    setH1(it.title);
    var articles = document.querySelectorAll('article.article');
    var body = articles[articles.length - 1]; if (!body) return;
    if (it.image) setDetailImage(it.image);
    body.innerHTML = (it.markdown ? MD.render(it.markdown) : renderBlocks(it.blocks)) +
      '<div class="related print-hide"><h2>Drugs mentioned &amp; help</h2><div class="rel-grid">' +
      ((it.drugsInvolved || []).map(function (d) {
        return '<a href="/drugs/' + d + '/"><span class="mini" style="background:#d97706">' + esc((d[0] || '?').toUpperCase()) + '</span><span>' + esc(d.replace(/-/g, ' ')) + '</span></a>';
      }).join('')) +
      '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines — help now</span></a>' +
      '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a></div></div>';
  }

  function renderQuit(it) {
    setH1('What happens when you quit ' + it.name);
    if (it.image) setDetailImage(it.image);
    var call = document.querySelector('.callout');
    if (call && it.danger) { var b = call.querySelector('b'); call.innerHTML = (b ? '<b>' + b.textContent + '</b>' : '') + esc(it.danger); }
    var tl = document.querySelector('.timeline');
    if (tl && Array.isArray(it.days)) tl.innerHTML = it.days.map(function (x, i) {
      return '<div class="tl-item' + (i === 1 ? ' red' : '') + '"><h4>' + esc(x[0]) + ' &mdash; ' + esc(x[1]) + '</h4><p>' + esc(x[2]) + '</p></div>'; }).join('');
    var cl = document.querySelector('ul.checklist');
    if (cl && Array.isArray(it.tips)) cl.innerHTML = it.tips.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
  }

  function renderCenter(it) {
    setH1(it.name);
    var ps = document.querySelectorAll('main p');
    for (var i = 0; i < ps.length; i++) { if (ps[i].textContent.length > 60) { ps[i].textContent = it.desc; break; } }
    document.querySelectorAll('.fact').forEach(function (f) {
      var b = f.querySelector('b'), v = f.querySelector('span'); if (!b || !v) return;
      if (/Website/.test(b.textContent) && it.website) v.innerHTML = '<a href="' + esc(it.website) + '">' + esc(it.website) + '</a>';
      if (/Contact/.test(b.textContent) && it.phone) v.textContent = it.phone;
    });
  }

  function renderCategory(items, seg) {
    var grid = document.querySelector('.cards'); if (!grid) return;
    var mine = items.filter(function (x) { return x.category === seg[1]; });
    if (!mine.length) return;
    grid.innerHTML = mine.map(function (d) {
      return '<a class="card" href="/drugs/' + d.slug + '/"><div class="meta"><span class="chip">' +
        esc((d.schedule || '').split('(')[0].trim().slice(0, 24)) + '</span></div><h3>' + esc(d.name) +
        '</h3><p>' + esc(d.appearance || '') + '</p><div class="foot">Effects &amp; risks &rarr;</div></a>';
    }).join('');
  }

  /* ---------------- directory-style pages ---------------- */
  function renderHotlines(items) {
    document.querySelectorAll('.hl-region').forEach(function (sec) {
      var k = sec.querySelector('.kicker'); if (!k) return;
      var it = items.find(function (x) { return x.region === k.textContent.trim(); });
      var grid = sec.querySelector('.hl-grid'); if (!it || !grid) return;
      grid.innerHTML = it.items.map(function (h) {
        return '<div class="hl-card"><h3>' + esc(h[1]) + '</h3><div class="num">' + esc(h[0]) + '</div>' +
          '<div class="who">' + esc(h[2]) + '</div>' +
          (h[3] ? '<a class="call-btn" href="tel:' + esc(h[3]) + '">&#128222; Call now</a>' : '<span class="chip" style="margin-top:12px">Text-based service</span>') + '</div>';
      }).join('');
    });
  }

  function renderSentencing(items) {
    document.querySelectorAll('.legal-doc').forEach(function (doc) {
      var h = doc.querySelector('h2'); if (!h) return;
      var it = items.find(function (x) { return x.region === h.textContent.trim(); });
      if (!it) return;
      var p = doc.querySelector('p'); if (p && it.summary) p.textContent = it.summary;
      var tb = doc.querySelector('.tbl tbody'); if (tb && Array.isArray(it.table))
        tb.innerHTML = it.table.slice(1).map(function (r) {
          return '<tr>' + r.map(function (c, i) { return (i === 0 ? '<th style="width:45%">' : '<td>') + esc(c) + (i === 0 ? '</th>' : '</td>'); }).join('') + '</tr>';
        }).join('');
    });
  }
})();

  /* ---------------- home page ---------------- */
  var CATCOL = {opioids:'#dc2626', stimulants:'#d97706', benzodiazepines:'#7c3aed', sedatives:'#0f766e',
    depressants:'#1d4ed8', dissociatives:'#0891b2', empathogens:'#be185d', psychedelics:'#4d7c0f',
    cannabinoids:'#57534e', performance:'#b45309', hazardous:'#111827'};
  function renderHome() {
    Promise.all(['news', 'busts', 'topics', 'quit', 'hotlines', 'drugs', 'categories'].map(function (t) {
      return fetch('/api/public/content?type=' + t).then(function (r) { return r.json(); }).catch(function () { return {items: []}; });
    })).then(function (res) {
      var news = res[0].items || [], busts = res[1].items || [], topics = res[2].items || [],
          quit = res[3].items || [], hotlines = res[4].items || [], drugs = res[5].items || [],
          cats = res[6].items || [];
      var catMap = {};
      cats.forEach(function (c) { if (c.slug) catMap[c.slug] = c; });
      var hlCount = hotlines.reduce(function (n, r) { return n + ((r.items || []).length); }, 0);
      var regions = hotlines.filter(function (r) { return r.region; }).length;
      var kick = document.querySelector('.hero .kicker');
      if (kick) kick.textContent = 'Harm-reduction library · ' + drugs.length + ' substances · ' + regions + ' regions';
      var stats = document.querySelectorAll('.hero-stats .st b');
      if (stats[0] && drugs.length) stats[0].textContent = drugs.length;
      if (stats[1] && cats.length) stats[1].textContent = cats.length;
      if (stats[2] && hlCount) stats[2].textContent = hlCount + '+';
      if (stats[3]) stats[3].textContent = topics.length + quit.length;
      if (drugs.length) {
        var rail = document.querySelector('.rail');
        if (rail) rail.innerHTML = drugs.map(function (d) {
          var cat = catMap[d.category];
          var col = (cat && cat.color) || CATCOL[d.category] || '#667085';
          return '<a class="tile" href="/drugs/' + d.slug + '/">' +
            '<span class="sched">' + esc((d.schedule || '').split('(')[0].trim().slice(0, 16)) + '</span>' +
            '<span class="glyph" style="background:' + col + '">' + esc((d.name || '?')[0]) + '</span>' +
            '<h3>' + esc(d.name) + '</h3><span class="cat"><span class="cat-dot" style="background:' + col + '"></span>' + esc((cat && cat.name) || d.category || '') + '</span></a>';
        }).join('');
        window.DRUG_INDEX = drugs.map(function (d) {
          return {n: d.name, a: (d.aliases || []).slice(0, 3).join(', '), c: d.category || '', u: '/drugs/' + d.slug + '/', col: CATCOL[d.category] || '#d97706'};
        });
      }
      function pane(sel, items, cardFn) {
        var p = document.querySelector('.tab-pane[data-pane="' + sel + '"] .cards');
        if (p && items.length) p.innerHTML = items.map(cardFn).join('');
      }
      pane('news', news, function (it) {
        return '<a class="card" href="/news/' + it.slug + '/">' + (it.image ? '<div class="thumb"><img src="' + esc(it.image) + '" loading="lazy"></div>' : '') + '<div class="meta"><span class="badge-live">' + esc((it.tag || 'NEWS').toUpperCase()) + '</span>' + chip(it.date || '') + '</div><h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p><div class="foot">Read &rarr;</div></a>';
      });
      pane('busts', busts, function (it) {
        return '<a class="card" href="/busts/' + it.slug + '/">' + (it.image ? '<div class="thumb"><img src="' + esc(it.image) + '" loading="lazy"></div>' : '') + '<div class="meta">' + (it.confirmed ? chip('CONFIRMED', 'amber') : chip('PENDING VERIFICATION', 'red')) + chip(it.date || '') + '</div><h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p><div class="foot">' + esc(it.location || '') + ' · ' + esc(it.agency || '') + ' &rarr;</div></a>';
      });
      pane('topics', topics, function (it) {
        return '<a class="card" href="/topics/' + it.slug + '/">' + (it.image ? '<div class="thumb"><img src="' + esc(it.image) + '" loading="lazy"></div>' : '') + '<div class="meta">' + chip('GUIDE', 'red') + chip(it.read || '') + chip(it.date || '') + '</div><h3>' + esc(it.title) + '</h3><p>' + esc(it.desc || '') + '</p><div class="foot">Read guide &rarr;</div></a>';
      });
    }).catch(function () {});
  }
