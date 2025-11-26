'use client';
import React, { useEffect, useState } from 'react';
import { db } from '@/lib/offline-db';

export default function QueueStatus(){
  const [count, setCount] = useState(0);
  useEffect(()=>{
    let mounted=true;
    (async ()=>{ if(!mounted) return; const n = await db.queue.count(); setCount(n); })();
    const id = setInterval(async ()=>{ const n=await db.queue.count(); setCount(n); }, 2000);
    return ()=>{ mounted=false; clearInterval(id); };
  },[]);
  if(count===0) return null;
  return <div className='text-xs text-muted-foreground'>Queued messages: {count}</div>;
}
