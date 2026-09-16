export async function onRequestGet({request, env}) {
  const type = new URL(request.url).searchParams.get('type');
  if (!env.CONTENT) return Response.json({ok: true, items: [], note: 'kv-not-bound'});
  if (type === 'settings') {
    const raw = await env.CONTENT.get('settings');
    return Response.json({ok: true, items: raw ? [JSON.parse(raw)] : []});
  }
  const raw = await env.CONTENT.get('content:' + type);
  if (!raw) return Response.json({ok: true, items: []});
  // public consumers only see published items (admin uses the authenticated API)
  return Response.json({ok: true, items: JSON.parse(raw).filter(x => !x.unpublished)});
}
