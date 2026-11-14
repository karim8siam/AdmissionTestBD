/* =========================================================
   Admission Test BD - Push & Monetization Service Worker
   Designed for RichAds (RichPush) & Web Push Notifications
   ========================================================= */

// RICHADS-WORKER-IMPORT-START
// RICHADS-WORKER-IMPORT-END

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

// Native Web Push notification listener
self.addEventListener('push', (event) => {
  if (event.data) {
    try {
      const data = event.data.json();
      const title = data.title || 'Admission Test BD';
      const options = {
        body: data.body || 'নতুন মডেল টেস্ট ও ভর্তি প্রস্তুতি আপডেট!',
        icon: data.icon || '/assets/logo.svg',
        badge: data.badge || '/assets/logo.svg',
        data: data.url || '/',
        vibrate: [100, 50, 100],
        actions: data.actions || []
      };
      event.waitUntil(self.registration.showNotification(title, options));
    } catch (e) {
      const text = event.data.text();
      event.waitUntil(
        self.registration.showNotification('Admission Test BD', {
          body: text || 'নতুন আপডেট উপলব্ধ!',
          icon: '/assets/logo.svg'
        })
      );
    }
  }
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const targetUrl = (event.notification.data && typeof event.notification.data === 'string') 
    ? event.notification.data 
    : '/';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      for (let client of windowClients) {
        if (client.url === targetUrl && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
