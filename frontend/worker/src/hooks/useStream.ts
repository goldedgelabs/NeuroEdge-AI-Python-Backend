import { useEffect, useRef, useState } from 'react';
export function useStream(url?:string){
  const [chunks, setChunks] = useState<string[]>([]);
  const esRef = useRef<EventSource|null>(null);
  useEffect(()=>{
    if(!url) return;
    const es = new EventSource(url);
    esRef.current = es;
    es.onmessage = (ev)=>{
      const raw = ev.data;
      let token = raw;
      try{ const p = JSON.parse(raw); if(p.token) token = p.token; }
      catch{}
      setChunks(c=>[...c, token]);
    };
    es.onerror = (e)=>{ console.error('sse err',e); es.close(); };
    return ()=> es.close();
  },[url]);
  return { chunks };
}
