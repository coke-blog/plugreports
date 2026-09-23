const C='pr-v14';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(['/','/assets/css/style.css','/assets/js/app.js?v=10','/assets/img/logo.svg','/manifest.webmanifest'])))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>clients.claim()))});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET'||!e.request.url.startsWith(self.location.origin))return;
 const p=new URL(e.request.url).pathname;
 // cache-first ONLY for fingerprinted static assets
 if(p.startsWith('/assets/')){
   e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(r=>{
     if(r.ok){const cl=r.clone();caches.open(C).then(c=>c.put(e.request,cl));}
     return r;
   })));
   return;
 }
 // network-first for HTML (and everything else) — fall back to cache when offline
 e.respondWith(fetch(e.request).then(r=>{
   if(r.ok){const cl=r.clone();caches.open(C).then(c=>c.put(e.request,cl));}
   return r;
 }).catch(()=>caches.match(e.request).then(hit=>hit||caches.match('/'))));
});
