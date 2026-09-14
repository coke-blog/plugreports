export async function onRequestGet({request, env}) {
  const type = new URL(request.url).searchParams.get('type');
  if(!env.CONTENT) return Response.json({ok:true, items:[], note:'kv-not-bound'});
  const raw = await env.CONTENT.get('content:' + type);
  if (!raw) return Response.json({ok: true, items: []});
  return Response.json({ok: true, items: JSON.parse(raw)});
}
