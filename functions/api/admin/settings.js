import {checkAuth, hasKV} from './_util.js';
const noKV = () => Response.json({ok:false, error:'KV namespace CONTENT not bound yet — add it in Pages Settings → Functions → KV bindings, then retry.'}, {status:503});
export async function onRequestGet({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  return Response.json({ok: true, settings: JSON.parse(await env.CONTENT.get('settings') || '{}')});
}
export async function onRequestPost({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!hasKV(env)) return noKV();
  const cur = JSON.parse(await env.CONTENT.get('settings') || '{}');
  await env.CONTENT.put('settings', JSON.stringify({...cur, ...await request.json()}));
  return Response.json({ok: true});
}
