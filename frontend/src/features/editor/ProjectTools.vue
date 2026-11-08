<script setup lang="ts">
import GroupAssistant from "./GroupAssistant.vue";
import ProjectHistory from "./ProjectHistory.vue";
import { ref, computed, onUnmounted } from "vue";
import { VoiceCapture } from "./voice-capture";
import { useEditorStore } from "./editor-store";
import {
  request,
  json,
  nativeDocument,
  getProject,
  projectView,
  type NativeProject,
} from "./editor-api";
import { authenticatedFetch } from "../../services/api";
import { applyAssistantCommand } from "./editor-sync";
const props = defineProps<{ observer?: boolean }>();
const store = useEditorStore();
const id = computed(() => store.projectId);
const busy = ref(false),
  error = ref(""),
  notice = ref(""),
  text = ref(""),
  tab = ref(
    new URLSearchParams(window.location.search).get("view") === "activity"
      ? "activity"
      : "assistant",
  ),
  output = ref(""),
  artifact = ref("mi-aplicacion"),
  basePackage = ref("com.example.app"),
  color = ref("#35D0BA"),
  mode = ref("SIMPLE_CRUD");
const authClass = ref<string>(),
  username = ref<string>(),
  password = ref<string>();
const classes = computed(
  () =>
    store.document?.umlModel.elements.filter((e) => e.kind === "class") ?? [],
);
const attributes = computed(() => {
  const c = classes.value.find((c) => c.id === authClass.value);
  return c?.kind === "class" ? c.attributes : [];
});
interface Plan {
  summary: string;
  baseRevision: number;
  command: unknown;
  warnings?: string[];
}
const plan = ref<Plan | null>(null),
  preview = ref<{
    previewToken: string;
    classCount: number;
    attributeCount: number;
    relationshipCount: number;
    diagnostics: unknown[];
  } | null>(null);
