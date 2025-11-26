import { useEffect, useRef } from 'react';
export function useWebSocket(url:string, onMessage:(data:any)=>void){
  const wsRef = useRef<WebSocket|null>(null);
  useEffect(()=>{
    if(!url) return;
    const ws = new WebSocket(url);
    wsRef.current = ws;
    ws.onopen = ()=> console.log('ws open');
    ws.onmessage = (ev)=> onMessage(ev.data);
    ws.onclose = ()=> console.log('ws closed');
    ws.onerror = (e)=> console.error('ws err', e);
    return ()=> { try{ ws.close(); }catch{} };
  },[url,onMessage]);
  return wsRef;
}
