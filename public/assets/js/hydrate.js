/* hydrate.js — live-load admin (KV) content over static HTML.
   Static pages remain the SEO base; admin edits appear instantly. Covers:
   drugs, busts, news, topics, quit, hotlines, pharmacies, rehabs, sentencing. */
(function () {
  var seg = location.pathname.split('/').filter(Boolean);
  if (seg.length === 0) { renderHome(); return; }
  var type = seg[0] || '';
  if (!/^(drugs|busts|news|topics|quit|hotlines|pharmacies|rehabs|sentencing|categories|vs|mix)$/.test(type)) return;
  if (seg.length === 2) { fetch('/api/view', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({type: type, slug: seg[1]})}).catch(function(){}); }
  fetch('/api/public/content?type=' + (type === 'categories' ? 'drugs' : type)).then(function (r) { return r.json(); }).then(function (d) {
    var all = (d.items || []);
    if (seg.length === 2 && type !== 'categories') {
      var hit = all.find(function (x) { return x && x.slug === seg[1]; });
      if (hit && hit.unpublished) return renderGone();
    }
    var items = all.filter(function (x) { return x && !x.unpublished; });
    if (type === 'categories') return renderCategory(items, seg);
    if (!items.length) return;
    if (type === 'hotlines') return renderHotlines(items);
    if (type === 'sentencing') return renderSentencing(items);
    if (seg.length === 1 || (type === 'sentencing')) return renderIndex(items, type);
    var it = items.find(function (x) { return x.slug === seg[1]; });
    if (!it) return;
    if (type === 'drugs') return renderDrug(it);
    if (type === 'mix') return renderMix(it);
    if (type === 'vs') return renderVs(it);
    if (type === 'busts' || type === 'news') return renderDetail(it, type);
    if (type === 'topics') return renderTopic(it);
    if (type === 'quit') return renderQuit(it);
    if (type === 'pharmacies' || type === 'rehabs') return renderCenter(it);
  }).catch(function () {});

  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function mdRender(x) {
    if (typeof MD !== 'undefined' && MD && MD.render) return MD.render(x);
    return String(x || '').split(/\n{2,}/).map(function (p) { return '<p>' + esc(p).replace(/\n/g, '<br>') + '</p>'; }).join('');
  }
  function renderGone() {
    var m = document.querySelector('main'); if (!m) return;
    m.innerHTML = '<div class="wrap"><div class="panel" style="max-width:620px;margin:48px auto;padding:34px;text-align:center">' +
      '<span class="kicker" style="background:#dc2626;color:#fff;border:0">410 &mdash; GONE</span>' +
      '<h1 style="margin-top:12px">This page has been taken offline</h1>' +
      '<p>This content was unpublished by the editors and is no longer available. ' +
      'Browse the <a href="/categories/opioids/">drug library</a> or go <a href="/">back to home</a>.</p></div></div>';
    document.title = 'Page offline | plugreports';
    var rob = document.querySelector('meta[name="robots"]');
    if (!rob) { rob = document.createElement('meta'); rob.name = 'robots'; document.head.appendChild(rob); }
    rob.setAttribute('content', 'noindex');
  }
  function chipEntry(entry) {
    var e2 = String(entry);
    var pipe = e2.split('|');
    var target = pipe[0].trim(), custom = (pipe[1] || '').trim();
    if (/^https?:\/\//.test(target)) {
      var elab = custom || target.replace(/^https?:\/\//, '').split('/')[0];
      return '<a href="' + esc(target) + '" target="_blank" rel="noopener"><span class="mini" style="background:#667085">&#8599;</span><span>' + esc(elab) + '</span></a>';
    }
    var p = target.split(':');
    var SECTIONS = ['busts','news','drugs','topics','quit','categories','hotlines','pharmacies','rehabs','sentencing','mix','suggest','about'];
    var href = '/' + (p.length > 1 ? p[0] + '/' + p[1] : (SECTIONS.indexOf(target) > -1 ? target : 'drugs/' + entry)) + '/';
    var lbl = custom || (p.length > 1 ? p[1] : target).replace(/-/g, ' ');
    return '<a href="' + href + '"><span class="mini" style="background:#d97706">' + esc((lbl[0] || '?').toUpperCase()) + '</span><span>' + esc(lbl) + '</span></a>';
  }
function _bShow(box, slides, dots, i) {
  _bIdx = (i + slides.length) % slides.length;
  slides.forEach(function (sl, j) { sl.classList.toggle('on', j === _bIdx); });
  dots.forEach(function (d, j) { d.classList.toggle('on', j === _bIdx); });
}
function _bAuto(box, slides, dots) { clearInterval(_bTimer); _bTimer = setInterval(function () { _bShow(box, slides, dots, _bIdx + 1); }, 6000); }
var _bTimer = null, _bIdx = 0;
function initBreaking() {
  var box = document.getElementById('breaking'); if (!box) return;
  var slides = box.querySelectorAll('.b-slide'); if (!slides.length) return;
  var dots = box.querySelectorAll('.b-dot');
  box.querySelectorAll('.b-dot').forEach(function (d) { d.onclick = function () { _bShow(box, slides, dots, +d.getAttribute('data-i')); _bAuto(box, slides, dots); }; });
  var pv = box.querySelector('.b-prev'), nx = box.querySelector('.b-next');
  if (pv) pv.onclick = function () { _bShow(box, slides, dots, _bIdx - 1); _bAuto(box, slides, dots); };
  if (nx) nx.onclick = function () { _bShow(box, slides, dots, _bIdx + 1); _bAuto(box, slides, dots); };
  box.onmouseenter = function () { clearInterval(_bTimer); };
  box.onmouseleave = function () { _bAuto(box, slides, dots); };
  _bShow(box, slides, dots, 0); _bAuto(box, slides, dots);
}

  function chip(t, cls) { return '<span class="chip ' + (cls || '') + '">' + esc(t) + '</span>'; }

  /* ---------------- index pages ---------------- */
  function renderIndex(items, type) {
    if (type === 'pharmacies' || type === 'rehabs') {
      var dir = document.querySelector('.dir-grid'); if (!dir) return;
      dir.innerHTML = items.map(function (it) {
        return '<a class="card" href="/' + type + '/' + it.slug + '/">' +
          '<div class="thumb" style="height:110px;background:linear-gradient(135deg,#fef3c7,#fee2e2);display:grid;place-items:center;font-size:34px">' +
          (type === 'pharmacies' ? '&#128138;' : '&#10010;') + '</div>' +
          '<h3>' + esc(it.name) + '</h3><p>' + esc((it.desc || '').slice(0, 120)) + '&hellip;</p>' +
          '<div class="foot">' + esc(it.region || '') + ' &rarr;</div></a>';
      }).join('');
      return;
    }
    if (type === 'mix') {
      var LV = {deadly: 'DEADLY COMBINATION', dangerous: 'DANGEROUS COMBINATION', caution: 'USE WITH CAUTION'};
      ['deadly', 'dangerous', 'caution'].forEach(function (tier) {
        var tgrid = document.querySelector('[data-tier="' + tier + '"]'); if (!tgrid) return;
        tgrid.innerHTML = items.filter(function (x) { return (x.level || 'caution') === tier; }).map(function (it) {
          return '<a class="card" href="/mix/' + it.slug + '/"><div class="meta">' +
            chip(LV[it.level] || LV.caution, it.level === 'deadly' ? 'red' : it.level === 'dangerous' ? 'amber' : '') + '</div>' +
            '<h3>' + esc(it.a || '') + ' + ' + esc(it.b || '') + '</h3><p>' + esc((it.summary || '').slice(0, 140)) + '</p>' +
            '<div class="foot">Why it&rsquo;s dangerous &rarr;</div></a>';
        }).join('');
      });
      return;
    }
    if (type === 'vs') {
      var pairCard = function (it) {
        return '<a class="card vs-card" href="/vs/' + it.slug + '/">' +
          '<div class="vs-duo"><span class="vs-dot" style="background:#0f766e">' + esc((it.a || '?')[0]) + '</span>' +
          '<span class="vs-x">vs</span>' +
          '<span class="vs-dot" style="background:#d97706">' + esc((it.b || '?')[0]) + '</span></div>' +
          '<h3>' + esc(it.title || '') + '</h3><p>' + esc((it.intro || '').slice(0, 120)) + '</p>' +
          '<div class="foot">See the comparison &rarr;</div></a>';
      };
      var seenCat = {};
      document.querySelectorAll('.vs-group').forEach(function (sec) {
        var key = sec.id;
        var mine = items.filter(function (x) { return (x.cat || '') === key; });
        if (!mine.length) return;
        seenCat[key] = 1;
        var g = sec.querySelector('.cards'); if (!g) return;
        g.innerHTML = mine.map(pairCard).join('');
      });
      var fresh = items.filter(function (x) { return x.cat && !seenCat[x.cat]; });
      if (!fresh.length) return;
      var host = document.querySelector('main .wrap') || document.querySelector('main');
      if (!host) return;
      var byCat = {};
      fresh.forEach(function (x) { (byCat[x.cat] = byCat[x.cat] || []).push(x); });
      Object.keys(byCat).forEach(function (key) {
        host.insertAdjacentHTML('beforeend', '<section class="vs-group" id="' + esc(key) + '"><h2>' + esc(key) + '</h2>' +
          '<div class="cards">' + byCat[key].map(pairCard).join('') + '</div></section>');
      });
      return;
    }
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

  function setTicksAfter(panel, re, arr) {
    if (!panel || !Array.isArray(arr) || !arr.length) return;
    var hs = panel.querySelectorAll('h2');
    for (var i = 0; i < hs.length; i++) {
      if (!re.test(hs[i].textContent)) continue;
      var ul = hs[i].nextElementSibling;
      while (ul && ul.tagName !== 'UL') ul = ul.nextElementSibling;
      if (ul) ul.innerHTML = arr.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
      return;
    }
  }
  function renderDrug(it) {
    var im = document.querySelector('img.pimg');
    var ph = document.querySelector('.pimg-formula');
    if (im && it.image) im.src = it.image;
    else if (!im && ph && it.image) {
      // static page had no photo (formula placeholder) but KV now has one — swap it in
      var ni = document.createElement('img');
      ni.className = 'pimg';
      ni.src = it.image;
      ni.alt = (it.name || '') + (it.appearance ? ' — ' + it.appearance : '');
      ni.width = 510; ni.height = 383;
      ni.setAttribute('style', 'border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow);object-fit:cover;max-height:340px');
      ni.loading = 'lazy';
      ph.parentNode.replaceChild(ni, ph);
    }
    setH1(it.name);
    if (it.seoTitle) document.title = it.seoTitle;
    if (it.seoDesc) { var m = document.querySelector('meta[name="description"]'); if (m) m.setAttribute('content', it.seoDesc); }
    var al = document.querySelector('.phead .alias b') || document.querySelector('.alias b');
    if (al && Array.isArray(it.aliases) && it.aliases.length) al.textContent = it.aliases.join(', ');
    var panels = document.querySelectorAll('.profile-grid .panel');
    setTicksAfter(panels[0], /What it does/i, it.effects);
    setTicksAfter(panels[0], /Key risks/i, it.risks);
    setTicksAfter(panels[0], /Overdose signs/i, it.overdoseSigns);
    var fp = panels[1];
    if (fp) {
      fp.querySelectorAll('.fact').forEach(function (f) {
        var b = f.querySelector('b'), v = f.querySelector('span'); if (!b || !v) return;
        var k = b.textContent.trim();
        if (k === 'Also known as' && Array.isArray(it.aliases) && it.aliases.length) v.textContent = it.aliases.join(', ');
        if (k === 'Schedule / class' && it.schedule) v.textContent = it.schedule;
        if (k === 'Appearance' && it.appearance) v.textContent = it.appearance;
        if (k === 'Street price' && it.streetPrice) v.textContent = it.streetPrice;
        if (k === 'Legal status' && it.legalStatus) v.textContent = it.legalStatus;
        if (k === 'Last updated' && it.lastUpdated) v.textContent = it.lastUpdated;
      });
      if (Array.isArray(it.sources) && it.sources.length) {
        var sc = fp.querySelector('.chip.green');
        if (sc) sc.textContent = 'Sources: ' + it.sources.join(', ');
      }
    }
    if (Array.isArray(it.brands) && it.brands.length) {
      var bh = null;
      document.querySelectorAll('h2').forEach(function (h) { if (!bh && /Brand names/i.test(h.textContent)) bh = h; });
      var bp = bh && bh.closest('.panel');
      var tr = bp && bp.querySelector('.tagrow');
      if (tr) tr.innerHTML = it.brands.map(function (b) { return '<span class="chip">' + esc(b) + '</span>'; }).join('');
    }
    if (it.related && it.related.length) {
      var rg = document.querySelector('.related .rel-grid');
      if (rg) {
        rg.innerHTML = it.related.map(chipEntry).join('') + (it.relatedNoDefaults ? '' :
        '<a href="/topics/fentanyl-numbers/"><span class="mini" style="background:#b45309">&#128218;</span><span>Fentanyl: the numbers</span></a>' +
        '<a href="/quit/"><span class="mini" style="background:#16a34a">&#8987;</span><span>Quitting — day by day</span></a>' +
        '<a href="/pharmacies/"><span class="mini" style="background:#3b82f6">Rx</span><span>Verified pharmacies</span></a>' +
        '<a href="/hotlines/"><span class="mini" style="background:#dc2626">&#128222;</span><span>Hotlines</span></a>');
        var seen = {}, dup = [];
        Array.prototype.forEach.call(rg.querySelectorAll('a[href]'), function(a) {
          if (seen[a.getAttribute('href')]) dup.push(a); else seen[a.getAttribute('href')] = 1;
        });
        dup.forEach(function(a) { a.parentNode.removeChild(a); });
      }
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
      var html2 = mdRender(it.markdown);
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
    body.innerHTML = (it.markdown ? mdRender(it.markdown) : renderBlocks(it.blocks)) +
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

  function renderMix(it) {
    setH1(it.title);
    if (it.seoTitle) document.title = it.seoTitle;
    if (it.seoDesc) { var m = document.querySelector('meta[name="description"]'); if (m) m.setAttribute('content', it.seoDesc); }
    var q = function (k) { return document.querySelector('[data-mix="' + k + '"]'); };
    var LV = {deadly: 'DEADLY COMBINATION', dangerous: 'DANGEROUS COMBINATION', caution: 'USE WITH CAUTION'};
    var badge = q('badge');
    if (badge && it.level) {
      badge.textContent = LV[it.level] || String(it.level).toUpperCase();
      badge.className = 'chip lvl-badge ' + (it.level === 'deadly' ? 'red' : it.level === 'dangerous' ? 'amber' : '');
    }
    var s = q('summary'); if (s && it.summary) s.textContent = it.summary;
    var mech = q('mechanism'); if (mech && it.mechanism) mech.textContent = it.mechanism;
    var fill = function (k, arr) {
      var el = q(k);
      if (el && Array.isArray(arr) && arr.length) el.innerHTML = arr.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
    };
    fill('effects', it.effects); fill('signs', it.signs); fill('whatToDo', it.whatToDo);
    var up = q('updated'); if (up && it.lastUpdated) up.textContent = 'Updated ' + it.lastUpdated;
    var so = q('sources'); if (so && it.sources) so.textContent = 'Sources: ' + it.sources;
  }

  function renderVs(it) {
    setH1(it.title);
    if (it.seoTitle) document.title = it.seoTitle;
    if (it.seoDesc) { var m = document.querySelector('meta[name="description"]'); if (m) m.setAttribute('content', it.seoDesc); }
    var q = function (k) { return document.querySelector('[data-vs="' + k + '"]'); };
    var up = q('updated'); if (up && it.lastUpdated) up.textContent = 'Updated ' + it.lastUpdated;
    var so = q('sources'); if (so && Array.isArray(it.sources)) so.textContent = 'Sources: ' + it.sources.join(', ');
    var in_ = q('intro'); if (in_ && it.intro) in_.textContent = it.intro;
    var vd = q('verdict'); if (vd && it.verdict) vd.textContent = it.verdict;
    var tb = document.querySelector('table.vs-table tbody');
    if (tb && Array.isArray(it.rows) && it.rows.length) {
      tb.innerHTML = it.rows.map(function (r) {
        return '<tr><th scope="row">' + esc(r[0]) + '</th><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td></tr>';
      }).join('');
    }
    var ths = document.querySelectorAll('table.vs-table thead th');
    if (ths.length === 3) { if (it.a && ths[1]) ths[1].textContent = it.a; if (it.b && ths[2]) ths[2].textContent = it.b; }
    var sides = document.querySelectorAll('.vs-side .vs-name');
    if (sides.length === 2) { if (it.a && sides[0]) sides[0].textContent = it.a; if (it.b && sides[1]) sides[1].textContent = it.b; }
    var imgs = document.querySelectorAll('.vs-hero .vs-img');
    if (imgs.length === 2) {
      if (it.aImg) { var ia = imgs[0]; if (ia.tagName === 'IMG') ia.src = it.aImg; }
      if (it.bImg) { var ib = imgs[1]; if (ib.tagName === 'IMG') ib.src = it.bImg; }
    }
    var rg = q('related');
    if (rg && Array.isArray(it.related) && it.related.length) {
      rg.innerHTML = '<a href="/vs/"><span class="mini" style="background:#0f766e">&#8646;</span><span>All comparisons</span></a>' +
        it.related.map(chipEntry).join('');
      var seen = {}, dup = [];
      Array.prototype.forEach.call(rg.querySelectorAll('a[href]'), function(a) {
        if (seen[a.getAttribute('href')]) dup.push(a); else seen[a.getAttribute('href')] = 1;
      });
      dup.forEach(function(a) { a.parentNode.removeChild(a); });
    }
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
    var apply = function (cat) {
      if (cat && cat.unpublished) return renderGone();
      if (cat) {
        var hero = document.querySelector('.cat-hero');
        if (hero) {
          if (cat.grad || cat.color) hero.style.background = cat.grad || cat.color;
          var h1 = hero.querySelector('h1'); if (h1 && cat.name) h1.textContent = cat.name;
          var p = hero.querySelector('p');
          var txt = ((cat.tagline || '') + ' ' + (cat.blurb || '')).trim();
          if (p && txt) p.textContent = txt;
        }
        if (cat.name) document.title = cat.name + ' | plugreports';
      }
      var grid = document.querySelector('.cards'); if (!grid) return;
      var mine = items.filter(function (x) { return x.category === seg[1]; });
      if (!mine.length) return;
      grid.innerHTML = mine.map(function (d) {
        return '<a class="card" href="/drugs/' + d.slug + '/"><div class="meta"><span class="chip">' +
          esc((d.schedule || '').split('(')[0].trim().slice(0, 24)) + '</span></div><h3>' + esc(d.name) +
          '</h3><p>' + esc(d.appearance || '') + '</p><div class="foot">Effects &amp; risks &rarr;</div></a>';
      }).join('');
    };
    if (!seg[1]) return apply(null);
    fetch('/api/public/content?type=categories').then(function (r) { return r.json(); }).then(function (cd) {
      apply((cd.items || []).find(function (x) { return x && x.slug === seg[1]; }) || null);
    }).catch(function () { apply(null); });
  }

  /* ---------------- directory-style pages ---------------- */
  function insertSection(host, html) {
    if (!host) return;
    var rel = null;
    for (var i = 0; i < host.children.length; i++) {
      if (host.children[i].classList && host.children[i].classList.contains('related')) { rel = host.children[i]; break; }
    }
    if (rel) rel.insertAdjacentHTML('beforebegin', html); else host.insertAdjacentHTML('beforeend', html);
  }
  function hlCards(list) {
    return (list || []).map(function (h) {
      return '<div class="hl-card"><h3>' + esc(h[1]) + '</h3><div class="num">' + esc(h[0]) + '</div>' +
        '<div class="who">' + esc(h[2]) + '</div>' +
        (h[3] ? '<a class="call-btn" href="tel:' + esc(h[3]) + '">&#128222; Call now</a>' : '<span class="chip" style="margin-top:12px">Text-based service</span>') + '</div>';
    }).join('');
  }
  function renderHotlines(items) {
    var seen = {};
    var secs = document.querySelectorAll('.hl-region');
    secs.forEach(function (sec) {
      var k = sec.querySelector('.kicker'); if (!k) return;
      var it = items.find(function (x) { return x.region === k.textContent.trim(); });
      if (!it) return;
      seen[it.region] = 1;
      var grid = sec.querySelector('.hl-grid'); if (!grid) return;
      grid.innerHTML = hlCards(it.items);
    });
    var fresh = items.filter(function (x) { return x && x.region && !seen[x.region] && Array.isArray(x.items) && x.items.length; });
    if (!fresh.length) return;
    var host = secs.length ? secs[secs.length - 1].parentNode : (document.querySelector('main .wrap') || document.querySelector('main'));
    fresh.forEach(function (it) {
      insertSection(host, '<section class="hl-region"><span class="kicker amber">' + esc(it.region) + '</span>' +
        '<div class="hl-grid">' + hlCards(it.items) + '</div></section>');
    });
  }

  function legalRows(table) {
    return table.slice(1).map(function (r) {
      return '<tr>' + r.map(function (c, i) { return (i === 0 ? '<th style="width:45%">' : '<td>') + esc(c) + (i === 0 ? '</th>' : '</td>'); }).join('') + '</tr>';
    }).join('');
  }
  function renderSentencing(items) {
    var seen = {};
    var docs = document.querySelectorAll('.legal-doc');
    docs.forEach(function (doc) {
      var h = doc.querySelector('h2'); if (!h) return;
      var it = items.filter(function (x) { return x.region === h.textContent.trim() && Array.isArray(x.table); })[0] || items.find(function (x) { return x.region === h.textContent.trim(); });
      if (!it) return;
      seen[it.region] = 1;
      var p = doc.querySelector('p'); if (p && it.summary) p.textContent = it.summary;
      var tb = doc.querySelector('.tbl tbody'); if (tb && Array.isArray(it.table)) tb.innerHTML = legalRows(it.table);
    });
    var fresh = items.filter(function (x) { return x && x.region && !seen[x.region]; });
    if (!fresh.length) return;
    var host = docs.length ? docs[docs.length - 1].parentNode : (document.querySelector('main .wrap') || document.querySelector('main'));
    fresh.forEach(function (it) {
      var tbl = (Array.isArray(it.table) && it.table.length) ? '<table class="tbl"><thead><tr>' +
        it.table[0].map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>' +
        legalRows(it.table) + '</tbody></table>' : '';
      insertSection(host, '<div class="legal-doc" style="margin-bottom:22px"><span class="seal">INFO<br>ONLY</span>' +
        '<h2 style="margin-top:0">' + esc(it.region) + '</h2>' +
        (it.summary ? '<p style="color:#667085">' + esc(it.summary) + '</p>' : '') + tbl + '</div>');
    });
    var relEntries = [];
    items.forEach(function (x) {
      (x.related || []).forEach(function (r) { if (relEntries.indexOf(r) < 0) relEntries.push(r); });
    });
    var relGrid = document.querySelector('[data-sent-rel]');
    if (relGrid && relEntries.length) relGrid.innerHTML = relEntries.map(chipEntry).join('');
  }
})();

  /* ---------------- home page ---------------- */
  var CATCOL = {opioids:'#dc2626', stimulants:'#d97706', benzodiazepines:'#7c3aed', sedatives:'#0f766e',
    depressants:'#1d4ed8', dissociatives:'#0891b2', empathogens:'#be185d', psychedelics:'#4d7c0f',
    cannabinoids:'#57534e', performance:'#b45309', hazardous:'#111827'};
  function renderHome() {
    Promise.all(['news', 'busts', 'topics', 'quit', 'hotlines', 'drugs', 'categories', 'settings'].map(function (t) {
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
      var settings = (res[7] && res[7].items && res[7].items[0]) || {};
      var bslot = document.getElementById('breaking');
      if (bslot && (settings.breakingEnabled === false || settings.breakingEnabled === 'false')) { bslot.style.display = 'none'; }
      else if (bslot) {
        bslot.style.display = '';
        var pick = settings.breakingSlug ? news.filter(function (x) { return x.slug === settings.breakingSlug; })[0] : null;
        var pool2 = news.concat(busts || []);
        var alerts = (pick ? [pick] : pool2.filter(function (x) { return x.tag === 'Alert'; }).sort(function (a, b) { return String(b.date || '').localeCompare(String(a.date || '')); }).slice(0, 5)) || [];
        if (!alerts.length) alerts = news.slice(0, 1);
        var slidesHtml = alerts.map(function (al, i) {
          return '<div class="b-slide' + (i === 0 ? ' on' : '') + '">' +
            (al.image ? '<img src="' + esc(al.image) + '" alt="">' : '') +
            '<div><div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">' +
            (al.country ? '<span class="b-country">&#127760; ' + esc(al.country) + '</span>' : '') +
            '<span class="b-date">' + esc(al.date || '') + '</span></div>' +
            '<h2>' + esc(al.title) + '</h2><p>' + esc((al.summary || '').slice(0, 170)) + '&hellip;</p>' +
            '<a class="btn btn-red" href="/news/' + al.slug + '/">Read the full story &rarr;</a></div></div>';
        }).join('');
        var dotsHtml = alerts.map(function (al, i) { return '<button class="b-dot' + (i === 0 ? ' on' : '') + '" data-i="' + i + '" aria-label="Slide ' + (i + 1) + '"></button>'; }).join('');
        bslot.innerHTML = '<div class="wrap"><div class="b-top"><span class="b-chip">&#9889; BREAKING</span><div class="b-dots">' + dotsHtml + '</div></div>' +
          '<div class="b-slides">' + slidesHtml + '</div>' +
          '<button class="b-arrow b-prev" aria-label="Previous">&#8249;</button>' +
          '<button class="b-arrow b-next" aria-label="Next">&#8250;</button></div>';
        if (typeof initBreaking === 'function') initBreaking();
      }
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
      var SORT = {news: 'latest', busts: 'latest', topics: 'latest', important: 'latest'};
      function order(items, sel) {
        if (SORT[sel] === 'trending') return items.slice().sort(function (a, b) { return (b.views || 0) - (a.views || 0); });
        return items.slice().sort(function (a, b) { return String(b.date || '').localeCompare(String(a.date || '')); });
      }
      function pane(sel, items, cardFn) {
        var p = document.querySelector('.tab-pane[data-pane="' + sel + '"] .cards');
        if (p && items.length) p.innerHTML = order(items, sel).map(cardFn).join('');
      }
      document.querySelectorAll('.sortrow').forEach(function (row) {
        row.addEventListener('click', function (e) {
          var b = e.target.closest('.spill'); if (!b) return;
          SORT[row.dataset.sort] = b.dataset.order;
          row.querySelectorAll('.spill').forEach(function (x) { x.classList.toggle('on', x === b); });
          if (row.dataset.sort === 'news') pane('news', news, newsCard);
          if (row.dataset.sort === 'busts') pane('busts', busts, bustCard);
          if (row.dataset.sort === 'topics') pane('topics', topics, topicCard);
          if (row.dataset.sort === 'important') pane('important', topics.filter(function (t) { return t.tag === 'Important' || (t.slug || '').indexOf('nasal-spray') > -1; }), topicCard);
        });
      });
      function newsCard(it) {
        return '<a class="card" href="/news/' + it.slug + '/">' + (it.image ? '<div class="thumb"><img src="' + esc(it.image) + '" loading="lazy"></div>' : '') + '<div class="meta"><span class="badge-live">' + esc((it.tag || 'NEWS').toUpperCase()) + '</span>' + chip(it.date || '') + '</div><h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p><div class="foot">Read &rarr;</div></a>'; }
      pane('news', news, newsCard);
      function bustCard(it) {
        return '<a class="card" href="/busts/' + it.slug + '/">' + (it.image ? '<div class="thumb"><img src="' + esc(it.image) + '" loading="lazy"></div>' : '') + '<div class="meta">' + (it.confirmed ? chip('CONFIRMED', 'amber') : chip('PENDING VERIFICATION', 'red')) + chip(it.date || '') + '</div><h3>' + esc(it.title) + '</h3><p>' + esc(it.summary || '') + '</p><div class="foot">' + esc(it.location || '') + ' · ' + esc(it.agency || '') + ' &rarr;</div></a>'; }
      pane('busts', busts, bustCard);
      function topicCard(it) {
        return '<a class="card" href="/topics/' + it.slug + '/">' + (it.image ? '<div class="thumb"><img src="' + esc(it.image) + '" loading="lazy"></div>' : '') + '<div class="meta">' + chip('GUIDE', 'red') + chip(it.read || '') + chip(it.date || '') + '</div><h3>' + esc(it.title) + '</h3><p>' + esc(it.desc || '') + '</p><div class="foot">Read guide &rarr;</div></a>'; }
      var important = topics.filter(function (t) { return t.tag === 'Important' || (t.slug || '').indexOf('nasal-spray') > -1; });
      function importantCard(it) { return topicCard(it); }
      pane('important', important, importantCard);
      pane('topics', topics, topicCard);
    }).catch(function () {});
  }

