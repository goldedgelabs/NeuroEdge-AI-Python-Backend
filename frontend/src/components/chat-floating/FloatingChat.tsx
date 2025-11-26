'use client';

import React, { useState, useEffect } from 'react';
import ChatStream from '@/components/chat/ChatStream';
import ChatInput from '@/components/chat/ChatInput';
import { getDecryptedMessages } from '@/lib/encrypted-db-adapter';

export default function FloatingChat() {
  const [open, setOpen] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  //
  // Restore encrypted offline messages (optional UI sync)
  //
  useEffect(() => {
    (async () => {
      try {
        const msgs = await getDecryptedMessages();
        console.log("FloatingChat decrypted:", msgs);
      } catch (err) {
        console.warn("FloatingChat could not decrypt messages:", err);
      }
      setHydrated(true);
    })();
  }, []);

  if (!hydrated) {
    // Avoid hydration mismatch
    return null;
  }

  return (
    <div>
      {/* Floating launcher button */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="
            fixed bottom-6 right-6 z-50
            rounded-full shadow-lg
            px-4 py-3 font-semibold
            bg-ne-primary text-white
            hover:opacity-90 transition
          "
          data-testid="floating-open"
        >
          NE
        </button>
      )}

      {/* Expanded panel */}
      {open && (
        <div
          className="
            fixed bottom-6 right-6
            w-96 h-[420px] z-50
            bg-white border rounded-xl shadow-xl
            flex flex-col p-3
            animate-in fade-in zoom-in duration-200
          "
          data-testid="floating-panel"
        >
          <div className="flex justify-between items-center mb-2">
            <strong className="text-lg">NeuroEdge</strong>
            <button
              onClick={() => setOpen(false)}
              className="px-2 py-1 text-sm rounded hover:bg-gray-200"
              data-testid="floating-close"
            >
              ✕
            </button>
          </div>

          <div className="flex-1 overflow-auto border rounded p-2 bg-ne-card">
            <ChatStream />
          </div>

          <div className="mt-2">
            <ChatInput />
          </div>
        </div>
      )}
    </div>
  );
      }
