import { dynamicResponse } from '../_seo.js';
// Build-time manifest, cached in module scope (60s TTL) — avoids hitting
// ASSETS for /_static.json on every request.
let _mf = null, _mfAt = 0;
async function getManifest(env, origin) {
  if (_mf && Date.now() - _mfAt < 60000) return _mf;
  try {
    const mf = await env.ASSETS.fetch(new Request(origin + '/_static.json'));
    if (mf.status === 200) { _mf = await mf.json(); _mfAt = Date.now(); return _mf; }
  } catch (e) { /* fall through */ }
  return null;
}
export async function onRequestGet({request, env, params}) {
  const url = new URL(request.url);
  // On manifest failure: fail OPEN to the static page, never to the client shell.
  const manifest = await getManifest(env, url.origin);
  if (!manifest || (manifest['categories'] || []).includes(params.slug)) {
    return env.ASSETS.fetch(new Request(url.origin + url.pathname.replace(/\/?$/, '/index.html')));
  }
  if (env.CONTENT) {
    const cats = JSON.parse(await env.CONTENT.get('content:categories') || '[]');
    const _it = cats.find(x => x.slug === params.slug && !x.unpublished);
    if (_it) {
      const _r = await dynamicResponse(env, url.origin, 'categories', _it);
      if (_r) return _r;
    }
  }
  return new Response('Not found', {status: 404});
}
