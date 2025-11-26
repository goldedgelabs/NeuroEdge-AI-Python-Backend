'use client';
import React, { useState } from 'react';
import { sendChatMessage } from '@/services/http';
import { addMessageToDB, addToQueue } from '@/lib/offline-db';
import { db } from '@/lib/offline-db';
export default function ChatInput(){
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  async function send(){
    const base = process.env.NEXT_PUBLIC_BACKEND_PROXY || process.env.NEXT_PUBLIC_TS_BACKEND || '';

    if(!text) return;
    setSending(true);
    const localMsg = { role: 'user', text, createdAt: Date.now() };
    await addMessageToDB(localMsg);

    try{
      await sendChatMessage(text);
      setText('');
    }catch(e){
      // network error - queue message locally
      try{ await addToQueue({ text }); }catch(err){ console.error('queue add failed', err); }

      console.error(e);
    }finally{
      setSending(false);
    }
  }
  return (
    <div className="flex items-center gap-2">
      <input value={text} onChange={e=>setText(e.target.value)} className="flex-1 border rounded px-3 py-2" placeholder="Type a message..." data-testid="chat-input"/>
      <button onClick={send} className="px-4 py-2 bg-ne-primary text-white rounded" data-testid="send-btn">
        {sending ? 'Sending...' : 'Send'}
      </button>
    </div>
  )
}
