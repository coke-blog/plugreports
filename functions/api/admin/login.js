import {sha256} from './_util.js';
export async function onRequestPost({request, env}) {
  const {pin} = await request.json();
  const hash = await sha256(String(pin || ''));
  const stored = (env.CONTENT ? await env.CONTENT.get('pinhash') : null)
    || env.ADMIN_PIN_SHA256
    || await sha256('plug2026!');           // default dev PIN — set ADMIN_PIN_SHA256 to override
  if (hash !== stored) return Response.json({ok: false}, {status: 401});
  const key = await crypto.subtle.importKey('raw',
    new TextEncoder().encode(env.TOKEN_SECRET || 'dev-secret-change-me'),
    {name: 'HMAC', hash: 'SHA-256'}, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode('plugreports-admin'));
  return Response.json({ok: true, token: [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('')});
}
