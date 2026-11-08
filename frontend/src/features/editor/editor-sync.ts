import { getProject, historyState } from "./editor-api";
import { Client } from "@stomp/stompjs";
import { API_BASE_URL } from "../../services/api";
import type {
  JsonValue,
  ProjectDocument,
  ProjectEditorState,
  ProjectRole,
} from "./types";
import type { SessionPage } from "./group-session-api";

export type SyncStatus =
  "connecting" | "connected" | "reconnecting" | "unavailable";
export interface DocumentChange {
  op: "set" | "remove";
  path: (string | number)[];
  value?: JsonValue;
}
export interface SnapshotEvent extends ProjectEditorState {
  type: "snapshot";
  effectiveRole: ProjectRole;
}
export interface PatchEvent {
  type: "patch";
  projectId: string;
  baseRevision: number;
  revision: number;
  changes: DocumentChange[];
  canUndo: boolean;
  canRedo: boolean;
  effectiveRole: ProjectRole;
}
export type SyncEvent = SnapshotEvent | PatchEvent;

export interface PresenceState {
  cursor: { x: number; y: number } | null;
  selectedElementId: string | null;
  editingElementId: string | null;
}
export interface Participant extends PresenceState {
  sessionId: string;
  userId: string;
  name: string;
  role: ProjectRole;
  lastActivity: string;
}
export interface PresenceEvent {
  type: "presence";
  projectId: string;
  sessionId: string;
  participants: Participant[];
}
export type PresenceConnection = (() => void) & {
  updatePresence: (state: PresenceState) => void;
};

export function applyDocumentChanges(
  document: ProjectDocument,
  changes: DocumentChange[],
): ProjectDocument {
  // Build an independent projection; never partially publish an invalid delta.
  const result = JSON.parse(JSON.stringify(document)) as Record<
    string,
    unknown
  >;
  for (const change of changes) {
    if (!change.path.length || !["set", "remove"].includes(change.op))
      throw new Error("Delta inválido");
    let parent: Record<string | number, unknown> = result;
    for (const segment of change.path.slice(0, -1)) {
      if (
        ["__proto__", "constructor", "prototype"].includes(String(segment)) ||
        !Object.hasOwn(parent, segment)
      )
        throw new Error("Ruta inválida");
      const child = parent[segment];
      if (child === null || typeof child !== "object")
        throw new Error("Ruta inválida");
      parent = child as Record<string | number, unknown>;
    }
    const key = change.path.at(-1)!;
    if (["__proto__", "constructor", "prototype"].includes(String(key)))
      throw new Error("Ruta inválida");
    if (Array.isArray(parent)) {
      if (
        typeof key !== "number" ||
        !Number.isInteger(key) ||
        key < 0 ||
        key > parent.length ||
        (change.op === "remove" && key === parent.length)
      ) {
        throw new Error("Índice inválido");
      }
      if (change.op === "remove") parent.splice(key, 1);
      else parent[key] = change.value;
    } else if (change.op === "remove") {
      if (!Object.hasOwn(parent, key)) throw new Error("Ruta inválida");
      delete parent[key];
    } else {
      parent[key] = change.value;
    }
  }
  return result as unknown as ProjectDocument;
}

