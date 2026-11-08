import { authenticatedFetch } from "../../services/api";

export interface SessionEvent {
  id: string;
  sequence: number;
  kind:
    | "message"
    | "activity"
    | "aiRequest"
    | "aiResult"
    | "voiceRequest"
    | "voiceTranscript"
    | "voiceResult"
    | "adviceRequest"
    | "adviceResult";
  actorId: string;
  actorName: string;
  createdAt: string;
  text?: string;
  action?: string;
  projectRevision?: number;
  elementId?: string | null;
  requestId?: string;
  baseRevision?: number;
  status?:
    | "proposed"
    | "clarify"
    | "unsupported"
    | "failed"
    | "stale"
    | "applied"
    | "answered"
    | "declined";
  adviceMode?: "explain" | "review" | "summary";
  references?: { type: "element" | "event"; id: string; label: string }[];
  coverage?: {
    totalRecordedEvents: number;
    includedEvents: number;
    fromSequence: number | null;
    toSequence: number | null;
    snapshotCursor: number;
    historyTruncated: boolean;
  };
  appliedRevision?: number;
  canApply?: false;
  code?: string;
}
export interface SessionPage {
  projectId: string;
  events: SessionEvent[];
  participants: { userId: string; name: string; joinedAt: string }[];
  cursor: number;
  version: number;
  hasEarlier: boolean;
  hasMore: boolean;
}

export async function sendSessionMessage(
  _projectId: string,
  _id: string,
  _text: string,
): Promise<SessionEvent> {
  throw new Error("Usa la conversación del Asistente en Herramientas.");
}
export async function getEarlierSession(
  _projectId: string,
  _before: number,
): Promise<SessionPage> {
  throw new Error("Consulta las sesiones en Herramientas.");
}

const activityLabels: Record<string, string> = {
  addElement: "agregó un elemento",
  updateElement: "editó un elemento",
  removeElement: "eliminó un elemento",
  setNodeLayout: "movió una clase",
  removeNodeLayout: "quitó una posición",
  undo: "deshizo una operación",
  redo: "rehizo una operación",
};
export function sessionActivityLabel(event: SessionEvent): string {
  return activityLabels[event.action ?? ""] ?? "actualizó el diagrama";
}
