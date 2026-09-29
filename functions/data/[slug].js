import { dynamicResponse } from '../_seo.js';
export async function onRequestGet({request, env, params}) {
  const url = new URL(request.url);
  // 1) published KV item wins — admin edits always take precedence over the
  //    static build copy (same precedence rule as the other content types)
  if (env.CONTENT) {
    const items = JSON.parse(await env.CONTENT.get('content:data') || '[]');
    const _it = items.find(x => x.slug === params.slug && !x.unpublished);
    if (_it) {
      const _r = await dynamicResponse(env, url.origin, 'data', _it);
      if (_r) return _r;
    }
  }
  // 2) static build-time page for anything not in KV
  const st = await env.ASSETS.fetch(new Request(url.origin + '/data/' + params.slug + '/index.html'));
  if (st.status === 200) return st;
  return new Response('Not found', {status: 404});
}
