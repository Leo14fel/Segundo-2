<script setup lang="ts">
import { ref, onMounted } from "vue";
import { request, json } from "./editor-api";
import { useEditorStore } from "./editor-store";
const props = defineProps<{ projectId?: string }>();
const emit = defineEmits<{ accepted: [] }>();
const store = useEditorStore();
interface Invitation {
  id: string;
  projectId: string;
  projectName: string;
  invitedEmail: string;
  status: string;
}
const invitations = ref<Invitation[]>([]),
  email = ref(""),
  error = ref(""),
  notice = ref(""),
  busy = ref(false);
async function load() {
  try {
    invitations.value = await request<Invitation[]>(
      props.projectId
        ? `/projects/${props.projectId}/invitations`
        : "/project-invitations",
    );
  } catch (e) {
    error.value = (e as Error).message;
  }
}
async function send() {
  busy.value = true;
  error.value = "";
  try {
    await request(
      `/projects/${props.projectId}/invitations`,
      json({ email: email.value }),
    );
    email.value = "";
    notice.value = "Invitación enviada";
    await load();
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
async function accept(i: Invitation) {
  busy.value = true;
  try {
    await request(`/project-invitations/${i.id}/accept`, json({}));
    await store.loadProjects();
    await store.openProject(i.projectId);
    emit("accepted");
    await load();
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
async function cancel(i: Invitation) {
  try {
    await request(`/projects/${props.projectId}/invitations/${i.id}`, {
      method: "DELETE",
    });
    await load();
  } catch (e) {
    error.value = (e as Error).message;
  }
}
onMounted(load);
</script>
<template>
  <section>
    <v-alert v-if="error" type="error" variant="tonal">{{ error }}</v-alert
    ><v-alert v-if="notice" type="success" variant="tonal">{{
      notice
    }}</v-alert>
    <form v-if="projectId" @submit.prevent="send">
      <v-text-field
        v-model="email"
        type="email"
        label="Correo del colaborador"
        required
      /><v-btn type="submit" :loading="busy" :disabled="!email" color="primary"
        >Invitar como editor</v-btn
      >
    </form>
    <v-list
      ><v-list-item
        v-for="i in invitations"
        :key="i.id"
        :title="projectId ? i.invitedEmail : i.projectName"
        :subtitle="i.status"
        ><template #append
          ><v-btn
            v-if="!projectId && i.status === 'PENDING'"
            :loading="busy"
            @click="accept(i)"
            >Aceptar</v-btn
          ><v-btn v-if="projectId && i.status === 'PENDING'" @click="cancel(i)"
            >Cancelar</v-btn
          ></template
        ></v-list-item
      ></v-list
    >
    <p v-if="!invitations.length" class="text-medium-emphasis">
      No hay invitaciones pendientes.
    </p>
  </section>
</template>
