// src/components/ui/OfflineBadge.tsx
'use client';
import React, { useEffect, useState } from 'react';
export default function OfflineBadge() {
  const [online, setOnline] = useState(navigator.onLine);
  useEffect(() => {
    const on = () => setOnline(true);
    const off = () => setOnline(false);
    window.addEventListener('online', on);
    window.addEventListener('offline', off);
    return () => {
      window.removeEventListener('online', on);
      window.removeEventListener('offline', off);
    };
  }, []);
  return (
    <div
      title={online ? 'Online' : 'Offline'}
      className={`inline-block w-3 h-3 rounded-full ${online ? 'bg-green-400' : 'bg-red-500'}`}
    />
  );
}
