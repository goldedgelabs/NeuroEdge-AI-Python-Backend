'use client';
import React, { useEffect, useState } from 'react';

export default function OfflineBanner(){
  const [online, setOnline] = useState(typeof navigator !== 'undefined' ? navigator.onLine : true);
  useEffect(()=>{
    const up = ()=> setOnline(true);
    const down = ()=> setOnline(false);
    window.addEventListener('online', up); window.addEventListener('offline', down);
    return ()=>{ window.removeEventListener('online', up); window.removeEventListener('offline', down); };
  },[]);
  if(online) return null;
  return (<div className='w-full bg-yellow-50 text-yellow-800 p-2 text-center'>You are offline. Messages will be queued and sent when you reconnect.</div>);
}