const channels = new Map<string, Client>();
export function applyAssistantCommand(
  projectId: string,
  baseRevision: number,
  command: unknown,
): Promise<void> {
  const client = channels.get(projectId);
  if (!client?.connected)
    return Promise.reject(
      new Error("El canal colaborativo está desconectado."),
    );
  const operationId = crypto.randomUUID();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      clean();
      reject(
        new Error(
          "No se confirmó la operación. Actualiza el proyecto antes de reintentar.",
        ),
      );
    }, 15000);
    const ok = client.subscribe(
      `/topic/projects/${projectId}/operations`,
      (m) => {
        const e = JSON.parse(m.body);
        if (e.operationId === operationId) {
          clean();
          resolve();
        }
      },
    );
    const bad = client.subscribe(
      `/user/queue/projects/${projectId}/operations`,
      (m) => {
        const e = JSON.parse(m.body);
        if (e.operationId === operationId) {
          clean();
          reject(new Error(e.message));
        }
      },
    );
    function clean() {
      clearTimeout(timer);
      ok.unsubscribe();
      bad.unsubscribe();
    }
    client.publish({
      destination: `/app/projects/${projectId}/operations`,
      body: JSON.stringify({
        operationId,
        clientId: clientIds.get(projectId),
        projectId,
        baseRevision,
        command,
      }),
    });
  });
}
const clientIds = new Map<string, string>();
export function connectProjectSync(options: {
  projectId: string;
  token: string;
  onEvent: (event: SyncEvent) => boolean;
  onStatus: (status: SyncStatus) => void;
  onForbidden: (code: number) => void;
  onPresence?: (event: PresenceEvent) => void;
  onConversation?: (page: SessionPage) => void;
}): PresenceConnection {
  let stopped = false;
  let timer: ReturnType<typeof setTimeout> | undefined;
  let refreshing = false;
  const id = options.projectId,
    clientId = crypto.randomUUID();
  clientIds.set(id, clientId);
  let participants: Participant[] = [];
  let currentDocument: ProjectDocument | null = null;
  async function refresh() {
    if (refreshing || stopped) return;
    refreshing = true;
    try {
      const document = await getProject(id);
      currentDocument = document;
      if (!stopped)
        options.onEvent({
          type: "snapshot",
          document,
          ...historyState(id),
          effectiveRole: "EDITOR",
        });
    } catch (e) {
      if (!stopped && (e as { status?: number }).status === 403)
        options.onForbidden(4403);
    } finally {
      refreshing = false;
    }
  }
  const client = new Client({
    brokerURL: `${location.protocol === "https:" ? "wss:" : "ws:"}//${location.host}/ws`,
    connectHeaders: { Authorization: `Bearer ${options.token}` },
    reconnectDelay: 3000,
    heartbeatIncoming: 10000,
    heartbeatOutgoing: 10000,
  });
  function publish(type: string, state?: PresenceState) {
    if (!client.connected) return;
    client.publish({
      destination: `/app/projects/${id}/presence`,
      body: JSON.stringify({
        eventId: crypto.randomUUID(),
        clientId,
        type,
        selectedElement: state?.selectedElementId
          ? {
              elementId: state.selectedElementId,
              elementType:
                currentDocument?.umlModel.elements.find(
                  (e) => e.id === state.selectedElementId,
                )?.kind === "class"
                  ? "CLASS"
                  : "RELATIONSHIP",
            }
          : null,
        cursor: state?.cursor ?? null,
      }),
    });
  }
  function presence(body: string) {
    try {
      const e = JSON.parse(body);
      const convert = (p: any): Participant => ({
        sessionId: p.clientId,
        userId: p.actor.id,
        name: p.actor.displayName,
        role: "EDITOR",
        lastActivity: p.joinedAt,
        selectedElementId: p.selectedElement?.elementId ?? null,
        cursor: p.cursor,
        editingElementId: null,
      });
      if (e.participants) participants = e.participants.map(convert);
      else if (e.participant) {
        participants = participants.filter(
          (p) => p.sessionId !== e.participant.clientId,
        );
        if (e.type !== "USER_LEFT") participants.push(convert(e.participant));
      }
      options.onPresence?.({
        type: "presence",
        projectId: id,
        sessionId: clientId,
        participants,
      });
    } catch {
      /* malformed presence is ignored */
    }
  }
  client.onConnect = () => {
    if (stopped) return;
    channels.set(id, client);
    client.subscribe(`/topic/projects/${id}/operations`, () => void refresh());
    client.subscribe(`/topic/projects/${id}/presence`, (m) => presence(m.body));
    client.subscribe(`/user/queue/projects/${id}/presence`, (m) =>
      presence(m.body),
    );
    client.subscribe(`/topic/projects/${id}/assistant`, (m) => {
      try {
        const event = JSON.parse(m.body);
        if (event.projectId === id)
          window.dispatchEvent(
            new CustomEvent("forge:assistant", { detail: event }),
          );
      } catch {}
    });
    publish("USER_JOINED");
    void refresh();
    options.onStatus("connected");
  };
  client.onWebSocketClose = () => {
    if (!stopped) options.onStatus("reconnecting");
  };
  client.onStompError = () => {
    if (!stopped) options.onStatus("unavailable");
  };
  options.onStatus("connecting");
  client.activate();
  const tick = () => {
    void refresh();
    if (!stopped) timer = setTimeout(tick, 2500);
  };
  tick();
  const stop = () => {
    stopped = true;
    clearTimeout(timer);
    publish("USER_LEFT");
    channels.delete(id);
    clientIds.delete(id);
    void client.deactivate();
  };
  let lastPresence = 0;
  stop.updatePresence = (state: PresenceState) => {
    if (Date.now() - lastPresence < 100) return;
    lastPresence = Date.now();
    publish("USER_MOVED_CURSOR", state);
    publish("USER_SELECTED_ELEMENT", state);
  };
  return stop;
}
