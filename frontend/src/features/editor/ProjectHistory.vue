<script setup lang="ts">
import PushPanel from "../notifications/PushPanel.vue";
import { ref, onMounted, onUnmounted } from "vue";
import { request, json } from "./editor-api";
import { useEditorStore } from "./editor-store";
const store = useEditorStore(),
  project = store.projectId!;
interface Activity {
  id: string;
  actorDisplayName: string;
  description: string;
  revisionAfter: number;
  createdAt: string;
}
interface Session {
  id: string;
  status: string;
  summary: string;
  startedAt: string;
  totalChanges: number;
  participants: { displayName: string }[];
}
interface Notice {
  id: string;
  title: string;
  message: string;
  read: boolean;
  createdAt: string;
}
interface Page<T> {
  items: T[];
  totalPages: number;
}
const tab = ref("activity"),
  page = ref(0),
  totalPages = ref(0),
  activities = ref<Activity[]>([]),
  sessions = ref<Session[]>([]),
  notices = ref<Notice[]>([]),
  error = ref(""),
  busy = ref(false),
  actor = ref(""),
  unreadOnly = ref(false),
  unreadCount = ref(0);
const continuity = ref<{
  firstVisit: boolean;
  lastSeenRevision: number;
  currentRevision: number;
  newActivityCount: number;
  activities: Activity[];
} | null>(null);
let stopped = false,
  timer: ReturnType<typeof setTimeout> | undefined,
  serial = 0;
