'use client';
import React, { useState } from 'react';
import { sendChatMessage } from '@/services/http';

// 🔐 encrypted storage adapter
import { addEncryptedMessage } from '@/lib/encrypted-db-adapter';

// queue for offline network retries
import { addToQueue } from '@/lib/offline-db';

export default function ChatInput() {
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);

  async function send() {
    const trimmed = text.trim();
    if (!trimmed) return;

    setSending(true);

    // LOCAL ENCRYPTED SAVE
    const localMsg = {
      role: 'user',
      text: trimmed,
      createdAt: Date.now(),
      status: 'queued',
    };

    try {
      // 🔐 save encrypted version of user message
      await addEncryptedMessage(localMsg);
    } catch (e) {
      console.error('Encrypted local save failed:', e);
    }

    // Now try NETWORK SEND
    try {
      await sendChatMessage(trimmed);
      setText('');
    } catch (err) {
      console.error('Network error, queueing message...', err);

      // Save to queue so Service Worker can retry later
      try {
        await addToQueue({ text: trimmed });
      } catch (queueErr) {
        console.error('Queue add failed', queueErr);
      }
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="flex items-center gap-2">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="flex-1 border rounded px-3 py-2"
        placeholder="Type a message..."
        data-testid="chat-input"
      />

      <button
        onClick={send}
        className="px-4 py-2 bg-ne-primary text-white rounded"
        data-testid="send-btn"
      >
        {sending ? 'Sending...' : 'Send'}
      </button>
    </div>
  );
        }
