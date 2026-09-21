const TYPES = {webp: 'image/webp', jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png',
  gif: 'image/gif', svg: 'image/svg+xml', avif: 'image/avif', mp4: 'video/mp4', webm: 'video/webm'};
export async function onRequestGet({env, params}) {
  const key = (params.path || []).join('/');
  if (!key) return new Response('not found', {status: 404});
  let body = null, ct = TYPES[key.split('.').pop().toLowerCase()] || 'application/octet-stream';
  if (env.MEDIA) {
    const obj = await env.MEDIA.get(key);
    if (obj) { body = obj.body; ct = obj.httpMetadata?.contentType || ct; }
  }
  if (!body && env.CONTENT) {
    const kv = await env.CONTENT.get('media:' + key, 'arrayBuffer');
    if (kv) body = kv;
  }
  if (!body) return new Response('not found', {status: 404});
  // KV/R2-backed media is mutable (re-uploads reuse the same filename), so keep
  // cache lifetimes short and force revalidation instead of immutable year-long caching.
  return new Response(body, {headers: {'Content-Type': ct, 'Cache-Control': 'public, max-age=3600, must-revalidate'}});
}
