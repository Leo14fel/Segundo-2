# Integraciones del segundo parcial

Corte de trabajo: 8 de noviembre de 2026. Esta bitácora complementa la evaluación de requisitos; no declara aceptación total.

## Cambios implementados

- Chat común con autores, fechas, modos ASK/REVIEW/EDIT/SUMMARY_CURRENT, historial paginado, reconciliación por ID y recepción STOMP. La consulta periódica recupera mensajes perdidos al reconectar.
- Reintento de solicitudes conservando requestId para utilizar la idempotencia del backend. Las propuestas no se aplican por recibir un mensaje: exigen confirmación y revisión vigente.
- Contexto del asistente ampliado con hasta 50 hechos de actividad, autor y revisión, más cobertura total. Se informa al modelo cuando la ventana es incompleta. El resumen no se presenta como una reconstrucción ilimitada ni como los cambios específicos desde la última visita del usuario.
- Vista móvil informativa por ancho hasta 900 px: edición del diagrama y propuestas EDIT deshabilitadas; chat de consulta/revisión/resumen, presencia y avisos disponibles. Es una restricción de experiencia, no un nuevo permiso de seguridad: los permisos de backend siguen siendo OWNER/EDITOR.
- Actividad paginada, sesiones y cierre explícito, continuidad con confirmación de revisión vista, notificaciones y marcado individual/todas.
- Autoorganización guardada como una sola revisión y entrada de Undo/Redo, con validación del backend.
- Script demo-acceptance actualizado para las pruebas Vue existentes.

## Base para diagramas

`docs/formal/forge-studio-componentes.mmd` contiene el diagrama de componentes de la implementación local. Se puede reproducir en Enterprise Architect con componentes, interfaces REST/STOMP, base de datos y dependencias de IA.

El diagrama de despliegue final será distinto: navegador y móvil, entrada HTTPS/WSS, servidor de aplicación, MongoDB replica set en nube y proveedor IA. Todavía no se debe dibujar un despliegue real como entregado: el usuario confirmó que no tiene nube configurada.

Para un diagrama de secuencia usar: usuario envía petición → JWT/permiso → persistir mensaje → publicar al grupo → construir contexto acotado → llamar proveedor → persistir respuesta → publicar al grupo → reconciliar cada cliente. En EDIT agregar propuesta → confirmación → operación con baseRevision → validación → transacción → nueva revisión → propagación. La IA no escribe directamente en MongoDB ni en el canvas.

## Pendientes de aceptación global

- Métodos UML: ampliación manual implementada en el incremento siguiente (dominio, inspector, validación, actividad y XMI). El catálogo de herramientas de IA ya incluye edición de métodos; falta validarlo con proveedor y voz reales y definir generación de cuerpos si se exige. No se consideran inventados a partir de una firma.
- Notificaciones Web Push: implementación incorporada en el incremento final de este documento. Falta configurar claves, HTTPS y aceptación en un dispositivo real; los avisos internos por sí solos no prueban recepción push.
- Nube: cuenta/proveedor/servidor y MongoDB remoto por configurar; no se crearon recursos.
- IA/voz/imagen reales: requieren proveedor o modelos activos y pruebas completas; los tests de gateway no prueban calidad de una inferencia real.
- Recertificación integral de los casos heredados, aplicaciones generadas y pruebas con dos cuentas/dispositivo móvil real.
- Undo/Redo continúa siendo historial de sesión; no persistente entre recargas.

No modificar estados históricos CERRADO hasta contar con evidencia correspondiente a esta versión.

## Verificación de este incremento

- 33 pruebas del backend del asistente aprobadas, incluyendo contexto de actividad/cobertura y rechazo de contexto excesivo.
- Verificación visual del chat grupal, móvil informativo sin edición, actividad con autores, continuidad y sesiones.
- Backend reiniciado con las clases actualizadas; health por el proxy responde UP.
- En esa verificación seguían pendientes las llamadas a IA con modelos reales y push. La implementación posterior de Web Push se describe abajo; su recepción real aún no fue aceptada.

## Incremento: métodos UML

- `UmlClass.operations` es un campo aditivo. Los documentos antiguos sin ese campo se leen con una lista vacía; el constructor anterior continúa disponible para el código existente.
- `UmlOperation` conserva UUID, nombre, visibilidad, retorno opcional y parámetros con UUID/nombre/tipo. void se normaliza como ausencia de retorno.
- Se validan identificadores, nombres de código, tipos simples/arreglo, parámetros sin void, nombres de parámetros repetidos y firmas duplicadas. Se admite sobrecarga con tipos de parámetros diferentes.
- Renombrar clases y modificar atributos mediante comandos existentes conserva los métodos. El guardado manual usa el documento autoritativo con baseRevision; Undo/Redo y sincronización existentes conservan sus datos.
- XMI representa métodos como ownedOperation y parámetros como ownedParameter con dirección in/return. Las direcciones out/inout se rechazan explícitamente porque el modelo no puede conservarlas.
- La actividad distingue añadir, editar y eliminar métodos; el contexto de IA recibe esos hechos a través de la actividad registrada.
- Si hay métodos, el ZIP generado adjunta `uml-design.json` y `UML-METHODS.md`. CRUD/persistencia siguen generándose; las firmas no se convierten en implementaciones arbitrarias de negocio.
- El catálogo de comandos IA se extendió en el incremento posterior, descrito abajo. Su calidad con modelos y voz reales aún requiere aceptación.

### Evidencia del incremento de métodos

