export async function onRequestPost({request, env}) {
  if (!env.CONTENT) return Response.json({ok: false}, {status: 503});
  const {type, slug} = await request.json();
  if (!type || !slug || !/^[a-z0-9:-]+$/.test(slug)) return Response.json({ok: false}, {status: 400});
  const raw = await env.CONTENT.get('content:' + type);
  if (!raw) return Response.json({ok: false}, {status: 404});
  const items = JSON.parse(raw);
  const it = items.find(x => x.slug === slug);
  if (!it) return Response.json({ok: false}, {status: 404});
  it.views = (it.views || 0) + 1;
  await env.CONTENT.put('content:' + type, JSON.stringify(items));
  return Response.json({ok: true, views: it.views});
}
