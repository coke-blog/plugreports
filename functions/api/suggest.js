export async function onRequestPost({request, env}) {
  const data = await request.json();
  if(!env.CONTENT) return Response.json({ok:true, note:'kv-not-bound'});
  const list = JSON.parse(await env.CONTENT.get('suggestions') || '[]');
  list.unshift({ts: Date.now(), ...data});
  await env.CONTENT.put('suggestions', JSON.stringify(list.slice(0, 500)));
  return Response.json({ok: true});
}
