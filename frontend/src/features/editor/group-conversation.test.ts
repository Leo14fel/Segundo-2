import { describe, it, expect } from "vitest";
import {
  mergeMessages,
  canApplyPlan,
  type GroupMessage,
} from "./group-conversation";
const m = (id: string, sequence: number, content = id) =>
  ({ id, sequence, content }) as GroupMessage;
describe("Conversación común HTTP + STOMP", () => {
  it("reconcilia eventos duplicados y mensajes recibidos fuera de orden", () => {
    expect(
      mergeMessages(
        [m("b", 2), m("a", 1)],
        [m("b", 2, "actualizado"), m("c", 3)],
      ).map((x) => [x.id, x.content]),
    ).toEqual([
      ["a", "a"],
      ["b", "actualizado"],
      ["c", "c"],
    ]);
  });
  it("conserva historial cargado al llegar una página reciente", () => {
    expect(
      mergeMessages([m("old", 1)], [m("new", 50)]).map((x) => x.sequence),
    ).toEqual([1, 50]);
  });
  it("impide aplicar una propuesta obsoleta o desde la vista móvil", () => {
    const plan = {
      summary: "Crear clase",
      baseRevision: 3,
      command: { type: "CREATE_CLASS" },
    };
    expect(canApplyPlan(plan, 3, false)).toBe(true);
    expect(canApplyPlan(plan, 4, false)).toBe(false);
    expect(canApplyPlan(plan, 3, true)).toBe(false);
    expect(canApplyPlan(null, 3, false)).toBe(false);
  });
});
