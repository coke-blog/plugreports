import {checkAuth, hasKV} from './_util.js';
const noKV = () => Response.json({ok:false, error:'KV namespace CONTENT not bound yet — add it in Pages Settings → Functions → KV bindings, then retry.'}, {status:503});
async function getList(env, type) { return JSON.parse(await env.CONTENT.get('content:' + type) || '[]'); }
export async function onRequestGet({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  const type = new URL(request.url).searchParams.get('type') || 'drugs';
  if (!hasKV(env)) return Response.json({ok: true, items: [], note: 'kv-not-bound'});
  return Response.json({ok: true, items: await getList(env, type)});
}
export async function onRequestPost({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!hasKV(env)) return noKV();
  const type = new URL(request.url).searchParams.get('type');
  const item = await request.json();
  if (!item.slug) return Response.json({ok: false, error: 'slug required'}, {status: 400});
  const list = await getList(env, type);
  if (list.some(x => x.slug === item.slug)) return Response.json({ok: false, error: 'slug exists'}, {status: 409});
  list.unshift(item);
  await env.CONTENT.put('content:' + type, JSON.stringify(list));
  return Response.json({ok: true});
}
export async function onRequestPut({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!hasKV(env)) return noKV();
  const {searchParams} = new URL(request.url);
  const type = searchParams.get('type'), slug = searchParams.get('slug');
  const item = await request.json();
  const list = (await getList(env, type)).map(x => x.slug === slug ? {...x, ...item, slug} : x);
  await env.CONTENT.put('content:' + type, JSON.stringify(list));
  return Response.json({ok: true});
}
export async function onRequestDelete({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!hasKV(env)) return noKV();
  const {searchParams} = new URL(request.url);
  const type = searchParams.get('type'), slug = searchParams.get('slug');
  // UNPUBLISH instead of wipe: item + fields preserved in KV, hidden from site.
  const list = (await getList(env, type)).map(x => x.slug === slug ? {...x, unpublished: true} : x);
  await env.CONTENT.put('content:' + type, JSON.stringify(list));
  return Response.json({ok: true, note: 'unpublished - fields preserved'});
}
