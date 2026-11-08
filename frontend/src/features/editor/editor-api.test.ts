import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  projectView,
  nativeDocument,
  executeProjectCommand,
  undoProject,
  redoProject,
  historyState,
  saveLayouts,
  type NativeProject,
} from "./editor-api";
const { fetchMock } = vi.hoisted(() => ({ fetchMock: vi.fn() }));
vi.mock("../../services/api", () => ({ authenticatedFetch: fetchMock }));
function fixture(id = "project-a"): NativeProject {
  return {
    id,
    name: "Biblioteca",
    accessRole: "OWNER",
    revision: 0,
    createdAt: "2026-11-08",
    updatedAt: "2026-11-08",
    document: {
      schemaVersion: "1.0",
      umlModel: {
        classes: [
          {
            id: "c1",
            name: "Libro",
            attributes: [
              {
                id: "a1",
                name: "id",
                dataType: "UUID",
                customTypeName: null,
                visibility: "PRIVATE",
                nullable: false,
                identifier: true,
              },
              {
                id: "a2",
                name: "estado",
                dataType: "CUSTOM",
                customTypeName: "EstadoLibro",
                visibility: "PUBLIC",
                nullable: true,
                identifier: false,
              },
            ],
          },
        ],
        relationships: [
          {
            id: "r1",
            type: "ASSOCIATION",
            sourceClassId: "c1",
            targetClassId: "c1",
            sourceMultiplicity: { lower: 0, upper: null },
            targetMultiplicity: { lower: 1, upper: 1 },
          },
        ],
      },
      layout: { nodes: { c1: { x: 10, y: 20, width: 280, height: 180 } } },
    },
  };
}
beforeEach(() => {
  fetchMock.mockReset();
});
describe("Adaptación al backend", () => {
  it("conserva tipos custom, identificadores, nulabilidad, multiplicidades ilimitadas y layout", () => {
    const n = fixture();
    expect(nativeDocument(projectView(n))).toEqual(n.document);
  });
  it("conserva métodos, parámetros y visibilidad al guardar la proyección", () => {
    const n = fixture("operations");
    n.document.umlModel.classes[0].operations = [
      {
        id: "op1",
        name: "buscar",
        visibility: "PROTECTED",
        returnType: "Libro",
        parameters: [{ id: "p1", name: "codigo", type: "String" }],
      },
    ];
    expect(nativeDocument(projectView(n))).toEqual(n.document);
  });
  it("guarda con baseRevision y permite deshacer/rehacer sin perder metadatos", async () => {
    let n = fixture("history");
    projectView(n);
    fetchMock.mockImplementation(async (_path: string, init: RequestInit) => {
      const body = JSON.parse(String(init.body));
      expect(body.baseRevision).toBe(n.revision);
      n = { ...n, revision: n.revision + 1, document: body.document };
      return new Response(JSON.stringify(n), { status: 200 });
    });
    const state = await executeProjectCommand(n.id, 0, {
      commandType: "setNodeLayout",
      elementId: "c1",
      layout: { x: 99, y: 88, width: 280, height: 180 },
    });
    expect(state.document.revision).toBe(1);
    expect(state.canUndo).toBe(true);
    expect((await undoProject(n.id, 1)).document.diagramLayout.nodes.c1.x).toBe(
      10,
    );
    expect((await redoProject(n.id, 2)).document.diagramLayout.nodes.c1.x).toBe(
      99,
    );
    expect(n.document.umlModel.classes[0].attributes[0].identifier).toBe(true);
  });
  it("no publica ni agrega historial si el servidor rechaza una revisión", async () => {
    const n = fixture("conflict");
    projectView(n);
    fetchMock.mockResolvedValue(
      new Response(
        JSON.stringify({
          error: "PROJECT_REVISION_CONFLICT",
          message: "Conflicto",
        }),
        { status: 409 },
      ),
    );
    await expect(
      executeProjectCommand(n.id, 0, {
        commandType: "removeElement",
        elementId: "c1",
      }),
    ).rejects.toMatchObject({ code: "PROJECT_REVISION_CONFLICT" });
    expect(historyState(n.id).canUndo).toBe(false);
    expect(nativeDocument(projectView(n)).umlModel.classes).toHaveLength(1);
  });
  it("invalida el historial tras una revisión externa", async () => {
    let n = fixture("remote");
    projectView(n);
    fetchMock.mockImplementation(async (_path: string, init: RequestInit) => {
      n = {
        ...n,
        revision: 1,
        document: JSON.parse(String(init.body)).document,
      };
      return new Response(JSON.stringify(n));
    });
    await executeProjectCommand(n.id, 0, {
      commandType: "setNodeLayout",
      elementId: "c1",
      layout: { x: 1, y: 2, width: 280, height: 180 },
    });
    projectView({ ...n, revision: 2 });
    expect(historyState(n.id)).toEqual({ canUndo: false, canRedo: false });
  });
  it("autoorganiza en un único guardado y un solo paso de deshacer", async () => {
    let n = fixture("layout-batch");
    projectView(n);
    fetchMock.mockImplementation(async (_path: string, init: RequestInit) => {
      const body = JSON.parse(String(init.body));
      n = { ...n, revision: n.revision + 1, document: body.document };
      return new Response(JSON.stringify(n));
    });
    const result = await saveLayouts(n.id, 0, {
      c1: { x: 88, y: 99, width: 280, height: 180 },
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(result.document.revision).toBe(1);
    expect((await undoProject(n.id, 1)).document.diagramLayout.nodes.c1.x).toBe(
      10,
    );
    expect(historyState(n.id).canUndo).toBe(false);
  });
});
