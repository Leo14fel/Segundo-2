<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useAuthStore } from "../auth/auth-store";
import {
  pushSupported,
  pushConfiguration,
  pushActive,
  enablePush,
  disablePush,
} from "./browser-push";
const auth = useAuthStore(),
  supported = pushSupported(),
  configured = ref(false),
  active = ref(false),
  busy = ref(false),
  error = ref(""),
  notice = ref("");
let key = "";
onMounted(async () => {
  if (!supported || !auth.token || !auth.user) return;
  try {
    const config = await pushConfiguration(auth.token);
    configured.value = config.enabled;
    key = config.publicKey;
    active.value = await pushActive(auth.user.id);
  } catch (e) {
    error.value = (e as Error).message;
  }
});
async function enable() {
  if (!auth.user || !auth.token) return;
  busy.value = true;
  error.value = "";
  try {
    await enablePush(auth.user.id, auth.token, key);
    active.value = true;
    notice.value =
      "Recibirás avisos en este dispositivo, incluso con la aplicación cerrada si tu navegador lo permite.";
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
async function disable() {
  if (!auth.user) return;
  busy.value = true;
  try {
    await disablePush(auth.user.id, auth.token);
    active.value = false;
    notice.value = "Notificaciones desactivadas en este navegador.";
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
</script>
<template>
  <v-card variant="tonal" class="pa-4 mb-4"
    ><h3 class="text-subtitle-1">Avisos en este dispositivo</h3>
    <p v-if="!supported">
      Web Push no está disponible en este navegador o conexión. Los avisos
      dentro de la aplicación siguen disponibles.
    </p>
    <p v-else-if="!configured">
      Las notificaciones del dispositivo todavía no están configuradas en el
      servidor. Los avisos del proyecto siguen funcionando aquí.
    </p>
    <template v-else
      ><p>
        La activación es opcional. No mostramos contenido del diagrama ni
        conversaciones en la pantalla bloqueada.
      </p>
      <v-btn v-if="!active" :loading="busy" @click="enable"
        >Activar notificaciones</v-btn
      ><v-btn v-else :loading="busy" @click="disable"
        >Desactivar notificaciones</v-btn
      ></template
    ><v-alert v-if="error" type="error" variant="tonal" class="mt-2">{{
      error
    }}</v-alert>
    <p v-if="notice" role="status" class="mt-2">{{ notice }}</p></v-card
  >
</template>
