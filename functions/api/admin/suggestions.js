import {checkAuth} from './_util.js';
export async function onRequestGet({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  return Response.json({ok: true, items: JSON.parse(await env.CONTENT.get('suggestions') || '[]')});
}
