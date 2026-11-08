# Punto de continuación de Forge Studio

Actualizado: 8 de noviembre de 2026. Leer este archivo antes de continuar desde otro chat. Contiene contexto técnico, no credenciales. Comprobar el estado real de archivos y servicios; no asumir que un proceso sigue vivo por lo registrado aquí.

## Objetivo y autorización del usuario

Completar las integraciones del segundo parcial sin perder los casos de uso del primero. Se autorizó revisar, corregir e implementar en este checkout y ejecutar localmente. Mantener documentación y diagramas acordes al código. El usuario **todavía no tiene nube configurada**. No se crearon recursos en nube ni se desplegó la aplicación. No solicitar de nuevo autorización para arreglos locales reversibles.

Requisitos del docente: pizarra UML colaborativa multiusuario; IA compartida por proyecto con autoría/contexto, preguntas/revisión/resumen y cambios solo a pedido; voz para solicitar edición; persistencia obligatoria NoSQL en nube y continuidad; móvil informativo sin editar el diagrama y con notificaciones push. IA local es opcional. No hay conversaciones privadas con IA. Falta contrastar íntegramente el primer parcial y precisar con el docente si toda edición IA debe iniciarse por voz.

## Checkout y precauciones

- Ruta: `C:\Users\Lenovo\Documents\cosas variadas\materias\software 1\SWFT examen 1\classforge`.
- La migración autorizada a Vue eliminó fuentes del antiguo Angular y añadió las integraciones del segundo parcial. **No usar reset/clean ni restaurar masivamente archivos antiguos.** Revisar `git status --short` antes de editar.
- Repositorio elegido por el usuario: `https://github.com/Leo14fel/Segundo-2`. El remoto de publicación es `origin`. Se preparó como un historial independiente, con un único commit inicial de Leo14fel y sin padres de la historia anterior. Continuar los próximos commits desde esta nueva rama main; no mezclar ni publicar ramas del historial previo.
- Antes de reemplazar la historia local se guarda un bundle de respaldo en `backend/data/git-history-backups/`, ignorado por Git. Es únicamente para recuperación local y no forma parte de la publicación.
- Referencia Vue: `artifacts/frontend-rebuild/reference/frontend`. Respaldo de fuentes anteriores: `artifacts/frontend-rebuild/frontend-original-source.zip`.
- El frontend real de la herramienta es Vue. Los generadores aún pueden producir aplicaciones Angular y Flutter: eso no implica que el frontend de la herramienta siga siendo Angular.
- No agregar contraseñas, JWT, claves VAPID privadas ni credenciales cloud a archivos versionados. `backend/data/` está ignorado por Git.

## Stack y ejecución local

- Backend: Java 21 / Spring Boot 4.0.8 / Gradle Wrapper 9.2. Puerto 8082, REST `/api`, WebSocket/STOMP `/ws`.
- JDK instalado: `C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot`.
- Frontend: Vue 3, Vuetify, Pinia, Vue Flow, Vite y TypeScript. Node 24; ejecutables en `C:\Program Files\nodejs`. Puerto 4200, proxy al backend.
- MongoDB replica set local: `compose.mongo.yml`, puerto 27017, base de desarrollo `classforge`. Las transacciones requieren replica set. Las pruebas de integración usan bases separadas.
- Última verificación: backend reiniciado con Web Push incluido; `/api/health` por Vite respondió UP. URL local: http://127.0.0.1:4200. No memorizar PIDs: identificar proceso por command line y ruta antes de detenerlo.
- No se reinició Docker ni se borraron volúmenes durante este incremento. Los runtimes locales de IA/Whisper/visión se habían observado UNREACHABLE; comprobarlos de nuevo antes de aceptar esos flujos.

Terminal backend desde la raíz:

```powershell
docker compose -f compose.mongo.yml up -d --wait
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot'
Set-Location backend
.\gradlew.bat bootRun --console=plain
```

