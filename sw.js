/* FOYER — service worker: rede primeiro, cache como socorro (offline) */
/* v3: a virada do tema (a casa abre com a luz da sala em todo aparelho). O
   nome novo joga fora as cópias guardadas do CSS antigo, para que nem o
   aplicativo aberto sem rede volte a abrir no Blackout. */
var CACHE = 'foyer-v3';

self.addEventListener('install', function (e) {
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (ks) {
      return Promise.all(ks.filter(function (k) { return k !== CACHE; })
        .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

/* notificações do aplicativo (1 por dia) */
self.addEventListener('push', function (e) {
  var d = {};
  try { d = e.data ? e.data.json() : {}; } catch (err) {}
  e.waitUntil(self.registration.showNotification(d.title || 'FOYER', {
    body: d.body || 'Novidades no saguão do teatro brasileiro.',
    icon: 'assets/logo/pwa-192.png',
    badge: 'assets/logo/pwa-192.png',
    data: { url: d.url || './index.html' },
    tag: 'foyer-diaria'
  }));
});

self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  var alvo = (e.notification.data && e.notification.data.url) || './index.html';
  e.waitUntil(clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (js) {
    for (var i = 0; i < js.length; i++) {
      if ('focus' in js[i]) { js[i].navigate(alvo); return js[i].focus(); }
    }
    return clients.openWindow(alvo);
  }));
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  var url = new URL(e.request.url);
  if (url.origin !== location.origin) return; // só o próprio site
  e.respondWith(
    fetch(e.request).then(function (r) {
      if (r && r.ok) {
        var copia = r.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, copia); }).catch(function () {});
      }
      return r;
    }).catch(function () {
      return caches.match(e.request).then(function (hit) {
        return hit || caches.match('./index.html');
      });
    })
  );
});