async function load() {
  const ticket = ++serial;
  busy.value = true;
  error.value = "";
  try {
    const kind = tab.value;
    let result: Page<Activity> | Page<Session> | Page<Notice>;
    if (kind === "activity") {
      result = await request<Page<Activity>>(
        `/projects/${project}/activities?page=${page.value}&size=10${actor.value ? "&actorId=" + encodeURIComponent(actor.value) : ""}`,
      );
      if (ticket !== serial || stopped) return;
      activities.value = result.items;
    } else if (kind === "sessions") {
      result = await request<Page<Session>>(
        `/projects/${project}/sessions?page=${page.value}&size=10`,
      );
      if (ticket !== serial || stopped) return;
      sessions.value = result.items;
    } else {
      result = await request<Page<Notice>>(
        `/notifications?projectId=${project}&page=${page.value}&size=10&unreadOnly=${unreadOnly.value}`,
      );
      if (ticket !== serial || stopped) return;
      notices.value = result.items;
    }
    totalPages.value = result.totalPages;
  } catch (e) {
    if (ticket === serial && !stopped) error.value = (e as Error).message;
  } finally {
    if (ticket === serial) busy.value = false;
  }
}
async function select(value: unknown) {
  tab.value = String(value);
  page.value = 0;
  await load();
}
async function acknowledge() {
  try {
    await request(
      `/projects/${project}/visits`,
      json({ revision: store.document?.revision }),
    );
    await context();
  } catch (e) {
    error.value = (e as Error).message;
  }
}
async function context() {
  const value = await request<typeof continuity.value>(
    `/projects/${project}/since-last-visit`,
  );
  if (!stopped) continuity.value = value;
}
async function read(id?: string) {
  try {
    await request(
      id
        ? `/notifications/${id}/read`
        : `/notifications/read-all?projectId=${project}`,
      json({}),
    );
    await load();
    await count();
  } catch (e) {
    error.value = (e as Error).message;
  }
}
async function count() {
  const result = await request<{ totalElements: number }>(
    `/notifications?projectId=${project}&unreadOnly=true&size=1`,
  );
  if (!stopped) unreadCount.value = result.totalElements;
}
async function close(id: string) {
  try {
    await request(`/projects/${project}/sessions/${id}/close`, json({}));
    await load();
  } catch (e) {
    error.value = (e as Error).message;
  }
}
async function tick() {
  try {
    await count();
  } catch {}
  if (!stopped) timer = setTimeout(tick, 5000);
}
onMounted(() => {
  void load();
  void context().catch((e) => (error.value = e.message));
  void tick();
});
onUnmounted(() => {
  stopped = true;
  ++serial;
  clearTimeout(timer);
});
</script>
<template>
  <section aria-label="Actividad y continuidad">
    <v-alert v-if="error" type="error" variant="tonal">{{ error }}</v-alert
    ><v-card v-if="continuity" variant="tonal" class="mb-4 pa-4"
      ><h3>
        {{
          continuity.firstVisit
            ? "Bienvenido al proyecto"
            : "Desde tu última visita"
        }}
      </h3>
      <p>
        {{ continuity.newActivityCount }} cambios registrados · revisión
        {{ continuity.lastSeenRevision }} → {{ continuity.currentRevision }}
      </p>
      <ul>
        <li v-for="a in continuity.activities.slice(0, 5)" :key="a.id">
          {{ a.actorDisplayName }}: {{ a.description }}
        </li>
      </ul>
      <v-btn class="mt-2" @click="acknowledge"
        >Marcar revisión actual como vista</v-btn
      ></v-card
    ><v-tabs :model-value="tab" show-arrows @update:model-value="select"
      ><v-tab value="activity">Actividad</v-tab
      ><v-tab value="sessions">Sesiones</v-tab
      ><v-tab value="notifications">Avisos ({{ unreadCount }})</v-tab></v-tabs
    ><v-btn class="my-3" :loading="busy" @click="load">Actualizar</v-btn
    ><template v-if="tab === 'activity'"
      ><v-text-field
        v-model="actor"
        label="Filtrar por ID de integrante (opcional)"
        clearable
        @keyup.enter="
          page = 0;
          load();
        "
      /><v-list
        ><v-list-item
          v-for="a in activities"
          :key="a.id"
          :title="a.description"
          :subtitle="`${a.actorDisplayName} · revisión ${a.revisionAfter} · ${new Date(a.createdAt).toLocaleString()}`"
      /></v-list>
      <p v-if="!activities.length && !busy">
        Sin actividad para este filtro.
      </p></template
    ><template v-if="tab === 'sessions'"
      ><v-card
        v-for="s in sessions"
        :key="s.id"
        variant="outlined"
        class="pa-3 mb-3"
        ><h3>
          {{ s.status === "OPEN" ? "Sesión en curso" : "Sesión cerrada" }}
        </h3>
        <p>
          {{ s.summary || "Trabajo colaborativo" }} ·
          {{ s.totalChanges }} cambios
        </p>
        <p>
          {{ new Date(s.startedAt).toLocaleString() }} ·
          {{ s.participants.map((p) => p.displayName).join(", ") }}
        </p>
        <v-btn v-if="s.status === 'OPEN'" @click="close(s.id)"
          >Cerrar sesión de trabajo</v-btn
        ></v-card
      >
      <p v-if="!sessions.length && !busy">
        Sin sesiones registradas.
      </p></template
    ><template v-if="tab === 'notifications'"
      ><PushPanel /><v-checkbox
        v-model="unreadOnly"
        label="Solo no leídas"
        @update:model-value="
          page = 0;
          load();
        "
      /><v-btn @click="read()">Marcar todas como leídas</v-btn
      ><v-card
        v-for="n in notices"
        :key="n.id"
        class="pa-3 my-3"
        variant="outlined"
        ><h3>{{ n.title }}</h3>
        <p>{{ n.message }}</p>
        <small>{{ new Date(n.createdAt).toLocaleString() }}</small
        ><v-btn v-if="!n.read" @click="read(n.id)">Marcar leída</v-btn
        ><v-chip v-else size="small">Leída</v-chip></v-card
      >
      <p v-if="!notices.length && !busy">
        No hay avisos para mostrar.
      </p></template
    >
    <div class="d-flex align-center ga-3 mt-3">
      <v-btn
        :disabled="busy || page === 0"
        @click="
          page--;
          load();
        "
        >Anterior</v-btn
      ><span>Página {{ page + 1 }} de {{ Math.max(1, totalPages) }}</span
      ><v-btn
        :disabled="busy || page + 1 >= totalPages"
        @click="
          page++;
          load();
        "
        >Siguiente</v-btn
      >
    </div>
  </section>
</template>
