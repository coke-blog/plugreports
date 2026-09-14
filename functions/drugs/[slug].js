export async function onRequestGet({request, env, params}) {
  const url = new URL(request.url);
  // 1) real static page? (Pages serves 404.html as 200, so verify by marker)
  const st = await env.ASSETS.fetch(new Request(url.origin + url.pathname.replace(/\/?$/, '/index.html')));
  if (st.status === 200) {
    const txt = await st.text();
    if (txt.includes('/assets/js/hydrate.js'))
      return new Response(txt, {headers: {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=3600'}});
  }
  // 2) admin-created item in KV? render client-side
  if (env.CONTENT) {
    const items = JSON.parse(await env.CONTENT.get('content:drugs') || '[]');
    if (items.some(x => x.slug === params.slug)) {
      const shell = await env.ASSETS.fetch(new Request(url.origin + '/_dynamic'));
      if (shell.status === 200) return new Response(shell.body, {
        headers: {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache'}});
    }
  }
  return new Response('Not found', {status: 404});
}