- Suite seleccionada de validación, XMI, colaboración, actividad y generación: 164 casos reportados, 0 fallos y 7 omitidos (aceptaciones condicionadas).
- Frontend: 9 pruebas aprobadas y compilación Vite/TypeScript correcta.
- Prueba real por el proxy Vue: proyecto `QA - Metodos UML`, método `disponible(fecha: DATE): BOOLEAN`; guardar y reabrir desde MongoDB conserva UUID y parámetros.
- Export XMI contiene ownedOperation; generación real incluye uml-design.json; actividad registra autoría de la incorporación del método.
- La implementación probada cubre edición manual. No constituye evidencia de creación de métodos por IA/voz ni de ejecución automática de su lógica de negocio.

## Incremento: herramientas de IA para métodos

Se añadió `edit_operation` a los catálogos de llama.cpp y Bedrock. Admite CREATE, UPDATE y DELETE de un método por solicitud y produce la intención `EDIT_OPERATION`. No ejecuta Java ni modifica MongoDB directamente.

El pipeline conserva grounding y normalización y genera un BATCH con `SET_CLASS_OPERATIONS`. Ese comando solo reemplaza métodos: toma nombre y atributos del documento actual, ignorando esos campos en el payload. La validación de dominio se ejecuta antes de ofrecer la propuesta y también en la autoridad colaborativa.

Controles: clase mencionada, firma existente canónica, sobrecargas desambiguadas por firma, nombres/tipos solicitados, IDs nuevos generados en Java, propiedades omitidas conservadas, protección frente a eliminación no solicitada de parámetros y rechazo de solicitudes múltiples que pudieran aplicarse parcialmente.

Ejemplos para probar con un proveedor activo:

- «Agrega el método disponible a Libro con retorno BOOLEAN y parámetro fecha DATE».
- «Renombra el método buscar de Libro a consultar».
- «Modifica el método buscar de Libro con retorno STRING».
- «Modifica el método buscar de Libro sin parámetros».
- «Elimina el método buscar(STRING) de Libro» cuando hay sobrecargas.

La voz comparte el planner después de la transcripción; no hay una segunda implementación de edición de métodos.

Diagrama de secuencia: `docs/formal/ia-metodos-secuencia.mmd`. El flujo de edición desde el chat persiste y publica la propuesta mediante los servicios conversacionales existentes; el endpoint de planner aislado conserva su respuesta de preview.

Disponibilidad observada antes de reiniciar este incremento: llama.cpp, Whisper y visión UNREACHABLE. Por ello los tests de herramientas usan un gateway controlado; no son evidencia de calidad del modelo ni de reconocimiento de voz con micrófono real.

### Evidencia de herramientas IA para métodos

- Regresión de asistente, chat, colaboración y actividad: 314 casos reportados, 0 fallos y 3 omitidos.
- Suite específica final: 11 pruebas de routing, grounding, firmas ambiguas, preservación de datos, rechazo de cambios múltiples y tipos no solicitados.
- Tests de gateway llama.cpp/Bedrock aprobados tras actualizar instrucciones y catálogos; utilizan transporte controlado, no inferencia real.
- Smoke local real `scripts/smoke-methods-stomp.mjs`: autentica una cuenta QA, envía SET_CLASS_OPERATIONS, espera OPERATION_APPLIED, consulta MongoDB por la API y verifica creación/actualización/eliminación de un método temporal. Al terminar conserva los métodos originales; registra actividad normal de estas pruebas.
- Credenciales del smoke se reciben por SINAPUML_TEST_EMAIL / SINAPUML_TEST_PASSWORD. No se guardan en el script. Requiere el proyecto aislado QA - Metodos UML y Node 24 con dependencias frontend instaladas.
- Backend actualizado activo y validación final por STOMP completada. Los runtimes locales siguen sin estar configurados/activos en esta sesión.

## Incremento: Web Push y continuidad del trabajo

Se incorporaron suscripciones autenticadas por dispositivo, cola persistida en la misma transacción que el aviso, trabajador con lease y reintentos, cifrado AES128GCM / VAPID y limpieza de endpoints vencidos. El envío de red ocurre fuera de la transacción. La cola tiene TTL de siete días en un campo BSON Date, compatible con el conversor histórico de Instant a texto.

Vue ofrece activación explícita en Actividad → Avisos. El service worker conserva únicamente el vínculo de cuenta y presenta contenido genérico; valida el destinatario antes de mostrar avisos. La navegación abre el proyecto autorizado y vuelve a consultar la API. Se añadió manifiesto web e iconos; no se implementó cache de datos privados ni una aplicación nativa.

La configuración está desactivada por defecto. `scripts/generate-push-keys.mjs` prepara claves locales ignoradas por Git sin imprimirlas ni sobrescribirlas; el contacto VAPID y HTTPS se configuran antes de la prueba. No se han generado ni publicado credenciales, solicitado permisos en el navegador ni enviado avisos reales a un móvil durante esta etapa.

Guía y criterios de aceptación: `docs/runtime/web-push.md`. Diagramas actualizados: `docs/formal/forge-studio-componentes.mmd` y `docs/formal/web-push-secuencia.mmd`. Punto para otro chat: `CONTINUAR.md` en la raíz.

La verificación conjunta de push, notificaciones, actividad, chat y colaboración reportó 121 pruebas sin fallos ni omisiones; frontend 21 pruebas aprobadas y build correcto. Se comprueba transacción/rollback, deduplicación, aislamiento entre cuentas, TTL BSON Date, entrega desde cambio UML con gateway controlado, reintentos y privacidad del worker. Otras dos pruebas aprobaron el cifrado real y encabezados VAPID con claves efímeras, sin tráfico externo, y el gateway desactivado sin claves. Tras reiniciar, health por el proxy está UP; worker/manifiesto/icono responden 200 y la configuración push está deshabilitada. La aceptación por un proveedor y teléfono reales permanece pendiente.
