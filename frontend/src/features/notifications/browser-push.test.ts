import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  bindPushAccount,
  decodeApplicationKey,
  enablePush,
  pushActive,
} from "./browser-push";

describe("browser push activation", () => {
  const permission = vi.fn(async () => "denied" as NotificationPermission);
  const registration = vi.fn();
  beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal("isSecureContext", true);
    vi.stubGlobal("PushManager", class {});
    vi.stubGlobal("Notification", { requestPermission: permission });
    Object.defineProperty(navigator, "serviceWorker", {
      configurable: true,
      value: { getRegistration: registration, register: vi.fn() },
    });
    permission.mockClear();
    registration.mockReset().mockResolvedValue(undefined);
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    delete (navigator as any).serviceWorker;
  });
  it("never asks permission while loading or binding an account", async () => {
    await bindPushAccount("alice");
    expect(await pushActive("alice")).toBe(false);
    expect(permission).not.toHaveBeenCalled();
  });
  it("denied permission does not register a worker or send a subscription", async () => {
    await expect(enablePush("alice", "token", "key")).rejects.toThrow(
      "No se concedió permiso",
    );
    expect(permission).toHaveBeenCalledOnce();
    expect(navigator.serviceWorker.register).not.toHaveBeenCalled();
  });
  it("rejects activation if the account changed while permission was requested", async () => {
    permission.mockResolvedValueOnce("granted");
    localStorage.setItem("forge-studio.access-token", "different-token");
    await expect(enablePush("alice", "old-token", "key")).rejects.toThrow(
      "La cuenta cambió",
    );
    expect(navigator.serviceWorker.register).not.toHaveBeenCalled();
  });
  it("rejects malformed application keys", () => {
    expect(() => decodeApplicationKey("short")).toThrow();
    const bytes = new Uint8Array(65);
    bytes[0] = 4;
    const key = btoa(String.fromCharCode(...bytes))
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=+$/, "");
    expect(new Uint8Array(decodeApplicationKey(key))).toEqual(bytes);
  });
});
