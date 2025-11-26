'use client';
import { useEffect, useRef } from 'react';

export function useSSE(url:string, onMessage:(data:any)=>void){
  const esRef = useRef<EventSource | null>(null);
  useEffect(()=>{
    if(!url) return;
    const es = new EventSource(url);
    esRef.current = es;
    es.onmessage = (ev)=> onMessage(ev.data);
    es.onerror = (err)=>{ console.error('SSE err',err); es.close(); };
    return ()=>{ if(esRef.current) esRef.current.close(); };
  },[url,onMessage]);
}
