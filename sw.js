const CACHE = 'konstsok-v4';
const PRECACHE = [
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
  // lägg till ./style.css, ./main.js här om du bryter ut filerna
];

// Installera och cacha
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

// Aktivera och städa gamla cachear
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Strategier: nät-först för API, cache-först för övrigt
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // API-anrop mot EntryScape
  if (url.hostname.includes('entryscape.net')) {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }

  // Navigering: returnera index.html (SPA-lik fallback)
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch('./index.html').catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Övrigt: cache först
  event.respondWith(
    caches.match(event.request).then(res => res || fetch(event.request))
  );
});
