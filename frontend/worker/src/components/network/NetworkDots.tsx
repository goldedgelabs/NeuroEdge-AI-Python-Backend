'use client';
import React, { useEffect, useState } from 'react';

export default function NetworkDots(){ 
  const [status, setStatus] = useState<'online'|'limited'|'offline'>(navigator.onLine ? 'online':'offline');
  useEffect(()=>{
    const onOnline = ()=> setStatus('online');
    const onOffline = ()=> setStatus('offline');
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);
    // limited detection: try a quick fetch
    let id = setInterval(async ()=>{
      try{
        const r = await fetch('/favicon.ico', {method:'HEAD', cache:'no-store'});
        if(r.ok) setStatus('online'); else setStatus('limited');
      }catch{ setStatus('limited'); }
    }, 10000);
    return ()=>{ window.removeEventListener('online', onOnline); window.removeEventListener('offline', onOffline); clearInterval(id); };
  },[]);
  const color = status==='online' ? '#10b981' : status==='limited' ? '#f59e0b' : '#ef4444';
  return <div title={status} style={{width:12,height:12,borderRadius:'50%',background:color,boxShadow:'0 0 6px rgba(0,0,0,0.2)'}} />;
}
