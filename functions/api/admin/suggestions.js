import {checkAuth} from './_util.js';
export async function onRequestGet({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  return Response.json({ok: true, items: JSON.parse(await env.CONTENT.get('suggestions') || '[]')});
}
export async function onRequestDelete({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  const i = parseInt(new URL(request.url).searchParams.get('i'), 10);
  const items = JSON.parse(await env.CONTENT.get('suggestions') || '[]');
  if (isNaN(i) || i < 0 || i >= items.length)
    return Response.json({ok: false, error: 'invalid index'}, {status: 400});
  items.splice(i, 1);
  await env.CONTENT.put('suggestions', JSON.stringify(items));
  return Response.json({ok: true});
}
