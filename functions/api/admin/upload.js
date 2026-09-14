import {checkAuth} from './_util.js';
export async function onRequestPost({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  const name = new URL(request.url).searchParams.get('name') || '';
  if (!/^[\w\-\/\.]{3,200}$/.test(name) || name.includes('..') || name.startsWith('/'))
    return Response.json({ok: false, error: 'Invalid file name. Use e.g. drugs/fentanyl.webp'}, {status: 400});
  const ct = request.headers.get('Content-Type') || 'application/octet-stream';
  const base = (env.MEDIA_PUBLIC_URL || '').replace(/\/$/, '');
  const url = `${base}/media/${name}`;
  if (env.MEDIA) {
    await env.MEDIA.put(name, request.body, {httpMetadata: {contentType: ct}});
    return Response.json({ok: true, url, name, store: 'r2'});
  }
  if (env.CONTENT) {
    const buf = await request.arrayBuffer();
    if (buf.byteLength > 20 * 1024 * 1024) return Response.json({ok: false, error: 'File too large (20 MB max)'}, {status: 400});
    await env.CONTENT.put('media:' + name, buf);
    return Response.json({ok: true, url, name, store: 'kv'});
  }
  return Response.json({ok: false, error: 'No storage bound (KV or R2)'}, {status: 503});
}
