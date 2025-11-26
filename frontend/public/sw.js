/* NeuroEdge service worker - precache + queue + background sync */
const PRECACHE = ['/', '/chat', '/offline', '/manifest.json'];
const CACHE_NAME = 'neuroedge-static-v1';
const QUEUE_DB = 'neuroedge-queue-v1';
const QUEUE_STORE = 'requests';

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(QUEUE_DB, 1);
    req.onupgradeneeded = () => { const db = req.result; if(!db.objectStoreNames.contains(QUEUE_STORE)) db.createObjectStore(QUEUE_STORE, { autoIncrement:true }); };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}
async function addToQueue(item) {
  const db = await openDB();
  const tx = db.transaction(QUEUE_STORE, 'readwrite');
  tx.objectStore(QUEUE_STORE).add(item);
  return tx.complete;
}
async function getAllQueue() { const db = await openDB(); const tx = db.transaction(QUEUE_STORE, 'readonly'); const req = tx.objectStore(QUEUE_STORE).getAll(); return new Promise((res,rej)=>{ req.onsuccess=()=>res(req.result); req.onerror=()=>rej(req.error); }); }
async function clearQueue(){ const db = await openDB(); const tx = db.transaction(QUEUE_STORE,'readwrite'); tx.objectStore(QUEUE_STORE).clear(); return tx.complete; }

self.addEventListener('install', (evt)=>{ evt.waitUntil(caches.open(CACHE_NAME).then(c=>c.addAll(PRECACHE)).then(()=>self.skipWaiting())); });
self.addEventListener('activate', (evt)=>{ evt.waitUntil(self.clients.claim()); });

self.addEventListener('fetch', (evt)=>{
  const req = evt.request;
  const url = new URL(req.url);
  if(req.method === 'GET'){
    evt.respondWith(caches.match(req).then(cached=>cached||fetch(req).then(res=>{ const r2=res.clone(); caches.open(CACHE_NAME).then(c=>c.put(req,r2)); return res; }).catch(()=>caches.match('/offline'))));
    return;
  }
  if(req.method !== 'GET' && (url.pathname.startsWith('/v1/')||url.pathname.startsWith('/api/'))){
    evt.respondWith((async ()=>{ try{ const r = await fetch(req.clone()); return r; }catch(e){ const b = await req.clone().text().catch(()=>null); await addToQueue({ url:req.url, method:req.method, headers:Array.from(req.headers||[]), body:b, ts:Date.now() }); try{ await self.registration.sync.register('neuroedge-sync'); }catch{} return new Response(JSON.stringify({ queued:true }), { status:202, headers:{ 'Content-Type':'application/json' } }); } })());
    return;
  }
});

self.addEventListener('sync', (evt)=>{ if(evt.tag==='neuroedge-sync'){ evt.waitUntil((async ()=>{ const items = await getAllQueue(); for(const it of items){ try{ await fetch(it.url, { method: it.method, body: it.body, headers: Object.fromEntries(it.headers||[]) }); }catch{} } await clearQueue(); })()); } });
self.addEventListener('message', (evt)=>{ if(evt.data==='skipWaiting') self.skipWaiting(); });
