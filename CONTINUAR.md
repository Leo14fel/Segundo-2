# Punto de continuación de Forge Studio

Actualizado: 8 de noviembre de 2026. Leer este archivo antes de continuar desde otro chat. Contiene contexto técnico, no credenciales. Comprobar el estado real de archivos y servicios; no asumir que un proceso sigue vivo por lo registrado aquí.

## Objetivo y autorización del usuario

Completar las integraciones del segundo parcial sin perder los casos de uso del primero. Se autorizó revisar, corregir e implementar en este checkout y ejecutar localmente. Mantener documentación y diagramas acordes al código. El usuario **todavía no tiene nube configurada**. No se crearon recursos en nube ni se desplegó la aplicación. No solicitar de nuevo autorización para arreglos locales reversibles.

Requisitos del docente: pizarra UML colaborativa multiusuario; IA compartida por proyecto con autoría/contexto, preguntas/revisión/resumen y cambios solo a pedido; voz para solicitar edición; persistencia obligatoria NoSQL en nube y continuidad; móvil informativo sin editar el diagrama y con notificaciones push. IA local es opcional. No hay conversaciones privadas con IA. Falta contrastar íntegramente el primer parcial y precisar con el docente si toda edición IA debe iniciarse por voz.

## Checkout y precauciones

