import { db } from '@/lib/offline-db';
'use client';
import React, { useEffect, useRef, useState } from 'react';
import { getStreamURL } from '@/services/backendSelector';

export default function ChatStream(){
  const [messages, setMessages] = useState<string[]>([]);
  const evtRef = useRef<EventSource | null>(null);

  useEffect(()=>{ (async ()=>{ try{ const cached = await db.messages.toArray(); if(cached && cached.length) setMessages(cached.map(m=>m.text)); }catch{} })();
    let mounted = true;
    async function start(){
      const url = await getStreamURL();
      if(!url) return;
      const es = new EventSource(url);
      evtRef.current = es;
      es.onmessage = (ev) => {
        try{
          // server sends token fragments as plain text or JSON {token: "...", done: bool}
          const raw = ev.data;
          // example: plain token or JSON
          let token = raw;
          try{ const parsed = JSON.parse(raw); if(parsed.token) token = parsed.token; }catch{}
          if(!mounted) return;
          setMessages(prev => {
            const last = prev[prev.length-1] ?? '';
            const updated = [...prev.slice(0, -1), last + token];
            if(prev.length===0) return [token];
            return updated;
          });
        }catch(e){ console.error('sse parse', e); }
      };
      es.onerror = (err)=>{ console.error('sse error', err); es.close(); };
    }
    start();
    return ()=>{ mounted=false; if(evtRef.current) evtRef.current.close(); };
  }, []);

  return (
    <div>
      <div className="space-y-3">
        {messages.map((m,i)=>(
          <div key={i} className="p-3 bg-white border rounded" data-testid="assistant-message-stream">{m}</div>
        ))}
      </div>
    </div>
  );
}
