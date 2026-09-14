export const hasKV = env => !!env.CONTENT;
export async function checkAuth(env, request) {
  const pinHash = (env.CONTENT ? await env.CONTENT.get('pinhash') : null) || env.ADMIN_PIN_SHA256 || '';
  const key = await crypto.subtle.importKey('raw',
    new TextEncoder().encode(env.TOKEN_SECRET || 'dev-secret-change-me'),
    {name: 'HMAC', hash: 'SHA-256'}, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode('plugreports-admin'));
  const expect = [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
  const token = (request.headers.get('Authorization') || '').replace('Bearer ', '');
  return token === expect;
}
export const sha256 = async s => [...new Uint8Array(
  await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))]
  .map(b => b.toString(16).padStart(2, '0')).join('');
