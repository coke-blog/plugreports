/* Admin-managed video library — homepage slider + /watch/ hub.
   Clips come from KV (content:videos) via the public content API, so anything
   uploaded in /admin appears without a rebuild. The homepage slider shows only
   videos with featured=true; /watch/ shows the whole library. */
(function () {
  function escV(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  }
  async function fetchVideos() {
    try {
      const r = await fetch('/api/public/content?type=videos');
      const j = await r.json();
      return (j.items || []).filter(v => v && v.video);
    } catch (e) { return []; }
  }
  /* "drug" field accepts a library slug (cocaine), or an external resource
     * as https://url or https://url|Label — rendered as a new-tab read-more link. */
  function relLink(raw) {
    const parts = String(raw).split('|');
    const target = parts[0].trim(), custom = (parts[1] || '').trim();
    if (/^https?:\/\//.test(target)) {
      const lab = custom || target.replace(/^https?:\/\//, '').split('/')[0];
      return '<a href="' + escV(target) + '" target="_blank" rel="noopener">' + escV(lab) + ' &#8599;</a>';
    }
    if (/^[a-z]+:[\w-]+$/.test(target)) {
      const p = target.split(':');
      return '<a href="/' + escV(p[0]) + '/' + escV(p[1]) + '/">' + (custom ? escV(custom) : escV(p[1].replace(/-/g, ' '))) + ' &rarr;</a>';
    }
    return '<a href="/drugs/' + escV(target) + '/">' + (custom ? escV(custom) : 'Full ' + escV(target.replace(/-/g, ' ')) + ' profile') + ' &rarr;</a>';
  }
  function card(v) {
    const poster = v.poster ? ' poster="' + escV(v.poster) + '"' : '';
    const dur = v.duration ? '<span class="chip" style="position:absolute;bottom:8px;right:8px;background:rgba(0,0,0,.72);color:#fff;border:0;z-index:2">' + escV(v.duration) + '</span>' : '';
    const prof = v.drug ? relLink(v.drug) : '';
    return '<div class="vcard"><div class="vwrap"><video controls preload="none" playsinline' + poster +
      ' aria-label="' + escV(v.title) + '"><source src="' + escV(v.video) + '" type="video/mp4"></video>' + dur + '</div>' +
      '<h3><a href="/watch/' + escV(v.slug) + '/" style="color:inherit;text-decoration:none">' + escV(v.title) + '</a></h3>' +
      (v.desc ? '<p>' + escV(v.desc) + '</p>' : '') + prof + '</div>';
  }
  function wirePause(root) {
    root.querySelectorAll('video').forEach(v => v.addEventListener('play', () => {
      root.querySelectorAll('video').forEach(o => { if (o !== v && !o.paused) o.pause(); });
    }));
  }
  function injectLD(vids) {
    try {
      const ld = vids.map(v => ({
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": v.title, "description": v.desc || v.title,
        "thumbnailUrl": v.poster || undefined, "uploadDate": v.uploaded || undefined,
        "contentUrl": v.video, "embedUrl": location.origin + "/watch/"
      }));
      const s = document.createElement('script');
      s.type = 'application/ld+json';
      s.textContent = JSON.stringify(ld);
      document.head.appendChild(s);
    } catch (e) { }
  }
  async function slider(sec) {
    const vids = (await fetchVideos()).filter(v => v.featured);
    if (!vids.length) return; // section stays hidden until a clip is featured in /admin
    const rail = sec.querySelector('.vrail');
    rail.innerHTML = vids.map(card).join('');
    sec.hidden = false;
    wirePause(rail);
    injectLD(vids);
    const step = () => Math.max(260, Math.min(rail.clientWidth * 0.8, 360));
    const pv = sec.querySelector('.vprev'), nx = sec.querySelector('.vnext');
    if (pv) pv.onclick = () => rail.scrollBy({ left: -step(), behavior: 'smooth' });
    if (nx) nx.onclick = () => rail.scrollBy({ left: step(), behavior: 'smooth' });
  }
  async function grid(el) {
    const vids = await fetchVideos();
    el.innerHTML = vids.length ? vids.map(card).join('') :
      '<p style="color:#667085">Clips are being uploaded — check back soon.</p>';
    if (vids.length) { wirePause(el); injectLD(vids); }
  }
  document.addEventListener('DOMContentLoaded', () => {
    const s = document.getElementById('vidslider'); if (s) slider(s);
    const g = document.getElementById('watchgrid'); if (g) grid(g);
  });
})();
