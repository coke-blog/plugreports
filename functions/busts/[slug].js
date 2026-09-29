import { dynamicResponse } from '../_seo.js';
export async function onRequestGet({request, env, params}) {
  const url = new URL(request.url);
  // 1) is this slug a real static page? (Pages falls back to index.html for missing paths,
  //    so we decide using the build-time manifest instead of probing)
  const mf = await env.ASSETS.fetch(new Request(url.origin + '/_static.json'));
  const manifest = mf.status === 200 ? await mf.json() : {};
  if ((manifest['busts'] || []).includes(params.slug)) {
    return env.ASSETS.fetch(new Request(url.origin + url.pathname.replace(/\/?$/, '/index.html')));
  }
  // 2) admin-created item in KV? render client-side
  if (env.CONTENT) {
    const items = JSON.parse(await env.CONTENT.get('content:busts') || '[]');
    const _it = items.find(x => x.slug === params.slug && !x.unpublished);
    if (_it) {
      const _r = await dynamicResponse(env, url.origin, 'busts', _it);
      if (_r) return _r;
    }
  }
  return new Response('Not found', {status: 404});
}
