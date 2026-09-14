export async function onRequestPost({request, env}) {
  if (!env.AI) return Response.json({ok: false, error: 'AI binding not configured'}, {status: 503});
  const {texts, target} = await request.json();
  if (!Array.isArray(texts) || !texts.length || !target)
    return Response.json({ok: false, error: 'bad input'}, {status: 400});
  const results = await Promise.all(texts.slice(0, 60).map(async t => {
    if (!t || typeof t !== 'string' || t.trim().length < 2 || t.length > 1500) return t;
    try {
      const out = await env.AI.run('@cf/meta/m2m100-1.2b', {text: t, target_lang: target, source_lang: 'en'});
      return out.translated_text || t;
    } catch (e) { return t; }
  }));
  return Response.json({ok: true, results});
}
