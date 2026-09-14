export async function onRequestGet({request, env, params}) {
  if (!env.CONTENT) return new Response('Storage not bound', {status: 503});
  const items = JSON.parse(await env.CONTENT.get('content:drugs') || '[]');
  if (!items.some(x => x.slug === params.slug)) return new Response('Not found', {status: 404});
  const url = new URL('/_dynamic.html', request.url);
  return env.ASSETS.fetch(new Request(url, request));
}
