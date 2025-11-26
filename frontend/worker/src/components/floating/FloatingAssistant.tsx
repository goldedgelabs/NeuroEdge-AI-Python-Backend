'use client';
import React, { useState } from 'react';
import ChatInput from '@/components/chat/ChatInput';
import ChatStream from '@/components/chat/ChatStream';

export default function FloatingAssistant(){
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button data-testid="floating-assistant-toggle" onClick={()=>setOpen(true)} className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-ne-primary text-white shadow-lg">NE</button>

      {open && (
        <div data-testid="floating-chat" className="fixed bottom-20 right-6 w-96 bg-white border rounded shadow-lg p-4">
          <div className="flex justify-between items-center mb-2">
            <div className="font-semibold">NeuroEdge Assistant</div>
            <button data-testid="floating-assistant-close" onClick={()=>setOpen(false)}>Close</button>
          </div>
          <div className="h-56 overflow-auto mb-2 border rounded p-2 bg-ne-card">
            <ChatStream />
          </div>
          <ChatInput />
          <div className="mt-2 text-xs text-muted-foreground">NeuroEdge can make mistakes — check important info.</div>
        </div>
      )}
    </div>
  );
}