En otra terminal, desde la raíz:

```powershell
Set-Location frontend
npm ci # solo si faltan dependencias o cambió el lockfile
npm run dev
```

No iniciar otro servidor si el puerto ya está ocupado. Para crear cuentas usar registro de la aplicación; el perfil demo y sus datos se describen en `docs/runtime/cu27-demo.md`.

## Implementado en los incrementos recientes

1. Nuevo frontend de referencia adaptado a autenticación, proyectos, modelado manual, validación, XMI y generación. Revisión optimista al guardar; reconciliación del documento cada 2,5 s y STOMP para presencia/operaciones del asistente. Undo/Redo es de sesión y se invalida con cambios externos.
2. `GroupAssistant.vue`: conversación común persistida y reconciliada, autores, modos ASK/REVIEW/EDIT/SUMMARY_CURRENT, paginación/deduplicación, requestId conservado al reintentar y confirmación de propuestas con revisión. Contexto del backend incluye UML, miembros, mensajes recientes y hasta 50 hechos de actividad con autores/cobertura.
3. `ProjectHistory.vue`: actividad, sesiones, visitas, continuidad y avisos con lectura/paginación. Móvil hasta 900 px funciona como observador sin edición del UML. Falta aceptación física del dispositivo.
4. Métodos UML: `UmlOperation`/`UmlParameter`, inspector, dominio compatible con documentos antiguos, validación, persistencia, actividad y XMI ownedOperation/ownedParameter. Renombrar clases y editar atributos conserva métodos. ZIP con métodos incluye `uml-design.json` y `UML-METHODS.md`; no inventa cuerpos de negocio.
5. Herramienta IA `edit_operation` CREATE/UPDATE/DELETE: grounding, sobrecargas desambiguadas, preservación de valores omitidos, tipos/nombres pedidos y rechazo de cambios múltiples. Produce `SET_CLASS_OPERATIONS`, que solo modifica métodos. Tests de gateways usan transporte controlado, no inferencia real. Voz usa el mismo pipeline después de transcribir.
6. Web Push: paquete backend `com.classforge.push`, suscripciones autenticadas por usuario, cola transaccional MongoDB, lease, reintentos acotados y cifrado AES128GCM/VAPID. `PushPanel`, `browser-push.ts`, `public/push-sw.js`, manifiesto e iconos. Vinculación de cuenta del worker, payload genérico, navegación segura y desvinculación al salir. Endpoint limitado a proveedores HTTPS exactos y sin redirecciones. Ver runbook.

Web Push está **desactivado por defecto**, sin claves/contacto configurados, sin permisos solicitados ni recepción real probada. `scripts/generate-push-keys.mjs` puede preparar un archivo local ignorado sin imprimir ni sobrescribir claves; todavía no se ejecutó para configurar este entorno. No activar permisos de notificaciones o micrófono durante QA sin que el usuario participe.

## Evidencia y comandos de pruebas

Último incremento:

- 121 pruebas backend de push/notificaciones/actividad/chat/colaboración: 0 fallos, 0 omitidas.
- 2 pruebas adicionales: cifrado real con claves efímeras y encabezados VAPID, sin tráfico externo; gateway desactivado sin claves. Aprobadas.
- 21 pruebas frontend, TypeScript y build Vite: aprobados. Advertencia de chunk de Vuetify ~608 kB sin gzip, no error.
- Integración MongoDB comprueba rollback/commit de cola, deduplicación, BSON Date para TTL y evento de cambio UML hasta entrega con gateway controlado. Tests del worker verifican cuentas, contenido genérico y navegación segura; tests del navegador verifican consentimiento y cambio de cuenta.
- Verificación HTTP local tras reiniciar: health UP, push enabled=false y publicKey vacío, service worker/manifiesto/icono 192 con HTTP 200. No equivale a recepción push real.

