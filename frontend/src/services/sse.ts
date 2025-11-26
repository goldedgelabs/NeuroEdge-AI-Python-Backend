export function connectSSE(url:string, onMessage:(d:any)=>void){
  const es = new EventSource(url);
  es.onmessage = (ev)=> onMessage(ev.data);
  es.onerror = (e)=> { console.error('SSE err', e); es.close(); };
  return es;
}
