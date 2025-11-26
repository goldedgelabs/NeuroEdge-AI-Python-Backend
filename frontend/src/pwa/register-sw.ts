// src/pwa/register-sw.ts
export async function registerServiceWorker() {
  if (!('serviceWorker' in navigator)) return;

  try {
    const reg = await navigator.serviceWorker.register('/sw.js');
    console.log('SW registered', reg);

    // Listen to messages from SW
    navigator.serviceWorker.addEventListener('message', (ev) => {
      if (ev.data?.type === 'neuroedge:queueFlushed') {
        console.log('Queue flushed by SW');
        // Optionally notify UI / update stores
      }
    });

    // Try register Periodic Background Sync (experimental)
    if ('periodicSync' in reg) {
      try {
        // request permission via Permissions API (if available)
        // some platforms require 'periodic-background-sync' permission
        const status = await (navigator as any).permissions?.query?.({ name: 'periodic-background-sync' });
        // register periodic sync for every 6 hours (example)
        await (reg as any).periodicSync.register('neuroedge-periodic-sync', {
          minInterval: 6 * 60 * 60 * 1000 // 6 hours in ms
        });
        console.log('Periodic sync registered');
      } catch (e) {
        console.warn('Periodic sync registration failed', e);
      }
    } else {
      // Fallback: if SW cannot do periodic, set up client-based interval as a best-effort
      const flushOnConnectivity = async () => {
        // notify SW to attempt flush via sync registration if available
        try {
          if (navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({ type: 'neuroedge:attemptFlush' });
          }
        } catch (e) {}
      };
      // try flush every 4 hours while page is open (best-effort)
      setInterval(flushOnConnectivity, 4 * 60 * 60 * 1000);
      // and flush on regaining connectivity
      window.addEventListener('online', flushOnConnectivity);
    }
  } catch (err) {
    console.error('Failed to register service worker', err);
  }
}
