'use client';

import React, { useEffect } from 'react';
import '@/styles/globals.css';
import FloatingChat from '@/components/chat-floating/FloatingChat';
import { ReactNode } from 'react';

export const metadata = {
  title: 'NeuroEdge',
  description: 'NeuroEdge frontend',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  useEffect(() => {
    // Your service worker injection
    if (typeof window !== "undefined" && "serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker
          .register("/service-worker.js")
          .catch(err => console.error("SW registration failed", err));
      });
    }
  }, []);

  return (
    <html lang="en">
      <head />
      <body className="app-shell min-h-screen">
        {children}

        {/* Floating Chat UI */}
        <FloatingChat />
      </body>
    </html>
  );
}
