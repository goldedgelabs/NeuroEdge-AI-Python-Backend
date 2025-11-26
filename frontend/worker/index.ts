// Cloudflare Worker example (Edge)
addEventListener('fetch', event => {
  event.respondWith(handle(event.request));
});

async function handle(request){
  const url = new URL(request.url);
  if(url.pathname.startsWith('/v1/')){
    // simple proxy rule: forward to TS backend
    const backend = TOKENS.BACKEND_TS || 'http://localhost:5001';
    const proxied = backend + url.pathname.replace('/v1','/v1') + url.search;
    const res = await fetch(proxied, { method: request.method, headers: request.headers, body: request.body });
    return res;
  }
  return new Response('Worker root', { status: 200 });
}
