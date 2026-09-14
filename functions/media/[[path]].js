export async function onRequestGet({env, params}) {
  if (!env.MEDIA) return new Response('Storage not bound', {status: 503});
  const key = (params.path || []).join('/');
  if (!key) return new Response('not found', {status: 404});
  const obj = await env.MEDIA.get(key);
  if (!obj) return new Response('not found', {status: 404});
  return new Response(obj.body, {
    headers: {
      'Content-Type': obj.httpMetadata?.contentType || 'application/octet-stream',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
}
