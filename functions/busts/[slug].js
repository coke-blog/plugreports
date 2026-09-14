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
    if (items.some(x => x.slug === params.slug)) {
      const shell = await env.ASSETS.fetch(new Request(url.origin + '/_dynamic'));
      if (shell.status === 200) return new Response(shell.body, {
        headers: {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache'}});
    }
  }
  return new Response('Not found', {status: 404});
}
