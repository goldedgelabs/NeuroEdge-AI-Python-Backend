import { EventRouter } from './event-router.js';

addEventListener('fetch', event => {
  event.respondWith(handle(event.request, event));
});

async function handle(request, event) {
  const url = new URL(request.url);
  // route events to Durable Object
  if (url.pathname.startsWith('/events')) {
    const id = EVENT_ROUTER.idFromName('main');
    const obj = EVENT_ROUTER.get(id);
    // forward request path as-is
    const forwardUrl = new URL(request.url);
    forwardUrl.hostname = 'dummy';
    return obj.fetch(new Request(forwardUrl.toString(), request));
  }

  // proxy /v1/* to configured backend (fallback order: TS, PY, GO)
  const ts = EVENT_ROUTER ? (EVENT_ROUTER.TS_BACKEND || 'http://localhost:4000') : 'http://localhost:4000';
  const py = EVENT_ROUTER ? (EVENT_ROUTER.PY_BACKEND || 'http://localhost:5000') : 'http://localhost:5000';
  const go = EVENT_ROUTER ? (EVENT_ROUTER.GO_BACKEND || 'http://localhost:6000') : 'http://localhost:6000';

  const backendList = [ts, py, go];
  if (url.pathname.startsWith('/v1/')) {
    let lastErr = null;
    for (const b of backendList) {
      try {
        const target = b.replace(/\/$/, '') + url.pathname + url.search;
        const res = await fetch(target, { method: request.method, headers: request.headers, body: request.body });
        // return on first successful
        if (res.ok || res.status < 500) {
          return res;
        } else {
          lastErr = res;
        }
      } catch (e) {
        lastErr = e;
      }
    }
    return new Response('All backends failed', { status: 502 });
  }

  return new Response('NeuroEdge Worker root');
}