Incrementos anteriores: regresión asistente/chat/colaboración/actividad de 314 casos sin fallos (3 omitidos); 11 tests específicos de métodos IA; suite de métodos/validación/XMI/generación de 164 casos sin fallos (7 omitidos); smoke real STOMP para crear/actualizar/eliminar un método temporal conservando originales. No sumar estas cifras como si fueran casos únicos.

```powershell
# Desde backend, con JAVA_HOME configurado:
.\gradlew.bat test --tests 'com.classforge.push.*' --tests 'com.classforge.notification.*' --tests 'com.classforge.activity.*' --tests 'com.classforge.projectassistant.*' --tests 'com.classforge.collaboration.*' --console=plain
# Desde frontend:
npm test
npm run build
```

`scripts/smoke-methods-stomp.mjs` necesita variables CLASSFORGE_TEST_EMAIL y CLASSFORGE_TEST_PASSWORD, frontend/node_modules y el proyecto aislado `QA - Metodos UML`. Modifica temporalmente un método y deja actividad normal de QA; no ejecutarlo sobre un proyecto de usuario arbitrario.

## Próximos pasos, por prioridad

1. Configurar un proveedor real de IA y Whisper; verificar chat compartido con dos cuentas y edición de métodos por voz, propuesta, confirmación y propagación. Los tests actuales no demuestran calidad del modelo ni transcripción física.
2. Elegir/configurar nube con el usuario, MongoDB remoto replica set y HTTPS/WSS. No afirmar cumplimiento de nube por tener archivos de despliegue escritos. Evitar crear infraestructura facturable sin alcance/cuenta definidos.
3. Configurar claves VAPID estables y contacto, y probar push en un teléfono con HTTPS. Guía completa en `docs/runtime/web-push.md`. SENT solo prueba aceptación del proveedor, no visualización en el teléfono.
4. Recertificar los CU del primer parcial sobre Vue: dos cuentas/conflictos/reconexión, voz/imagen/XMI, y compilar/ejecutar aplicaciones generadas. Corregir fallos con evidencia. `demo-acceptance.ps1` ya usa npm test.
5. Completar documentación final con evidencias reales. No cambiar estados históricos CERRADO como prueba de la nueva versión. No introducir funciones cosméticas antes de cerrar brechas obligatorias.

Límites: no rol persistente VIEWER ni administración completa de colaboradores; el modo móvil no reemplaza un permiso de backend. Undo/Redo no persiste entre recargas. Autoorganización guarda posiciones por separado. El observador es web, no una app nativa distribuida. Determinar si estas restricciones afectan la rúbrica antes de ampliar alcance.

## Documentos y diagramas

- `docs/runtime/integraciones-segundo-parcial.md`: implementación incremental y evidencia.
- `docs/runtime/evaluacion-requisitos-segundo-parcial.md`: matriz actualizada y CU heredados.
- `docs/runtime/frontend-vue-migration.md`: migración y límites.
- `docs/runtime/web-push.md`: configuración/aceptación push.
- `docs/formal/forge-studio-componentes.mmd`: arquitectura real con push.
- `docs/formal/ia-metodos-secuencia.mmd`: solicitud y confirmación de métodos IA.
- `docs/formal/web-push-secuencia.mmd`: suscripción, cola, envío y apertura.

## Texto para iniciar otro chat

«Continúa este proyecto. Lee CONTINUAR.md y docs/runtime/integraciones-segundo-parcial.md, revisa git status y retoma los pendientes prioritarios. Conserva los cambios existentes y no des por completados los casos de uso sin evidencia. Mi siguiente consulta/tarea es: …»

Abrir el nuevo chat en este mismo proyecto/carpeta. El historial completo no debe suponerse disponible automáticamente; estos archivos y el código permiten recuperar el estado. Un límite de uso de la cuenta es distinto del espacio de contexto: abrir otro chat no aumenta por sí mismo la cuota.
