const C='pr-v2';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(['/','/assets/css/style.css','/assets/js/app.js','/assets/img/logo.svg','/manifest.webmanifest'])))});
self.addEventListener('activate',e=>{e.waitUntil(clients.claim())});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET'||!e.request.url.startsWith(self.location.origin))return;
 e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(r=>{
   if(r.ok&&/\.(css|js|svg|png|webp|woff2?)$/.test(new URL(e.request.url).pathname)){const cl=r.clone();caches.open(C).then(c=>c.put(e.request,cl));}
   return r;
 }).catch(()=>caches.match('/'))));
});