import { API_BASE_URL } from "../../services/api";
const OWNER = "sinapuml.push-owner";
let tail: Promise<unknown> = Promise.resolve();
function serial<T>(operation: () => Promise<T>): Promise<T> {
  const result = tail.then(operation);
  tail = result.catch(() => {});
  return result;
}
export function pushSupported() {
  return (
    window.isSecureContext &&
    "serviceWorker" in navigator &&
    "PushManager" in window &&
    "Notification" in window
  );
}
export function decodeApplicationKey(value: string): ArrayBuffer {
  const normalized = value.replace(/-/g, "+").replace(/_/g, "/");
  const bytes = Uint8Array.from(atob(normalized), (c) => c.charCodeAt(0));
  if (bytes.length !== 65 || bytes[0] !== 4)
    throw new Error("La clave pública de notificaciones es inválida.");
  return bytes.buffer;
}
async function api<T>(
  token: string,
  path: string,
  method = "GET",
  body?: unknown,
): Promise<T> {
  const response = await fetch(API_BASE_URL + "/push" + path, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      error.message ?? `No se pudo configurar push (${response.status}).`,
    );
  }
  return response.status === 204 || method === "DELETE"
    ? (undefined as T)
    : response.json();
}
export const pushConfiguration = (token: string) =>
  api<{ enabled: boolean; publicKey: string }>(token, "/config");
async function bind(
  registration: ServiceWorkerRegistration,
  userId: string | null,
) {
  const worker = registration.active;
  if (!worker) return;
  await new Promise<void>((resolve, reject) => {
    const channel = new MessageChannel();
    const timer = setTimeout(
      () =>
        reject(
          new Error(
            "No se pudo vincular el dispositivo. Recarga la aplicación.",
          ),
        ),
      4000,
    );
    channel.port1.onmessage = (e) => {
      clearTimeout(timer);
      channel.port1.close();
      e.data?.ok
        ? resolve()
        : reject(new Error("No se pudo vincular el dispositivo."));
    };
    worker.postMessage({ type: "FORGE_PUSH_BIND", userId }, [channel.port2]);
  });
}
export function bindPushAccount(userId: string | null) {
  if (!pushSupported()) return Promise.resolve();
  return serial(async () => {
    const registration = await navigator.serviceWorker.getRegistration("/");
    if (registration) await bind(registration, userId);
  });
}
export async function pushActive(userId: string) {
  if (!pushSupported() || localStorage.getItem(OWNER) !== userId) return false;
  const registration = await navigator.serviceWorker.getRegistration("/");
  return !!(await registration?.pushManager.getSubscription());
}
export function enablePush(userId: string, token: string, publicKey: string) {
  if (!pushSupported())
    return Promise.reject(
      new Error(
        "Este navegador necesita soporte Web Push y una conexión segura.",
      ),
    );
  // Call permission directly from the click, before awaiting network or the device lock.
  const permission = Notification.requestPermission();
  return serial(async () => {
    if ((await permission) !== "granted")
      throw new Error(
        "No se concedió permiso para notificaciones. Puedes seguir consultando Avisos dentro de la aplicación.",
      );
    if (localStorage.getItem("sinapuml.access-token") !== token)
      throw new Error("La cuenta cambió; inicia la activación de nuevo.");
    await navigator.serviceWorker.register("/push-sw.js");
    const registration = await navigator.serviceWorker.ready;
    let subscription = await registration.pushManager.getSubscription();
    if (subscription && localStorage.getItem(OWNER) !== userId) {
      await subscription.unsubscribe();
      subscription = null;
    }
    const created = !subscription;
    subscription ??= await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: decodeApplicationKey(publicKey),
    });
    try {
      if (localStorage.getItem("sinapuml.access-token") !== token)
        throw new Error("La cuenta cambió durante la activación.");
      await api(token, "/subscriptions", "POST", subscription.toJSON());
      await bind(registration, userId);
      localStorage.setItem(OWNER, userId);
    } catch (error) {
      if (created) await subscription.unsubscribe();
      throw error;
    }
  });
}
export function disablePush(userId: string, token: string | null) {
  if (!pushSupported()) return Promise.resolve();
  return serial(async () => {
    if (localStorage.getItem(OWNER) !== userId) return;
    const registration = await navigator.serviceWorker.getRegistration("/");
    if (!registration) {
      localStorage.removeItem(OWNER);
      return;
    }
    const subscription = await registration.pushManager.getSubscription();
    await bind(registration, null).catch(() => {});
    if (subscription) {
      await subscription.unsubscribe();
      if (token)
        await api(token, "/subscriptions", "DELETE", {
          endpoint: subscription.endpoint,
        }).catch(() => {});
    }
    localStorage.removeItem(OWNER);
  });
}
