import {checkAuth} from './_util.js';
export async function onRequestGet({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!env.CONTENT) return Response.json({ok: true, items: []});
  const q = (new URL(request.url).searchParams.get('q') || '').toLowerCase().trim();
  const listed = await env.CONTENT.list({prefix: 'media:'});
  let keys = listed.keys.map(k => k.name.replace(/^media:/, ''));
  if (q) keys = keys.filter(k => k.toLowerCase().includes(q) || k.toLowerCase().replace(/\.[a-z0-9]+$/, '').replace(/[-_]/g, ' ').includes(q));
  const base = (env.MEDIA_PUBLIC_URL || '').replace(/\/$/, '');
  return Response.json({ok: true, items: keys.slice(0, 60).map(k => ({name: k, url: `${base}/media/${k}`}))});
}
