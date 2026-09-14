export async function onRequestGet({request, env, params}) {
  const url = new URL(request.url);
  const mf = await env.ASSETS.fetch(new Request(url.origin + '/_static.json'));
  const manifest = mf.status === 200 ? await mf.json() : {};
  if ((manifest['categories'] || []).includes(params.slug)) {
    return env.ASSETS.fetch(new Request(url.origin + url.pathname.replace(/\/?$/, '/index.html')));
  }
  if (env.CONTENT) {
    const cats = JSON.parse(await env.CONTENT.get('content:categories') || '[]');
    if (cats.some(x => x.slug === params.slug)) {
      const shell = await env.ASSETS.fetch(new Request(url.origin + '/_dynamic'));
      if (shell.status === 200) return new Response(shell.body, {
        headers: {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache'}});
    }
  }
  return new Response('Not found', {status: 404});
}
