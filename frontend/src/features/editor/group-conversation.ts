export type AssistantMode = "ASK" | "REVIEW" | "EDIT" | "SUMMARY_CURRENT";
export interface SharedPlan {
  summary: string;
  baseRevision: number;
  command: unknown;
}
export interface GroupMessage {
  id: string;
  sequence: number;
  requestId: string;
  authorDisplayName: string;
  role: string;
  type: AssistantMode;
  content: string;
  projectRevision: number;
  createdAt: string;
  plan: SharedPlan | null;
  review?: {
    findings?: { severity: string; message: string; elementRef?: string }[];
  } | null;
}
export function mergeMessages(
  current: GroupMessage[],
  incoming: GroupMessage[],
): GroupMessage[] {
  const items = new Map(current.map((m) => [m.id, m]));
  for (const m of incoming) items.set(m.id, m);
  return [...items.values()].sort(
    (a, b) => a.sequence - b.sequence || a.id.localeCompare(b.id),
  );
}
export function canApplyPlan(
  plan: SharedPlan | null,
  revision: number,
  observer: boolean,
) {
  return !!plan?.command && plan.baseRevision === revision && !observer;
}
