const CACHE_NAME = 'neuroedge-shell-v1';
const OFFLINE_URL = '/offline.html';
const PRECACHE = [
  '/',
  '/offline.html',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await cache.addAll(PRECACHE);
    self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.map(k => { if (k !== CACHE_NAME) return caches.delete(k); }));
    self.clients.claim();
  })());
});

// utility for isNavigation
function isNavigationRequest(req) {
  return req.mode === 'navigate' || (req.method === 'GET' && req.headers.get('accept') && req.headers.get('accept').includes('text/html'));
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API requests: try network-first, fallback to queue for POST, cache fallback for GET
  if (url.pathname.startsWith('/v1/') || url.pathname.startsWith('/api/')) {
    if (request.method === 'GET') {
      event.respondWith(networkFirst(request));
    } else if (request.method === 'POST') {
      // For POST we use background queue: respond with 202 if offline and queue
      event.respondWith((async () => {
        try {
          const resp = await fetch(request.clone());
          return resp;
        } catch (err) {
          // offline - queue the request and return 202 Accepted
          const body = await request.clone().text();
          const queue = await getQueue();
          await queueAdd({ url: request.url, body, headers: [...request.headers], method: request.method });
          return new Response(JSON.stringify({ queued: true }), { status: 202, headers: { 'Content-Type': 'application/json' } });
        }
      })());
    }
    return;
  }

  // Navigation: try network first, fallback to cached shell
  if (isNavigationRequest(request)) {
    event.respondWith((async () => {
      try {
        const resp = await fetch(request);
        const cache = await caches.open(CACHE_NAME);
        cache.put(request, resp.clone());
        return resp;
      } catch (err) {
        const cache = await caches.open(CACHE_NAME);
        const cached = await cache.match(request) || await cache.match(OFFLINE_URL);
        return cached;
      }
    })());
    return;
  }

  // Static resources: cache-first
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    if (cached) return cached;
    try {
      const resp = await fetch(request);
      cache.put(request, resp.clone());
      return resp;
    } catch (err) {
      return cached || fetch(request).catch(()=>new Response('', {status:408}));
    }
  })());
});

// Simple in-sw queue using IndexedDB via idb-like minimal code
function getDB() {
  return new Promise((resolve, reject) => {
    const openReq = indexedDB.open('neuroedge-sw-queue', 1);
    openReq.onupgradeneeded = () => {
      const db = openReq.result;
      if (!db.objectStoreNames.contains('queue')) db.createObjectStore('queue', { keyPath: 'id', autoIncrement: true });
    };
    openReq.onsuccess = () => resolve(openReq.result);
    openReq.onerror = () => reject(openReq.error);
  });
}
async function getQueue() {
  const db = await getDB();
  return {
    async add(item) {
      return new Promise((res, rej) => {
        const tx = db.transaction('queue', 'readwrite');
        const store = tx.objectStore('queue');
        const r = store.add(item);
        r.onsuccess = ()=>res(r.result);
        r.onerror = ()=>rej(r.error);
      });
    },
    async list() {
      return new Promise((res, rej) => {
        const tx = db.transaction('queue', 'readonly');
        const store = tx.objectStore('queue');
        const r = store.getAll();
        r.onsuccess = ()=>res(r.result);
        r.onerror = ()=>rej(r.error);
      });
    },
    async remove(id) {
      return new Promise((res, rej) => {
        const tx = db.transaction('queue', 'readwrite');
        const store = tx.objectStore('queue');
        const r = store.delete(id);
        r.onsuccess = ()=>res(true);
        r.onerror = ()=>rej(r.error);
      });
    }
  }
}

async function queueAdd(item) {
  const q = await getQueue();
  await q.add({ ...item, created: Date.now() });
  // notify clients
  const all = await self.clients.matchAll();
  for (const c of all) c.postMessage({ type: 'queue-updated' });
}

// process queue when online
self.addEventListener('sync', (event) => {
  if (event.tag === 'neuroedge-sync') event.waitUntil(processQueue());
});

self.addEventListener('message', (ev) => {
  if (ev.data && ev.data.type === 'process-queue') {
    event = ev; // eslint-disable-line
    processQueue();
  }
});

async function processQueue() {
  const q = await getQueue();
  const items = await q.list();
  for (const it of items) {
    try {
      const headers = new Headers(it.headers || []);
      await fetch(it.url, { method: it.method, body: it.body, headers });
      await q.remove(it.id);
    } catch (err) {
      // keep it for later
    }
  }
}

async function networkFirst(req) {
  try {
    const res = await fetch(req);
    const cache = await caches.open(CACHE_NAME);
    cache.put(req, res.clone());
    return res;
  } catch (err) {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(req);
    return cached || new Response(null, { status:408 });
  }
}
