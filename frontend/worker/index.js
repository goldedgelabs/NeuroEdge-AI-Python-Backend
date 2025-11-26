// simple worker proxy that handles /v1/* and forwards to TS backend by default
addEventListener('fetch', event=>{
  event.respondWith(handle(event.request));
});
async function handle(req){
  const url = new URL(req.url);
  if(url.pathname.startsWith('/v1/')){
    const target = process.env.BACKEND_TS || 'http://localhost:5001';
    const proxied = target + url.pathname + url.search;
    const res = await fetch(proxied, { method: req.method, headers: req.headers, body: req.body });
    return res;
  }
  return new Response('worker ok');
}