async function run(action: () => Promise<void>) {
  busy.value = true;
  error.value = "";
  notice.value = "";
  try {
    await action();
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
async function refresh() {
  if (id.value) store.applyProjectDocument(await getProject(id.value));
}
function path(s: string) {
  return `/projects/${id.value}/${s}`;
}
async function generate() {
  await run(async () => {
    const r = await authenticatedFetch(
      path("generation/spring-boot"),
      json({
        baseRevision: store.document?.revision,
        artifactName: artifact.value,
        basePackage: basePackage.value,
        primaryColor: color.value,
        mode: mode.value,
        useFirstAttributeAsIdentifier: true,
        authClassId: authClass.value,
        usernameAttributeId: username.value,
        passwordAttributeId: password.value,
      }),
    );
    if (!r.ok) {
      const e = await r.json();
      throw new Error(e.message ?? JSON.stringify(e));
    }
    download(await r.blob(), `${artifact.value}.zip`);
    notice.value = "Aplicación generada y descargada.";
  });
}
function download(blob: Blob, name: string) {
  const url = URL.createObjectURL(blob),
    a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
async function validate() {
  await run(async () => {
    output.value = JSON.stringify(
      await request(
        path("validate"),
        json({ document: nativeDocument(store.requireDocument()) }),
      ),
      null,
      2,
    );
  });
}
async function ask() {
  plan.value = null;
  await run(async () => {
    plan.value = await request<Plan>(
      path("assistant/plan"),
      json({ text: text.value }),
    );
  });
}
async function apply() {
  if (!plan.value) return;
  await run(async () => {
    await applyAssistantCommand(
      id.value!,
      plan.value!.baseRevision,
      plan.value!.command,
    );
    plan.value = null;
    await refresh();
    notice.value = "Cambios aplicados.";
  });
}
async function upload(event: Event, kind: "image" | "audio" | "xmi") {
  const input = event.target as HTMLInputElement,
    file = input.files?.[0];
  if (!file) return;
  plan.value = null;
  await run(async () => {
    const body = new FormData();
    body.append(kind === "xmi" ? "file" : kind, file);
    body.append("baseRevision", String(store.document?.revision));
    if (kind === "xmi")
      preview.value = await request(path("xmi/import/preview"), {
        method: "POST",
        body,
      });
    else
      plan.value = await request(
        path(kind === "image" ? "assistant/image/plan" : "assistant/voice"),
        { method: "POST", body },
      );
  });
  input.value = "";
}
async function applyXmi() {
  if (!preview.value) return;
  await run(async () => {
    const n = await request<NativeProject>(
      path("xmi/import/apply"),
      json({ previewToken: preview.value!.previewToken }),
    );
    store.applyProjectDocument(projectView(n));
    preview.value = null;
    notice.value = "XMI importado.";
  });
}
async function query(endpoint: string) {
  await run(async () => {
    output.value = JSON.stringify(await request(path(endpoint)), null, 2);
  });
}
async function rename() {
  await run(async () => {
    const name = window.prompt(
      "Nombre del proyecto",
      String(store.document?.metadata.name ?? ""),
    );
    if (name?.trim()) {
      store.applyProjectDocument(
        projectView(
          await request<NativeProject>(
            `/projects/${id.value}`,
            json({ name: name.trim() }, "PATCH"),
          ),
        ),
      );
      await store.loadProjects();
    }
  });
}
async function advise() {
  await run(async () => {
    const r = await request<{ assistantMessage: { content: string } }>(
      path("assistant/messages"),
      json({
        content: text.value,
        mode: "ASK",
        requestId: crypto.randomUUID(),
      }),
    );
    output.value = r.assistantMessage.content;
  });
}
const recording = ref(false);
const capture = new VoiceCapture(
  10 * 1024 * 1024,
  60,
  (v) => (recording.value = v),
  (audio) => void sendRecordedAudio(audio),
  (message) => (error.value = message),
);
onUnmounted(() => capture.dispose());
async function sendRecordedAudio(audio: Blob) {
  await run(async () => {
    const context = new AudioContext();
    try {
      const decoded = await context.decodeAudioData(await audio.arrayBuffer());
      const offline = new OfflineAudioContext(
        1,
        Math.ceil(decoded.duration * 16000),
        16000,
      );
      const source = offline.createBufferSource();
      source.buffer = decoded;
      source.connect(offline.destination);
      source.start();
      const samples = (await offline.startRendering()).getChannelData(0);
      const buffer = new ArrayBuffer(44 + samples.length * 2),
        view = new DataView(buffer);
      function str(offset: number, value: string) {
        for (let i = 0; i < value.length; i++)
          view.setUint8(offset + i, value.charCodeAt(i));
      }
      str(0, "RIFF");
      view.setUint32(4, 36 + samples.length * 2, true);
      str(8, "WAVE");
      str(12, "fmt ");
      view.setUint32(16, 16, true);
      view.setUint16(20, 1, true);
      view.setUint16(22, 1, true);
      view.setUint32(24, 16000, true);
      view.setUint32(28, 32000, true);
      view.setUint16(32, 2, true);
      view.setUint16(34, 16, true);
      str(36, "data");
      view.setUint32(40, samples.length * 2, true);
      samples.forEach((sample, i) => {
        const value = Math.max(-1, Math.min(1, sample));
        view.setInt16(
          44 + i * 2,
          value < 0 ? value * 32768 : value * 32767,
          true,
        );
      });
      const body = new FormData();
      body.append(
        "audio",
        new Blob([buffer], { type: "audio/wav" }),
        "grabacion.wav",
      );
      plan.value = await request(path("assistant/voice"), {
        method: "POST",
        body,
      });
    } finally {
      await context.close();
    }
  });
}
</script>
<template>
  <v-card class="mt-4" variant="outlined"
    ><v-tabs v-model="tab" color="primary" show-arrows
      ><v-tab value="assistant">Asistente</v-tab
      ><v-tab v-if="!observer" value="generation">Generar app</v-tab
      ><v-tab v-if="!observer" value="project">Proyecto</v-tab
      ><v-tab value="activity">Actividad</v-tab></v-tabs
    ><v-card-text
      ><v-alert v-if="error" type="error" variant="tonal" class="mb-3">{{
        error
      }}</v-alert
      ><v-alert v-if="notice" type="success" variant="tonal" class="mb-3">{{
        notice
      }}</v-alert>
      <div v-if="tab === 'assistant'">
        <GroupAssistant :observer="observer" />
        <div v-if="!observer" class="d-flex flex-wrap ga-4 mt-4">
          <label
            >Imagen → UML<input
              type="file"
              accept="image/*"
              :disabled="busy"
              @change="upload($event, 'image')" /></label
          ><v-btn
            :disabled="busy"
            :color="recording ? 'error' : 'primary'"
            @click="recording ? capture.stop() : capture.start()"
            >{{ recording ? "Detener y transcribir" : "Grabar voz" }}</v-btn
          ><label
            >Audio WAV → UML<input
              type="file"
              accept="audio/wav,.wav"
              :disabled="busy"
              @change="upload($event, 'audio')"
          /></label>
        </div>
        <v-alert
          v-if="plan && !observer"
          type="info"
          variant="tonal"
          class="mt-4"
          ><p>{{ plan.summary }}</p>
          <pre>{{ JSON.stringify(plan.command, null, 2) }}</pre>
          <v-btn
            :disabled="
              busy ||
              !plan.command ||
              plan.baseRevision !== store.document?.revision
            "
            @click="apply"
            >Confirmar cambios</v-btn
          ><v-btn @click="plan = null">Descartar</v-btn>
          <p v-if="plan.baseRevision !== store.document?.revision">
            El proyecto cambió. Solicita una nueva propuesta.
          </p></v-alert
        >
      </div>
      <div v-if="!observer && tab === 'generation'">
        <v-text-field
          v-model="artifact"
          label="Nombre del artefacto"
        /><v-text-field
          v-model="basePackage"
          label="Paquete Java"
        /><v-text-field
          v-model="color"
          label="Color primario (#RRGGBB)"
        /><v-select
          v-model="mode"
          :items="['SIMPLE_CRUD', 'AUTH_INFORMATION_SYSTEM']"
          label="Perfil"
        /><template v-if="mode !== 'SIMPLE_CRUD'"
          ><v-select
            v-model="authClass"
            :items="classes"
            item-title="name"
            item-value="id"
            label="Clase de usuarios" /><v-select
            v-model="username"
            :items="attributes"
            item-title="name"
            item-value="id"
            label="Atributo de usuario" /><v-select
            v-model="password"
            :items="attributes"
            item-title="name"
            item-value="id"
            label="Atributo contraseña" /></template
        ><v-btn color="primary" :loading="busy" @click="generate"
          >Descargar Spring + Angular + Flutter</v-btn
        >
      </div>
      <div v-if="!observer && tab === 'project'">
        <div class="d-flex flex-wrap ga-2">
          <v-btn :disabled="busy" @click="validate">Validar UML</v-btn
          ><v-btn :disabled="busy" @click="rename">Renombrar proyecto</v-btn>
        </div>
        <p class="mt-4">Importar XMI: revisa el resumen antes de confirmar.</p>
        <input
          type="file"
          accept=".xmi,.xml"
          :disabled="busy"
          @change="upload($event, 'xmi')"
        /><v-alert v-if="preview" type="info" class="mt-3"
          >{{ preview.classCount }} clases,
          {{ preview.attributeCount }} atributos,
          {{ preview.relationshipCount }} relaciones.
          <pre>{{ JSON.stringify(preview.diagnostics, null, 2) }}</pre>
          <v-btn :disabled="busy" @click="applyXmi">Confirmar importación</v-btn
          ><v-btn @click="preview = null">Cancelar</v-btn></v-alert
        >
      </div>
      <ProjectHistory v-if="tab === 'activity'" />
      <pre v-if="output" class="result mt-4">{{ output }}</pre>
    </v-card-text></v-card
  >
</template>
<style scoped>
pre {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  font-size: 12px;
  max-height: 360px;
  overflow: auto;
}
.result {
  background: #0f1720;
  padding: 16px;
  border-radius: 12px;
}
input[type="file"] {
  display: block;
  max-width: 100%;
  margin-top: 8px;
}
label {
  font-size: 13px;
}
</style>
