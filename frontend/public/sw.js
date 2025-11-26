/* public/sw.js */
/* NeuroEdge service worker - precache + queue + background sync + periodic sync */

const PRECACHE = [
  '/',
  '/chat',
  '/manifest.json',
  '/offline',
  // add other built assets you want pre-cached
];

const CACHE_NAME = 'neuroedge-static-v2';
const QUEUE_DB = 'neuroedge-queue-v1';
const QUEUE_STORE = 'requests';

// helper: open indexedDB store for queue (vanilla idb)
function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(QUEUE_DB, 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(QUEUE_STORE)) {
        db.createObjectStore(QUEUE_STORE, { keyPath: 'id', autoIncrement: true });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function addToQueue(payload) {
  const db = await openDB();
  return new Promise((res, rej) => {
    const tx = db.transaction(QUEUE_STORE, 'readwrite');
    const store = tx.objectStore(QUEUE_STORE);
    const r = store.add(payload);
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
}

async function getAllQueue() {
  const db = await openDB();
  return new Promise((res, rej) => {
    const tx = db.transaction(QUEUE_STORE, 'readonly');
    const store = tx.objectStore(QUEUE_STORE);
    const req = store.getAll();
    req.onsuccess = () => res(req.result);
    req.onerror = () => rej(req.error);
  });
}

async function clearQueue() {
  const db = await openDB();
  return new Promise((res, rej) => {
    const tx = db.transaction(QUEUE_STORE, 'readwrite');
    const store = tx.objectStore(QUEUE_STORE);
    const req = store.clear();
    req.onsuccess = () => res();
    req.onerror = () => rej(req.error);
  });
}

// Precache on install
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

// Activate immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

// Cache-first GET, queue POST/PUT/DELETE to /v1/ or /api/ for offline
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip cross-origin requests to not accidentally cache third-party resources
  if (url.origin !== location.origin) {
    return;
  }

  // GET requests -> cache-first
  if (req.method === 'GET') {
    event.respondWith(
      caches.match(req).then((cached) => {
        if (cached) return cached;
        return fetch(req)
          .then((res) => {
            // Only cache successful responses
            if (res && res.ok) {
              const copy = res.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
            }
            return res;
          })
          .catch(() => caches.match('/offline'));
      })
    );
    return;
  }

  // Non-GET requests to API -> try network; on failure, queue and respond 202
  if (req.method !== 'GET' && (url.pathname.startsWith('/v1/') || url.pathname.startsWith('/api/'))) {
    event.respondWith(
      (async () => {
        try {
          const networkResp = await fetch(req.clone());
          return networkResp;
        } catch (err) {
          // offline -> queue request body
          let body = null;
          try {
            body = await req.clone().json();
          } catch (e) {
            try {
              body = await req.clone().text();
            } catch (e2) {
              body = null;
            }
          }
          const headers = {};
          for (const [k, v] of req.headers.entries()) headers[k] = v;

          await addToQueue({
            url: req.url,
            method: req.method,
            headers,
            body,
            createdAt: Date.now(),
            retries: 0
          });

          // Try to register background sync
          try {
            await self.registration.sync.register('neuroedge-sync');
          } catch (e) {
            // Periodic sync registration will be tried by the client as well
          }

          return new Response(JSON.stringify({ queued: true }), {
            status: 202,
            headers: { 'Content-Type': 'application/json' }
          });
        }
      })()
    );
    return;
  }
});

// Sync event: flush the queue
self.addEventListener('sync', (event) => {
  if (event.tag === 'neuroedge-sync') {
    event.waitUntil(flushQueue());
  }
});

// Periodic background sync (if supported)
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'neuroedge-periodic-sync') {
    event.waitUntil(flushQueue());
  }
});

async function flushQueue() {
  const items = await getAllQueue();
  if (!items || items.length === 0) return;
  for (const item of items) {
    try {
      const headers = new Headers(item.headers || {});
      // do network request
      await fetch(item.url, {
        method: item.method,
        headers,
        body: typeof item.body === 'string' ? item.body : JSON.stringify(item.body)
      });
    } catch (e) {
      // increment retry and keep in DB for next try
      // (Simple approach: stop here to avoid continuous retries)
      console.warn('flush failed for', item.url, e);
      // No destructive action here; leave item in queue
      return;
    }
  }
  // If all processed without retry errors, clear queue
  await clearQueue();

  // Notify clients that queue flushed
  const clients = await self.clients.matchAll({ includeUncontrolled: true });
  for (const c of clients) {
    c.postMessage({ type: 'neuroedge:queueFlushed' });
  }
}

// message for skipWaiting
self.addEventListener('message', (ev) => {
  if (ev.data === 'skipWaiting') self.skipWaiting();
});
