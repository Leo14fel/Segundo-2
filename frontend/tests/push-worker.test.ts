// @vitest-environment node
import { describe, it, expect, vi } from "vitest";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";

const source = readFileSync(
  new URL("../public/push-sw.js", import.meta.url),
  "utf8",
);
const project = "a1234567-1234-4234-8234-123456789abc";
function worker(user: string | null = "alice") {
  const listeners = new Map<string, (event: any) => void>();
  const showNotification = vi.fn(),
    openWindow = vi.fn();
  const self = {
    location: { origin: "https://forge.example" },
    addEventListener: (name: string, callback: (event: any) => void) =>
      listeners.set(name, callback),
    registration: { showNotification },
    clients: { matchAll: vi.fn(async () => []), openWindow },
  };
  const context: Record<string, any> = { self, URL };
  runInNewContext(source, context);
  // Replace storage with a deterministic account boundary; the actual push/click handlers execute unchanged.
  context.settings = async () => user;
  async function dispatch(name: string, event: Record<string, any>) {
    let pending = Promise.resolve();
    listeners.get(name)!({
      ...event,
      waitUntil: (promise: Promise<void>) => {
        pending = promise;
      },
    });
    await pending;
  }
  return { self, showNotification, openWindow, dispatch };
}
describe("push service worker", () => {
  it.each([null, "bob"])(
    "ignores messages for a different or logged-out account (%s)",
    async (user) => {
      const w = worker(user);
      await w.dispatch("push", {
        data: { json: () => ({ recipientUserId: "alice" }) },
      });
      expect(w.showNotification).not.toHaveBeenCalled();
    },
  );
  it("shows only generic content and preserves the authorized project route", async () => {
    const w = worker();
    await w.dispatch("push", {
      data: {
        json: () => ({
          recipientUserId: "alice",
          title: "Private",
          body: "Private chat",
          tag: "notification-1",
          url: `/?project=${project}`,
        }),
      },
    });
    expect(w.showNotification).toHaveBeenCalledWith(
      "Forge Studio",
      expect.objectContaining({
        body: "Tienes novedades en un proyecto compartido.",
        tag: "notification-1",
        data: { url: `/?project=${project}&view=activity` },
      }),
    );
    expect(JSON.stringify(w.showNotification.mock.calls)).not.toContain(
      "Private",
    );
  });
  it.each([
    "https://attacker.invalid/steal",
    "/api/private?token=secret",
    "/?project=invalid",
  ])("sanitizes click destination %s", async (url) => {
    const w = worker();
    await w.dispatch("notificationclick", {
      notification: { close: vi.fn(), data: { url } },
    });
    expect(w.openWindow).toHaveBeenCalledWith("https://forge.example/");
  });
  it("ignores malformed payloads", async () => {
    const w = worker();
    await w.dispatch("push", {
      data: {
        json: () => {
          throw new Error("invalid JSON");
        },
      },
    });
    expect(w.showNotification).not.toHaveBeenCalled();
  });
  it("acknowledges account binding only after storage succeeds", async () => {
    const listeners = new Map<string, (event: any) => void>();
    const context: Record<string, any> = {
      self: {
        addEventListener: (name: string, callback: (event: any) => void) =>
          listeners.set(name, callback),
      },
    };
    runInNewContext(source, context);
    const store = vi.fn(async () => {}),
      reply = vi.fn();
    context.settings = store;
    let pending = Promise.resolve();
    listeners.get("message")!({
      data: { type: "FORGE_PUSH_BIND", userId: null },
      ports: [{ postMessage: reply }],
      waitUntil: (p: Promise<void>) => {
        pending = p;
      },
    });
    await pending;
    expect(store).toHaveBeenCalledWith(true, null);
    expect(reply).toHaveBeenCalledWith({ ok: true });
  });
});
