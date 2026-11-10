# Forge Studio · interfaz Vue

Interfaz reconstruida a partir de la referencia visual suministrada: Vue 3, Vuetify, Pinia y Vue Flow. El código ejecutable no depende de Angular ni JointJS.

## Ejecutar

Requiere Node 24+, backend Spring en 8082 y MongoDB activo.

```powershell
npm ci
npm run dev
```

Abrir http://127.0.0.1:4200. Vite reenvía `/api` y `/ws` al backend local. `.env.example` documenta la base relativa; no hace falta crear un `.env`.

```powershell
npm run build
npm test
```

## Publicar en Vercel

En Vercel importa el repositorio y configura:

- **Root Directory:** `frontend`
- **Framework Preset:** `Vite`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm ci`

Si el backend está publicado en otra URL, define estas variables en
**Project Settings > Environment Variables**:

```text
VITE_API_BASE_URL=https://tu-backend.example.com/api
VITE_WS_URL=wss://tu-backend.example.com/ws
```

En el backend configura el mismo dominio en
`SINAPUML_CORS_ALLOWED_ORIGINS` y `SINAPUML_WEBSOCKET_ALLOWED_ORIGINS`.
Sin esas variables, Vercel solo sirve la interfaz estática y las llamadas se
intentan hacer contra el mismo dominio de Vercel.

## Integración

`editor-api.ts` transforma los modelos del backend a la proyección visual de Vue Flow y conserva visibilidad, tipos, identificadores, nulabilidad y layout. Las escrituras usan revisión optimista y el backend valida/persiste. Undo/Redo conserva instantáneas durante la sesión y se invalida ante cambios externos; no se mantiene después de recargar.

`editor-sync.ts` usa JWT en STOMP CONNECT para presencia y notificaciones de operaciones. Además consulta el documento cada 2,5 s para recibir guardados REST de otros clientes. Ante desconexión se deshabilita la edición hasta reconectar.

Las herramientas consumen validación, XMI preview/apply/export, generación de aplicaciones, Assistant texto/imagen/audio, conversación, actividad, sesiones e invitaciones reales. El backend admite OWNER/EDITOR, sin rol de solo lectura ni cambio/eliminación de colaboradores. El inspector permite métodos UML con retorno, visibilidad y parámetros; se conservan en el documento y en XMI. Los generadores CRUD adjuntan el diseño con métodos cuando existen, sin inventar cuerpos de lógica de negocio.

La IA necesita sus runtimes locales; su ausencia se muestra como error del servicio. No se incluyen credenciales ni modelos. Los paneles de actividad y diagnóstico muestran la respuesta detallada del backend.

El respaldo del frontend anterior permanece fuera de esta aplicación en `artifacts/frontend-rebuild/`; no participa del build.
