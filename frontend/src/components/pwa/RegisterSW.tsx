'use client';
import { useEffect } from 'react';
import { processLocalQueue } from '@/lib/queue-processor';

export default function RegisterSW() {
  useEffect(()=>{
    if('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').then(reg=>{
        console.log('sw registered', reg);
      }).catch(err=> console.error('sw reg err', err));
    }

    const onOnline = () => {
      console.log('online - processing queue');
      const base = process.env.NEXT_PUBLIC_BACKEND_PROXY || process.env.NEXT_PUBLIC_TS_BACKEND || '';
      if(base) processLocalQueue(base.replace(/\/$/,''));
      // also send message to SW to process queue
      if(navigator.serviceWorker?.controller) navigator.serviceWorker.controller.postMessage({ type:'process-queue' });
    };

    window.addEventListener('online', onOnline);
    return ()=> window.removeEventListener('online', onOnline);
  },[]);
  return null;
}
