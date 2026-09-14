import {checkAuth} from './_util.js';
export async function onRequestPost({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!env.MEDIA) return Response.json({ok: false, error: 'R2 bucket MEDIA not bound yet'}, {status: 503});
  const name = new URL(request.url).searchParams.get('name') || '';
  if (!/^[\w\-\/\.]{3,200}$/.test(name) || name.includes('..') || name.startsWith('/'))
    return Response.json({ok: false, error: 'Invalid file name. Use e.g. drugs/fentanyl.webp'}, {status: 400});
  const ct = request.headers.get('Content-Type') || 'application/octet-stream';
  await env.MEDIA.put(name, request.body, {httpMetadata: {contentType: ct}});
  const base = (env.MEDIA_PUBLIC_URL || '').replace(/\/$/, '');
  return Response.json({ok: true, url: `${base}/media/${name}`, name});
}
