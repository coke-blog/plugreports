import {checkAuth, sha256, hasKV} from './_util.js';
const noKV = () => Response.json({ok:false, error:'Storage not bound'}, {status:503});
export async function onRequestPost({request, env}) {
  if (!await checkAuth(env, request)) return Response.json({ok: false}, {status: 401});
  if (!hasKV(env)) return noKV();
  const {current, next} = await request.json();
  const hash = await sha256(String(current || ''));
  const stored = await env.CONTENT.get('pinhash') || env.ADMIN_PIN_SHA256 || await sha256('plug2026!');
  if (hash !== stored) return Response.json({ok: false, error: 'Current PIN wrong'}, {status: 403});
  if (!next || String(next).length < 6) return Response.json({ok: false, error: 'New PIN too short'}, {status: 400});
  await env.CONTENT.put('pinhash', await sha256(String(next)));
  return Response.json({ok: true});
}
