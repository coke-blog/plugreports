import { dynamicResponse } from '../_seo.js';
export async function onRequestGet({request, env, params}) {
  const url = new URL(request.url);
  const mf = await env.ASSETS.fetch(new Request(url.origin + '/_static.json'));
  const manifest = mf.status === 200 ? await mf.json() : {};
  if ((manifest['quit'] || []).includes(params.slug)) {
    return env.ASSETS.fetch(new Request(url.origin + url.pathname.replace(/\/?$/, '/index.html')));
  }
  if (env.CONTENT) {
    const items = JSON.parse(await env.CONTENT.get('content:quit') || '[]');
    const _it = items.find(x => x.slug === params.slug && !x.unpublished);
    if (_it) {
      const _r = await dynamicResponse(env, url.origin, 'quit', _it);
      if (_r) return _r;
    }
  }
  return new Response('Not found', {status: 404});
}