- Ruta: `C:\Users\Lenovo\Documents\cosas variadas\materias\software 1\SWFT examen 1\sinapuml`.
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
- MongoDB replica set local: `compose.mongo.yml`, puerto 27017, base de desarrollo `sinapuml`. Las transacciones requieren replica set. Las pruebas de integración usan bases separadas.
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
6. Web Push: paquete backend `com.sinapuml.push`, suscripciones autenticadas por usuario, cola transaccional MongoDB, lease, reintentos acotados y cifrado AES128GCM/VAPID. `PushPanel`, `browser-push.ts`, `public/push-sw.js`, manifiesto e iconos. Vinculación de cuenta del worker, payload genérico, navegación segura y desvinculación al salir. Endpoint limitado a proveedores HTTPS exactos y sin redirecciones. Ver runbook.

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
.\gradlew.bat test --tests 'com.sinapuml.push.*' --tests 'com.sinapuml.notification.*' --tests 'com.sinapuml.activity.*' --tests 'com.sinapuml.projectassistant.*' --tests 'com.sinapuml.collaboration.*' --console=plain
# Desde frontend:
npm test
npm run build
```

`scripts/smoke-methods-stomp.mjs` necesita variables SINAPUML_TEST_EMAIL y SINAPUML_TEST_PASSWORD, frontend/node_modules y el proyecto aislado `QA - Metodos UML`. Modifica temporalmente un método y deja actividad normal de QA; no ejecutarlo sobre un proyecto de usuario arbitrario.

## Próximos pasos, por prioridad

Actualización de documentación: el usuario indicó que dispone de Gemini, sin confirmar todavía si es acceso a la aplicación o a Gemini API. Solicitó comenzar las bases de la documentación mediante Google Drive. Se creó un borrador editable enlazado desde `docs/formal/README-segundo-parcial.md`, con una copia Markdown, doce requisitos RF-SP, siete CU-SP provisionales y fuentes iniciales de casos de uso y dominio. No se implementó un adaptador Gemini en este incremento. Completar los datos académicos y contrastar el formato exigido por el docente antes de cerrar el informe.

9 de noviembre: el usuario aportó `C:/Users/Lenovo/Downloads/Documentacion_CASE_Leonardo_V9_FINAL_CON_INDICE_DIAGRAMAS.docx` como referencia para mejorar la base. Se produjo `docs/formal/Documentacion_ForgeStudio_SegundoParcial_Base_V2.docx` con portada y datos reales de la referencia, nueve capítulos, siete casos detallados, siete figuras e índices automáticos, más `documentacion-segundo-parcial-v2.md`. La referencia describía FastAPI/PostgreSQL y otras capacidades no vigentes: se corrigieron a Spring/Mongo y límites reales. El original queda intacto. Drive está conectado a una cuenta distinta de la personal del usuario; no compartir ni suponer el correo de destino. La V2 se entrega localmente y no reemplaza el borrador remoto. Se verificaron 28 páginas con render Word y PNG, índices actualizados y ausencia de campos rotos. No se implementó Gemini ni se crearon recursos cloud al redactar.

1. Configurar un proveedor real de IA y Whisper; verificar chat compartido con dos cuentas y edición de métodos por voz, propuesta, confirmación y propagación. Los tests actuales no demuestran calidad del modelo ni transcripción física.
2. Elegir/configurar nube con el usuario, MongoDB remoto replica set y HTTPS/WSS. No afirmar cumplimiento de nube por tener archivos de despliegue escritos. Evitar crear infraestructura facturable sin alcance/cuenta definidos.
3. Configurar claves VAPID estables y contacto, y probar push en un teléfono con HTTPS. Guía completa en `docs/runtime/web-push.md`. SENT solo prueba aceptación del proveedor, no visualización en el teléfono.
4. Recertificar los CU del primer parcial sobre Vue: dos cuentas/conflictos/reconexión, voz/imagen/XMI, y compilar/ejecutar aplicaciones generadas. Corregir fallos con evidencia. `demo-acceptance.ps1` ya usa npm test.
5. Completar documentación final con evidencias reales. No cambiar estados históricos CERRADO como prueba de la nueva versión. No introducir funciones cosméticas antes de cerrar brechas obligatorias.

Límites: no rol persistente VIEWER ni administración completa de colaboradores; el modo móvil no reemplaza un permiso de backend. Undo/Redo no persiste entre recargas. Autoorganización guarda posiciones por separado. El observador es web, no una app nativa distribuida. Determinar si estas restricciones afectan la rúbrica antes de ampliar alcance.

## Documentos y diagramas

Revisión académica V2 de diagramas: `docs/formal/diagramas-drawio-v2/`, maestro `SinapUML-PUDS-Academico-V2.drawio` y galería `index.html`. El usuario aportó siete capturas para orientar la notación: detalle CU con include/extend, comunicación con símbolos BCE, realización de análisis con clases de tres compartimentos, despliegue con nodos, arquitectura por capas y secuencias con activaciones. Se mantienen las 25 vistas D01–D25 y se añaden siete detalles CU-SP y siete realizaciones AC-SP (39 vistas). Constructor reproducible: `scripts/build-puds-drawio-v2.py`, basado en los hechos del constructor V1 sin reescribir sus entregables. El exportador admite `-DiagramDirectory docs/formal/diagramas-drawio-v2`. Los nombres de controles de AC-SP son conceptuales y su correspondencia con los servicios reales está en la guía. No copiar tecnologías, roles comerciales ni proveedores de nube de las referencias. La versión anterior y el Word V4 se mantienen intactos; las 14 figuras nuevas requieren incorporación y actualización de índices en una siguiente revisión del Word.

Diagramas: el usuario eligió draw.io y se crearon las 25 vistas D01–D25 en `docs/formal/diagramas-drawio/`, con maestro `SinapUML-PUDS.drawio`, XML individuales, PNG y SVG exportados por draw.io Desktop, galería `index.html`, guía y manifest. Constructor: `scripts/build-puds-drawio.py`; exportador: `scripts/export-puds-drawio.ps1`. El constructor reemplaza sus salidas; preservar ediciones manuales antes de regenerar. Las vistas extensas se deben insertar en páginas completas u horizontales, sin comprimirlas en las reservas de tres pulgadas. El Word V4 se conserva intacto. Se identificó al contrastar el código que la propuesta de voz se devuelve al solicitante, mientras la operación confirmada sí se comparte: verificar/completar la difusión grupal de esa propuesta antes de afirmar el cumplimiento integral. No se implementó esa mejora durante este trabajo documental. Nube, IA real y recepción push siguen pendientes de aceptación.

Versión vigente del documento: `docs/formal/Documentacion_SinapUML_PUDS_Con_Diagramas_V5.docx`. A solicitud del usuario se insertaron las 39 vistas académicas V2: 46 láminas con siete secuencias divididas y participantes repetidos, SVG vectorial con respaldo PNG. Texto A4 y láminas A3 horizontales, 39 pies SEQ Figura e índices actualizados mediante Word. Se revisaron las 77 páginas renderizadas; V4 se conserva intacta. Constructor y QA local en `backend/data/documentacion-v5/`. La documentación mantiene pendientes de aceptación IA real, voz, nube y recepción push. No se subió a Drive ni a GitHub.

Versión anterior: `docs/formal/Documentacion_PUDS_V4.docx`. El usuario pidió retirar el nombre anterior y autorizó proponer uno relacionado con IA, colaboración, diagramas y UML: se eligió **SinapUML**. La V4 presenta portada blanca con un único escudo pequeño y tipografías, tablas y pies uniformes; conserva PUDS y las 25 reservas XML. V3 se mantiene intacta. No se renombró la aplicación ni se actualizó Drive en esta etapa. El Markdown V3 es histórico y no está sincronizado con la V4.

Nueva base vigente del 9 de noviembre: `docs/formal/Documentacion_ForgeStudio_PUDS_Base_V3.docx`. El usuario solicitó seguir la estructura PUDS del PDF `C:/Users/Lenovo/Documents/cosas variadas/materias/sistemas de informacion 1/si/documentacion parcial 2.pdf`, sin Ishikawa y dejando espacios para diagramas que se harán en XML. La V3 tiene 25 reservas D01–D25 con título, caption e identificación de archivo previsto; `diagramas-xml-planificados.csv` contiene el inventario y `documentacion-puds-v3.md` el contenido fuente. No se generaron XML ni se eligió un esquema/editor. Se conservó la V2 intacta y no se copiaron nombres, docente, materia ni datos de despliegue del PDF de otra asignatura. Se verifica Word renderizado en 39 páginas con índices, reservas y tablas revisados; no hubo implementación de IA/nube ni cambios de código de aplicación en esta etapa. Antes de dibujar: usar el inventario y confirmar el formato XML del editor.

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

10 de noviembre: el usuario rechazó la presentación del Word V5 y pidió materiales para montar los diagramas manualmente. No tomar V5 como diseño aprobado ni volver a insertarlos automáticamente. Entrega: docs/formal/SinapUML-Para-Montaje-Manual.zip, con V4 intacta, 39 vistas editables, PNG/SVG, galería, GUIA-MONTAJE-MANUAL.md y ubicacion-diagramas.csv (39 correspondencias). El documento conectado de Drive es el borrador inicial de 7 páginas, no el PUDS completo: se renombró a SinapUML, corrigieron datos académicos conocidos y uniformaron tamaños de títulos; tabla a 10 pt con espaciado compacto para evitar dividir RF-SP-11. Se verificó lectura nativa y PDF exportado; no se insertaron diagramas ni se cambiaron permisos. URL: https://docs.google.com/document/d/1MpLWCJMCpJRsIh3P6C-mxb9pXBJ56FlVoayUjlhfiu4 . Para el montaje PUDS usar la V4 local y revisar personalmente las vistas.

10 de noviembre, revisión de subtítulos: el estudiante eligió explícitamente Documentacion_PUDS_V4.docx como mejor base y pidió ampliar subtítulos y establecer jerarquía según referencias. Se produjo docs/formal/Documentacion_SinapUML_PUDS_Subtitulos_V6.docx, a partir de V4 intacta, sin montar diagramas ni usar A3. Encabezados 20/16/14/12.5 pt, 4.3.1–7 para fichas, agrupadores Diagramas de comunicación y Diagramas de secuencia con casos de cuarto nivel, nombres de diseño de arquitectura/datos normalizados. Índice hasta nivel 4 actualizado mediante Word, 41 páginas renderizadas e inspeccionadas, tablas y 25 reservas preservadas. QA/constructor en backend/data/documentacion-v6/. No editar Drive por esta solicitud de un archivo local; V5 permanece rechazada. La nueva V6 se entrega para revisión, sin presumir aprobación del estudiante.

10 de noviembre, teoría y diagramas compactos: el usuario aprobó la base V6 y pidió ampliar teoría y preparar diagramas para corregirlos antes del montaje, con tamaño reducido dentro de A4. Nueva docs/formal/Documentacion_SinapUML_PUDS_Teoria_V7.docx, 45 páginas revisadas, 18 subsecciones de teoría (2027 palabras de desarrollo), ocho referencias primarias añadidas. Conserva formato y tablas de V6, siete fichas, 25 reservas y captions; no se insertaron nuevas figuras. V6 permanece intacta. Constructor/QA en backend/data/documentacion-v7/. Nuevos diagramas: docs/formal/diagramas-drawio-v3-compactos/, 39 códigos en 53 láminas nativas al dividir vistas densas, maestro SinapUML-PUDS-Compactos-V3.drawio, XML/PNG/SVG, galería, guías, control-revision.csv y tamano-insercion.csv. ZIP docs/formal/SinapUML-Diagramas-Compactos-V3.zip verificado. Se inspeccionaron las 53 láminas y corrigieron superposiciones y rutas de conectores. Tamaño de inserción proporcional máximo 16 cm de ancho y 11.3 cm de alto; letra estimada actual alrededor de 9 pt. Los modelos son borradores de revisión, pendientes de correcciones del estudiante y validación de notación. Cuando devuelva su .drawio corregido, exportar desde esa fuente e insertar por código en una nueva copia del Word, actualizar pies e índices, sin A3 ni figuras enormes. No regenerar la carpeta V3 sobre ediciones manuales sin respaldo. No se modificó la aplicación, Drive ni GitHub.

10 de noviembre, montaje aprobado de casos de uso: versión vigente docs/formal/Documentacion_SinapUML_PUDS_Casos_Uso_V8.docx, derivada de V7 intacta. Se insertaron siete detalles CU-SP y D03 en dos partes (9 imágenes), únicamente los casos de uso aprobados por el estudiante. A4, proporción conservada, máximo 16 × 11.3 cm; índices actualizados y 53 páginas revisadas visualmente. Comunicación D07–D13, dominio D14 y secuencia D19–D25 fueron rechazados por falta de detalle: corregir CON el estudiante antes de insertarlos. Otras vistas siguen pendientes de aprobación. Estado explícito en docs/formal/estado-revision-diagramas.md. No se regeneraron las fuentes editables ni se modificaron Drive, GitHub o la aplicación. QA local en backend/data/documentacion-v8/.
10 de noviembre: nuevas referencias nativas del estudiante inspeccionadas (paquetes, despliegue, comunicación y análisis de clase). Primera revisión editable de 29 vistas en docs/formal/diagramas-revision-referencias-v4/SinapUML-Revision-Referencias-V4.drawio. Recupera detalle académico V2 y reconstruye comunicaciones con acceso explícito. Borrador pendiente de revisión conjunta y QA visual completa; NO insertado en V8 ni aprobado. Constructor scripts/build-puds-reference-v4.py, inventario de referencias backend/data/referencias-puds/inventario.json. Preservar Word V8 y casos de uso aprobados.
Comunicación V5: usuario pidió reorganizar D007–D013 como su segunda captura. Nuevos archivos independientes con nombres descriptivos y maestro 00-SinapUML-Comunicacion-D007-D013.drawio en docs/formal/comunicacion-corregida-v5/. Actor/vista/control/entidades alineados, flechas de mensajes separadas de enlaces, proveedores externos explícitos. ZIP SinapUML-Comunicacion-D007-D013-V5.zip. D007 equivale a D07 del Word; correspondencia.json contiene el mapeo. Word V8 sin cambios; revisión del usuario pendiente. Constructor scripts/build-communication-v5.py.

Montaje V9 autorizado por el estudiante: docs/formal/Documentacion_SinapUML_PUDS_Diagramas_V9.docx es la versión vigente. Fuente V8 preservada. Se incorporaron D04–D25 y siete AC-SP (29 figuras nuevas). Comunicación utiliza EXACTAMENTE los siete PNG revisados en docs/formal/comunicacion-corregida-v5/de comunicacion/, no las exportaciones antiguas. Verificados hashes de cada imagen embebida. 39 imágenes contando portada y casos previos; 39 captions SEQ (D01/D02 son reservas), 49 páginas A4 vertical revisadas, índices actualizados. Figuras proporcionales máximo 15.8 × 8.7 cm, en línea, sin saltos manuales de figura. Retirados saltos heredados de fichas; tablas fluyen por filas con encabezados repetidos y unidos a primera fila. D01 y D02 no estaban en carpeta autorizada: permanecen reservados. Exportaciones draw.io escala 2 recortaban contenido; resuelto con --zoom 1 --scale 1. Fuentes editables e imágenes originales no se modificaron. QA/constructor backend/data/documentacion-v9/, final-r7.pdf y render-r7 internos; entregar solo DOCX. No cambios en Drive, GitHub ni aplicación.
