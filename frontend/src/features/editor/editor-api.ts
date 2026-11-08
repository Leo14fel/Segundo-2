import { authenticatedFetch } from "../../services/api";
import type {
  ProjectDocument,
  ProjectEditorState,
  ProjectSummary,
  ProjectCollaborator,
  ProjectRole,
  UmlCommand,
  UmlClass,
  UmlRelationship,
} from "./types";
export class EditorApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly code?: string,
  ) {
    super(message);
  }
}
export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await authenticatedFetch(path, init);
  if (!response.ok) {
    const e = await response.json().catch(() => ({}));
    throw new EditorApiError(
      e.message ?? e.detail?.message ?? `Error ${response.status}`,
      response.status,
      e.error ?? e.code,
    );
  }
  return response.status === 204 ? (undefined as T) : response.json();
}
export function json(body: unknown, method = "POST"): RequestInit {
  return {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
}
export interface NativeAttribute {
  id: string;
  name: string;
  dataType: string;
  customTypeName: string | null;
  visibility: string;
  nullable: boolean;
  identifier: boolean;
}
export interface NativeOperation {
  id: string;
  name: string;
  visibility: string;
  returnType: string | null;
  parameters: { id: string; name: string; type: string }[];
}
export interface NativeClass {
  id: string;
  name: string;
  attributes: NativeAttribute[];
  operations?: NativeOperation[];
}
export interface NativeRelationship {
  id: string;
  type: string;
  sourceClassId: string;
  targetClassId: string;
  sourceMultiplicity: { lower: number; upper: number | null } | null;
  targetMultiplicity: { lower: number; upper: number | null } | null;
}
export interface NativeDocument {
  schemaVersion: string;
  umlModel: { classes: NativeClass[]; relationships: NativeRelationship[] };
  layout: ProjectDocument["diagramLayout"];
}
export interface NativeProject {
  id: string;
  name: string;
  accessRole: "OWNER" | "EDITOR";
  revision: number;
  document: NativeDocument;
  createdAt: string;
  updatedAt: string;
}
const originals = new Map<string, NativeProject>();
const histories = new Map<
  string,
  { undo: NativeDocument[]; redo: NativeDocument[]; revision: number }
>();
const copy = <T>(value: T): T => JSON.parse(JSON.stringify(value));
export function projectView(n: NativeProject): ProjectDocument {
  const cached = originals.get(n.id);
  if (cached && cached.revision > n.revision) return projectView(cached);
  originals.set(n.id, copy(n));
  const classes: UmlClass[] = n.document.umlModel.classes.map((c) => ({
    id: c.id,
    name: c.name,
    kind: "class",
    visibility: "public",
    operations: (c.operations ?? []).map((op) => ({
      ...copy(op),
      kind: "operation" as const,
      visibility: op.visibility.toLowerCase() as "public",
    })),
    attributes: c.attributes.map((a) => ({
      id: a.id,
      kind: "attribute",
      name: a.name,
      type: a.customTypeName ?? a.dataType,
      visibility: a.visibility.toLowerCase() as "public",
      nullable: a.nullable,
      identifier: a.identifier,
    })),
  }));
  const relationships: UmlRelationship[] =
    n.document.umlModel.relationships.map((r) => ({
      id: r.id,
      kind: r.type.toLowerCase() as "association",
      sourceId: r.sourceClassId,
      targetId: r.targetClassId,
      sourceMultiplicity: r.sourceMultiplicity
        ? {
            lower: r.sourceMultiplicity.lower,
            upper: r.sourceMultiplicity.upper ?? "*",
          }
        : { lower: 0, upper: "*" },
      targetMultiplicity: r.targetMultiplicity
        ? {
            lower: r.targetMultiplicity.lower,
            upper: r.targetMultiplicity.upper ?? "*",
          }
        : { lower: 0, upper: "*" },
    }));
  let ownerId = "";
  try {
    const token = localStorage.getItem("forge-studio.access-token");
    if (n.accessRole === "OWNER" && token)
      ownerId = JSON.parse(atob(token.split(".")[1]!)).sub;
  } catch {
    /* no session */
  }
  return {
    id: n.id,
    ownerId,
    metadata: { name: n.name },
    revision: n.revision,
    createdAt: n.createdAt,
    updatedAt: n.updatedAt,
    umlModel: { elements: [...classes, ...relationships] },
    diagramLayout: copy(n.document.layout),
  };
}
export function nativeDocument(d: ProjectDocument): NativeDocument {
  const previous = originals.get(d.id)?.document;
  const supported = [
    "STRING",
    "INTEGER",
    "LONG",
    "DECIMAL",
    "BOOLEAN",
    "DATE",
    "DATETIME",
    "UUID",
  ];
  return {
    schemaVersion: previous?.schemaVersion ?? "1.0",
    umlModel: {
      classes: d.umlModel.elements
        .filter((e): e is UmlClass => e.kind === "class")
        .map((c) => {
          return {
            id: c.id,
            name: c.name,
            ...(c.operations.length
              ? {
                  operations: c.operations.map((op) => ({
                    id: op.id,
                    name: op.name,
                    visibility: op.visibility.toUpperCase(),
                    returnType:
                      op.returnType?.trim() &&
                      op.returnType.toLowerCase() !== "void"
                        ? op.returnType
                        : null,
                    parameters: copy(op.parameters),
                  })),
                }
              : {}),
            attributes: c.attributes.map((a) => {
              const old = previous?.umlModel.classes
                .flatMap((c) => c.attributes)
                .find((x) => x.id === a.id);
              const type =
                old?.dataType === "CUSTOM" && old.customTypeName === a.type
                  ? "CUSTOM"
                  : a.type.toUpperCase();
              return {
                id: a.id,
                name: a.name,
                dataType: supported.includes(type) ? type : "CUSTOM",
                customTypeName: supported.includes(type) ? null : a.type,
                visibility: a.visibility.toUpperCase(),
                nullable: a.nullable ?? old?.nullable ?? false,
                identifier: a.identifier ?? old?.identifier ?? false,
              };
            }),
          };
        }),
      relationships: d.umlModel.elements
        .filter((e): e is UmlRelationship => e.kind !== "class")
        .map((r) => ({
          id: r.id,
          type: r.kind.toUpperCase(),
          sourceClassId: r.sourceId,
          targetClassId: r.targetId,
          sourceMultiplicity:
            r.kind === "generalization"
              ? null
              : {
                  lower: r.sourceMultiplicity.lower,
                  upper:
                    r.sourceMultiplicity.upper === "*"
                      ? null
                      : r.sourceMultiplicity.upper,
                },
          targetMultiplicity:
            r.kind === "generalization"
              ? null
              : {
                  lower: r.targetMultiplicity.lower,
                  upper:
                    r.targetMultiplicity.upper === "*"
                      ? null
                      : r.targetMultiplicity.upper,
                },
        })),
    },
    layout: copy(d.diagramLayout),
  };
}
export function historyState(id: string) {
  const h = histories.get(id);
  if (h && h.revision !== originals.get(id)?.revision) {
    histories.delete(id);
    return { canUndo: false, canRedo: false };
  }
  return { canUndo: !!h?.undo.length, canRedo: !!h?.redo.length };
}
export async function createProject(metadata: Record<string, string>) {
  return projectView(
    await request<NativeProject>(
      "/projects",
      json({ name: metadata.name ?? "Nuevo proyecto" }),
    ),
  );
}
export async function getProject(id: string) {
  return projectView(await request<NativeProject>(`/projects/${id}`));
}
export async function listProjects(): Promise<ProjectSummary[]> {
  return (await request<NativeProject[]>("/projects")).map((n) => ({
    id: n.id,
    ownerId: "",
    metadata: { name: n.name },
    revision: n.revision,
    createdAt: n.createdAt,
    updatedAt: n.updatedAt,
    effectiveRole: "EDITOR",
  }));
}
export async function saveNative(
  id: string,
  revision: number,
  document: NativeDocument,
): Promise<ProjectDocument> {
  return projectView(
    await request<NativeProject>(
      `/projects/${id}/document`,
      json(
        { baseRevision: revision, document, operationId: crypto.randomUUID() },
        "PUT",
      ),
    ),
  );
}
export async function executeProjectCommand(
  id: string,
  revision: number,
  command: UmlCommand,
): Promise<ProjectEditorState> {
  const n = originals.get(id);
  if (!n || n.revision !== revision)
    throw new EditorApiError(
      "Actualiza el proyecto antes de editar.",
      409,
      "PROJECT_REVISION_CONFLICT",
    );
  const d = projectView(copy(n));
  const elements = d.umlModel.elements;
  if (command.commandType === "addElement") {
    if (elements.some((e) => e.id === command.element.id))
      throw new Error("Identificador duplicado");
    elements.push(copy(command.element));
  }
  if (command.commandType === "updateElement") {
    const i = elements.findIndex((e) => e.id === command.elementId);
    if (i < 0) throw new Error("Elemento inexistente");
    elements[i] = copy(command.element);
  }
  if (command.commandType === "removeElement") {
    d.umlModel.elements = elements.filter(
      (e) =>
        e.id !== command.elementId &&
        (e.kind === "class" ||
          (e.sourceId !== command.elementId &&
            e.targetId !== command.elementId)),
    );
    delete d.diagramLayout.nodes[command.elementId];
  }
  if (command.commandType === "setNodeLayout")
    d.diagramLayout.nodes[command.elementId] = copy(command.layout);
  if (command.commandType === "removeNodeLayout")
    delete d.diagramLayout.nodes[command.elementId];
  const document = await saveNative(id, revision, nativeDocument(d));
  let h = histories.get(id);
  if (!h || h.revision !== revision) h = { undo: [], redo: [], revision };
  h.undo.push(copy(n.document));
  h.redo = [];
  h.revision = document.revision;
  histories.set(id, h);
  return { document, ...historyState(id) };
}
async function travel(
  id: string,
  revision: number,
  undo: boolean,
): Promise<ProjectEditorState> {
  const h = histories.get(id),
    n = originals.get(id);
  if (!h || !n || h.revision !== revision) {
    histories.delete(id);
    throw new Error(
      "El historial se reinició porque el proyecto cambió en otra sesión.",
    );
  }
  const from = undo ? h.undo : h.redo,
    to = undo ? h.redo : h.undo;
  const target = from.at(-1);
  if (!target) throw new Error("Sin operaciones disponibles");
  const document = await saveNative(id, revision, target);
  from.pop();
  to.push(copy(n.document));
  h.revision = document.revision;
  return { document, ...historyState(id) };
}
export const undoProject = (id: string, revision: number) =>
  travel(id, revision, true);
export const redoProject = (id: string, revision: number) =>
  travel(id, revision, false);
export async function downloadProjectXmi(id: string) {
  const r = await authenticatedFetch(`/projects/${id}/xmi/export`);
  if (!r.ok) throw new Error("No se pudo exportar el XMI");
  return { blob: await r.blob(), filename: "modelo.xmi" };
}
export async function importProjectXmi(
  _file: File,
): Promise<{ document: ProjectDocument; warnings: string[] }> {
  throw new Error(
    "Abre un proyecto y usa Importar XMI en Herramientas para revisar y confirmar la importación.",
  );
}
export async function listCollaborators(
  id: string,
): Promise<ProjectCollaborator[]> {
  const r = await request<{
    owner: ProjectCollaborator;
    editors: ProjectCollaborator[];
  }>(`/projects/${id}/collaborators`);
  return [r.owner, ...r.editors];
}
export async function addCollaborator(
  id: string,
  email: string,
  _role: ProjectRole,
): Promise<ProjectCollaborator> {
  await request(`/projects/${id}/invitations`, json({ email }));
  throw new Error(
    "Invitación enviada. El destinatario debe aceptarla en Mis invitaciones.",
  );
}
export async function updateCollaborator(
  _id: string,
  _user: string,
  _role: ProjectRole,
): Promise<ProjectCollaborator> {
  throw new Error(
    "Los colaboradores tienen rol EDITOR; el backend no permite cambiarlo.",
  );
}
export async function removeCollaborator(
  _id: string,
  _user: string,
): Promise<void> {
  throw new Error("El backend no ofrece eliminación de colaboradores.");
}

/** One revision and one undo entry for the entire layout operation. */
export async function saveLayouts(
  id: string,
  revision: number,
  layouts: ProjectDocument["diagramLayout"]["nodes"],
): Promise<ProjectEditorState> {
  const n = originals.get(id);
  if (!n || n.revision !== revision)
    throw new EditorApiError(
      "El proyecto cambió. Actualiza antes de organizar.",
      409,
      "PROJECT_REVISION_CONFLICT",
    );
  const next = copy(n.document);
  Object.assign(next.layout.nodes, copy(layouts));
  const document = await saveNative(id, revision, next);
  let h = histories.get(id);
  if (!h || h.revision !== revision) h = { undo: [], redo: [], revision };
  h.undo.push(copy(n.document));
  h.redo = [];
  h.revision = document.revision;
  histories.set(id, h);
  return { document, ...historyState(id) };
}
