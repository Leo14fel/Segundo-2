<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { request, json, getProject } from "./editor-api";
import { useEditorStore } from "./editor-store";
import { applyAssistantCommand } from "./editor-sync";
import {
  mergeMessages,
  canApplyPlan,
  type GroupMessage,
  type AssistantMode,
} from "./group-conversation";
const props = defineProps<{ observer?: boolean }>();
const store = useEditorStore();
const project = store.projectId!;
const messages = ref<GroupMessage[]>([]),
  mode = ref<AssistantMode>("ASK"),
  content = ref(""),
  error = ref(""),
  sending = ref(false),
  loading = ref(false),
  hasMore = ref(false),
  applying = ref<string | null>(null);
let stopped = false,
  timer: ReturnType<typeof setTimeout> | undefined,
  inFlight = false;
const retry = ref<{
  content: string;
  mode: AssistantMode;
  requestId: string;
} | null>(null);
async function load(earlier = false) {
  if (inFlight) return;
  inFlight = true;
  loading.value = true;
  try {
    const before =
      earlier && messages.value[0]
        ? `&before=${messages.value[0].sequence}`
        : "";
    const page = await request<{ messages: GroupMessage[]; hasMore: boolean }>(
      `/projects/${project}/assistant/messages?limit=50${before}`,
    );
    if (stopped) return;
    messages.value = mergeMessages(messages.value, page.messages);
    if (earlier || messages.value.length <= 50) hasMore.value = page.hasMore;
  } catch (e) {
    if (!stopped) error.value = (e as Error).message;
  } finally {
    inFlight = false;
    loading.value = false;
  }
}
async function send(retryExisting = false) {
  if (sending.value) return;
  const body = retryExisting
    ? retry.value
    : {
        content: content.value.trim(),
        mode: mode.value,
        requestId: crypto.randomUUID(),
      };
  if (!body?.content || (props.observer && body.mode === "EDIT")) return;
  sending.value = true;
  error.value = "";
  retry.value = body;
  try {
    const result = await request<{
      userMessage: GroupMessage;
      assistantMessage: GroupMessage;
    }>(`/projects/${project}/assistant/messages`, json(body));
    if (stopped) return;
    messages.value = mergeMessages(messages.value, [
      result.userMessage,
      result.assistantMessage,
    ]);
    retry.value = null;
    content.value = "";
  } catch (e) {
    if (!stopped) error.value = (e as Error).message;
  } finally {
    sending.value = false;
    void load();
  }
}
async function apply(message: GroupMessage) {
  if (
    !canApplyPlan(
      message.plan,
      store.document?.revision ?? -1,
      !!props.observer,
    ) ||
    applying.value
  )
    return;
  applying.value = message.id;
  error.value = "";
  try {
    await applyAssistantCommand(
      project,
      message.plan!.baseRevision,
      message.plan!.command,
    );
    const document = await getProject(project);
    if (!stopped && store.projectId === project)
      store.applyProjectDocument(document);
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    applying.value = null;
  }
}
function event(e: Event) {
  const data = (e as CustomEvent).detail;
  if (data.projectId === project && data.message)
    messages.value = mergeMessages(messages.value, [data.message]);
}
async function tick() {
  await load();
  if (!stopped) timer = setTimeout(tick, 5000);
}
onMounted(() => {
  window.addEventListener("forge:assistant", event);
  void tick();
});
onUnmounted(() => {
  stopped = true;
  clearTimeout(timer);
  window.removeEventListener("forge:assistant", event);
});
</script>
<template>
  <section aria-label="Conversación grupal con IA">
    <div class="d-flex align-center justify-space-between">
      <h2 class="text-h6">IA del equipo</h2>
      <v-chip size="small">Conversación compartida</v-chip>
    </div>
    <p class="text-caption text-medium-emphasis mb-3">
      Todos los integrantes ven los mensajes. La IA solo actúa cuando alguien lo
      solicita; los cambios requieren confirmación.
    </p>
    <v-alert v-if="error" type="error" variant="tonal" class="mb-3"
      >{{ error
      }}<v-btn v-if="retry" :disabled="sending" @click="send(true)"
        >Reintentar la misma solicitud</v-btn
      ></v-alert
    ><v-btn v-if="hasMore" :loading="loading" @click="load(true)"
      >Mensajes anteriores</v-btn
    >
    <div class="conversation" role="log" aria-live="polite">
      <p v-if="!messages.length && !loading" class="text-medium-emphasis">
        Todavía no hay mensajes. Inicia una pregunta para el equipo.
      </p>
      <article
        v-for="m in messages"
        :key="m.id"
        class="message"
        :class="{ assistant: m.role.toLowerCase() === 'assistant' }"
      >
        <header>
          <strong>{{
            m.role.toLowerCase() === "assistant"
              ? "IA del equipo"
              : m.authorDisplayName
          }}</strong
          ><span
            >{{ m.type }} · revisión {{ m.projectRevision }} ·
            {{ new Date(m.createdAt).toLocaleString() }}</span
          >
        </header>
        <p>{{ m.content }}</p>
        <v-alert
          v-for="(finding, i) in m.review?.findings ?? []"
          :key="i"
          :type="
            finding.severity === 'ERROR'
              ? 'error'
              : finding.severity === 'WARNING'
                ? 'warning'
                : 'info'
          "
          variant="tonal"
          density="compact"
          >{{ finding.message }}</v-alert
        >
        <div v-if="m.plan">
          <p>{{ m.plan.summary }}</p>
          <details>
            <summary>Revisar propuesta</summary>
            <pre>{{ JSON.stringify(m.plan.command, null, 2) }}</pre>
          </details>
          <v-btn
            v-if="!observer"
            :disabled="
              !canApplyPlan(
                m.plan,
                store.document?.revision ?? -1,
                !!observer,
              ) || !!applying
            "
            :loading="applying === m.id"
            @click="apply(m)"
            >Confirmar cambios</v-btn
          ><small v-if="m.plan.baseRevision !== store.document?.revision"
            >Propuesta de otra revisión: solicita una nueva antes de
            aplicar.</small
          >
        </div>
      </article>
    </div>
    <form @submit.prevent="send()">
      <v-select
        v-model="mode"
        label="Qué necesitas"
        :items="[
          { title: 'Preguntar', value: 'ASK' },
          { title: 'Revisar el modelo', value: 'REVIEW' },
          { title: 'Resumir avances', value: 'SUMMARY_CURRENT' },
          ...(!observer ? [{ title: 'Proponer cambios', value: 'EDIT' }] : []),
        ]"
        :disabled="sending"
      /><v-textarea
        v-model="content"
        label="Mensaje para la IA y el equipo"
        rows="2"
        maxlength="4000"
        :disabled="sending"
      /><v-btn
        type="submit"
        color="primary"
        :loading="sending"
        :disabled="!content.trim()"
        >Enviar al grupo</v-btn
      >
    </form>
  </section>
</template>
<style scoped>
.conversation {
  max-height: 480px;
  overflow: auto;
  margin: 16px 0;
}
.message {
  padding: 16px;
  border: 1px solid #304451;
  border-radius: 12px;
  margin: 10px 0;
  background: #14212c;
}
.assistant {
  border-left: 3px solid #35d0ba;
}
header {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: space-between;
}
header span,
small {
  font-size: 11px;
  color: #a8b9c8;
}
p,
pre {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
pre {
  font-size: 12px;
  max-height: 220px;
  overflow: auto;
}
</style>
