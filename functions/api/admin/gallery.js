import {checkAuth} from './_util.js';
export async function onRequestGet({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!env.CONTENT) return Response.json({ok: true, items: []});
  const q = (new URL(request.url).searchParams.get('q') || '').toLowerCase().trim();
  const listed = await env.CONTENT.list({prefix: 'media:'});
  let keys = listed.keys.map(k => k.name.replace(/^media:/, ''));
  if (q) {
    // resolve query against drug names + aliases -> slugs, then match filenames
    const drugs = JSON.parse(await env.CONTENT.get('content:drugs') || '[]');
    const slugHits = new Set();
    for (const d of drugs) {
      const fields = [d.slug, d.name, ...(d.aliases || [])].map(x => String(x).toLowerCase());
      if (fields.some(f => f.includes(q))) slugHits.add(String(d.slug).toLowerCase());
    }
    keys = keys.filter(k => {
      const base = k.toLowerCase();
      if (base.includes(q)) return true;
      if (base.replace(/\.[a-z0-9]+$/, '').replace(/[-_]/g, ' ').includes(q)) return true;
      for (const sl of slugHits) { if (base.includes(sl)) return true; }
      return false;
    });
  }
  const base = (env.MEDIA_PUBLIC_URL || '').replace(/\/$/, '');
  return Response.json({ok: true, items: keys.slice(0, 60).map(k => ({name: k, url: `${base}/media/${k}`}))});
}
