'use client';

import React, { useEffect } from 'react';
import '@/styles/globals.css';
import FloatingChat from '@/components/chat-floating/FloatingChat';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'NeuroEdge',
  description: 'NeuroEdge frontend',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  useEffect(() => {
    // --- Service Worker Registration ---
    if (typeof window !== "undefined" && "serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker
          .register("/service-worker.js", { scope: "/" })
          .then((reg) => {
            console.log("Service Worker registered:", reg);

            // Auto-update logic
            if (reg.waiting) {
              reg.waiting.postMessage({ type: "SKIP_WAITING" });
            }

            reg.addEventListener("updatefound", () => {
              const newSW = reg.installing;
              if (newSW) {
                newSW.addEventListener("statechange", () => {
                  if (newSW.state === "installed" && navigator.serviceWorker.controller) {
                    console.log("New service worker ready (will activate on reload)");
                  }
                });
              }
            });
          })
          .catch((err) => console.error("SW registration failed", err));
      });
    }
  }, []);

  return (
    <html lang="en">
      <head>
        {/* PWA meta tags */}
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#0a0a0a" />

        {/* iOS Standalone Fix */}
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <link rel="apple-touch-icon" href="/icons/icon-192.png" />

        {/* Prevent font/layout flashing */}
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>

      <body className="app-shell min-h-screen bg-gray-50 text-black">
        {/* Page content */}
        {children}

        {/* Global Floating Chat (always accessible) */}
        <FloatingChat />
      </body>
    </html>
  );
}
