// Service Worker für krawl.ist
// Strategie: Network-First mit Fallback zu Cache (für Event-Updates)

const CACHE_NAME = 'krawl-ist-v1';
const RUNTIME_CACHE = 'krawl-runtime';

// Statische Assets die sofort gecached werden
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/info.html',
  '/404.html',
  '/assets/css/fullscreen.css',
  '/assets/js/main.js',
  '/favicon.svg',
  '/favicon.ico'
];

// Installation: Precache statische Assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

// Aktivierung: Alte Caches löschen
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME && name !== RUNTIME_CACHE)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Network-First Strategie
self.addEventListener('fetch', event => {
  // Nur GET-Requests cachen
  if (event.request.method !== 'GET') return;
  
  // Admin-Bereich nicht cachen
  if (event.request.url.includes('/admin')) {
    return event.respondWith(fetch(event.request));
  }
  
  // External resources (CDN) nicht cachen
  if (!event.request.url.startsWith(self.location.origin)) {
    return event.respondWith(fetch(event.request));
  }

  event.respondWith(
    // 1. Versuche Network (für aktuelle Events)
    fetch(event.request)
      .then(response => {
        // Clone response für Cache
        const responseClone = response.clone();
        
        // Speichere in Runtime-Cache
        caches.open(RUNTIME_CACHE).then(cache => {
          cache.put(event.request, responseClone);
        });
        
        return response;
      })
      .catch(() => {
        // 2. Fallback: Cache (Offline-Modus)
        return caches.match(event.request)
          .then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            
            // 3. Fallback: 404-Seite bei kompletter Offline-Situation
            if (event.request.mode === 'navigate') {
              return caches.match('/404.html');
            }
            
            // 4. Kein Fallback verfügbar
            return new Response('Offline - Keine gecachte Version verfügbar', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
      })
  );
});

// Nachrichten vom Main Thread empfangen
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  // Cache manuell leeren
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(name => caches.delete(name))
        );
      })
    );
  }
});
