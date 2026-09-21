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
    if (cats.some(x => x.slug === params.slug && !x.unpublished)) {
      const shell = await env.ASSETS.fetch(new Request(url.origin + '/_dynamic'));
      if (shell.status === 200) return new Response(shell.body, {
        headers: {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache'}});
    }
  }
  return new Response('Not found', {status: 404});
}
