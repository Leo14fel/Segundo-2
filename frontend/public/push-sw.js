const DATABASE = "forge-push-device";
function settings(write, value) {
  return new Promise((resolve, reject) => {
    const open = indexedDB.open(DATABASE, 1);
    open.onupgradeneeded = () => open.result.createObjectStore("settings");
    open.onerror = () => reject(open.error);
    open.onsuccess = () => {
      const db = open.result,
        tx = db.transaction("settings", write ? "readwrite" : "readonly"),
        store = tx.objectStore("settings");
      const request = write ? store.put(value, "userId") : store.get("userId");
      let result;
      request.onsuccess = () => (result = request.result);
      tx.oncomplete = () => {
        db.close();
        resolve(result);
      };
      tx.onerror = () => {
        db.close();
        reject(tx.error);
      };
    };
  });
}
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) =>
  event.waitUntil(self.clients.claim()),
);
self.addEventListener("message", (event) => {
  if (event.data?.type === "FORGE_PUSH_BIND")
    event.waitUntil(
      settings(true, event.data.userId ?? null)
        .then(() => event.ports[0]?.postMessage({ ok: true }))
        .catch(() => event.ports[0]?.postMessage({ ok: false })),
    );
});
function safeDestination(value) {
  try {
    const url = new URL(value, self.location.origin);
    if (url.origin !== self.location.origin || url.pathname !== "/") return "/";
    const project = url.searchParams.get("project");
    if (!project || !/^[-a-f0-9]{36}$/i.test(project)) return "/";
    return "/?project=" + encodeURIComponent(project) + "&view=activity";
  } catch {
    return "/";
  }
}
self.addEventListener("push", (event) =>
  event.waitUntil(
    (async () => {
      let data;
      try {
        data = event.data?.json();
      } catch {
        return;
      }
      if (!data) return;
      const user = await settings(false);
      if (!user || user !== data.recipientUserId) return;
      await self.registration.showNotification("SinapUML", {
        body: "Tienes novedades en un proyecto compartido.",
        tag: typeof data.tag === "string" ? data.tag : "forge-update",
        icon: "/icons/icon-192.png",
        data: { url: safeDestination(data.url) },
      });
    })(),
  ),
);
self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const path = safeDestination(event.notification.data?.url);
  event.waitUntil(
    (async () => {
      const windows = await self.clients.matchAll({
        type: "window",
        includeUncontrolled: true,
      });
      for (const client of windows) {
        if (new URL(client.url).origin === self.location.origin) {
          await client.navigate(new URL(path, self.location.origin).href);
          await client.focus();
          return;
        }
      }
      await self.clients.openWindow(new URL(path, self.location.origin).href);
    })(),
  );
});
