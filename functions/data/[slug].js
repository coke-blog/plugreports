export async function onRequestGet({request, env, params}) {
  const url = new URL(request.url);
  // 1) published KV item wins — admin edits always take precedence over the
  //    static build copy (same precedence rule as the other content types)
  if (env.CONTENT) {
    const items = JSON.parse(await env.CONTENT.get('content:data') || '[]');
    if (items.some(x => x.slug === params.slug && !x.unpublished)) {
      const shell = await env.ASSETS.fetch(new Request(url.origin + '/_dynamic'));
      if (shell.status === 200) return new Response(shell.body, {
        headers: {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache'}});
    }
  }
  // 2) static build-time page for anything not in KV
  const st = await env.ASSETS.fetch(new Request(url.origin + '/data/' + params.slug + '/index.html'));
  if (st.status === 200) return st;
  return new Response('Not found', {status: 404});
}
