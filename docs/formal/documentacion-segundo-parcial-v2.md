# Forge Studio Base académica V2

## Índice de diagramas

## Resumen

Forge Studio es una herramienta CASE web para modelar diagramas de clases y mantener un trabajo colaborativo por proyecto. El segundo parcial amplía la participación de la inteligencia artificial: la conversación, las revisiones y los resúmenes deben ser comunes al equipo, y las modificaciones se proponen a pedido, se validan y se aplican únicamente después de confirmarlas.

Esta base describe el frontend Vue y el backend Spring Boot con persistencia MongoDB replica set. Integra la especificación de la experiencia móvil informativa, la continuidad de las sesiones y los avisos Web Push. Distingue implementación, pruebas locales y aceptación real: todavía no están verificados el despliegue en nube, el uso de un proveedor de IA real, la voz con micrófono y la recepción push en un teléfono.

Versión 0.2 de trabajo al 9 de noviembre de 2026. No es un informe final de cumplimiento. El documento de referencia se utiliza para la organización académica y la portada; sus afirmaciones sobre FastAPI, PostgreSQL y permisos VIEWER no se trasladan a esta implementación.

Palabras clave: herramienta CASE, UML, colaboración, IA grupal, PUDS, Vue, Spring Boot, MongoDB, Web Push.

## Abstract

Forge Studio is a collaborative web CASE tool for class diagram modeling. Its second assessment scope adds a shared AI conversation, contextual reviews, progress summaries, and requested diagram changes that require explicit confirmation. The implementation uses Vue, Spring Boot, and a MongoDB replica set. This working documentation separates implemented features from acceptance evidence. Cloud deployment, a real AI provider, physical voice input, and push reception on a phone remain pending validation.

## Introducción

El diseño de software distribuido necesita una representación común y un registro que permita explicar qué cambió y quién participó. Cuando cada integrante consulta una IA de forma individual, el razonamiento y las propuestas pueden quedar fuera del conocimiento del equipo. El sistema propuesto concentra el diagrama, la conversación y los hechos de actividad alrededor del proyecto.

La consigna del segundo parcial exige conservar el alcance del primero, utilizar persistencia NoSQL en nube y ofrecer una experiencia móvil de consulta. Esta documentación toma la transcripción del docente como fuente de requisitos y el código del repositorio como fuente de implementación. Ante diferencias con documentos anteriores prevalece la evidencia de la versión actual.

## Capítulo 1 Perfil del proyecto

### 1.1 Antecedentes y problema

La herramienta dispone de modelado manual, validación, interoperabilidad XMI y generación de aplicaciones. El nuevo problema consiste en integrar a la IA como un participante consultivo compartido y mantener la coordinación de personas que trabajan desde ubicaciones y dispositivos diferentes.

La situación deseada es que un integrante pueda preguntar, revisar, solicitar una modificación o retomar la sesión sin perder el contexto disponible. Ninguna respuesta de IA debe eludir las reglas del dominio ni escribir de manera autónoma sobre el documento.

Fuente: elaboración propia a partir del código y de los requisitos. Vista de alcance, no evidencia de despliegue.

Figura 1. Contexto de la herramienta CASE colaborativa.

### 1.2 Objetivos

Objetivo general: desarrollar y documentar una herramienta CASE colaborativa que integre asistencia de IA grupal y permita construir, conservar y consultar diagramas de clases con autoría y control de cambios.

Conservar y recertificar los casos de uso obligatorios del primer parcial.

Mantener una conversación IA compartida con participantes, actividad y contexto acotado.

Validar propuestas y aplicar cambios solo por solicitud y confirmación explícitas.

Persistir el trabajo en NoSQL en nube y comprobar pausa y reanudación.

Ofrecer observación móvil en tiempo real y notificaciones push aceptadas en un teléfono.

### 1.3 Alcance y justificación

El alcance comprende identidad, proyectos, colaboración, clases, atributos, métodos, parámetros, relaciones, XMI, generación heredada, conversación IA, actividad, sesiones y avisos. No se afirma ejecución automática de cuerpos de negocio a partir de firmas UML. La aplicación Flutter generada y el observador móvil del CASE son productos distintos.

### 1.4 Metodología PUDS

La documentación se organiza por requisitos, análisis, diseño, implementación y pruebas, siguiendo la estructura PUDS de la referencia. Cada incremento debe vincular un requisito con su caso de uso, componentes, cambios y evidencia. Los cierres de ciclos anteriores se conservan como antecedentes y no certifican la nueva versión.

| Etapa de trabajo | Resultado verificable |
| --- | --- |
| Inicio | Alcance y requisitos contrastados con ambas consignas. |
| Elaboración | Casos, arquitectura y riesgos priorizados. |
| Construcción | Incrementos con validación y pruebas reproducibles. |
| Transición | Demo, nube, móvil y documentación aceptados. |

### 1.5 Recursos y planificación

Se requiere un equipo con Java 21, Node 24 y acceso a MongoDB replica set. No se documenta una GPU o memoria específica porque no se ha verificado el hardware de esta computadora. Las fechas de hitos deben acordarse; no se presentan duraciones ni costos no medidos.

## Capítulo 2 Fundamentos tecnológicos

### 2.1 CASE y modelado UML

Una herramienta CASE apoya actividades de ingeniería mediante modelos y transformaciones. UML aporta una notación para clases, atributos, operaciones y relaciones [1]. La aplicación implementa un subconjunto definido; no declara compatibilidad total con todo UML 2.5.1.

La semántica del modelo se mantiene separada de su layout. Un método conserva nombre, visibilidad, retorno y parámetros; la ausencia de retorno representa void. Una relación identifica ambos extremos y sus multiplicidades. Los identificadores permiten conservar referencias aunque cambie un nombre.

### 2.2 Colaboración y concurrencia

La revisión del proyecto evita que una escritura obsoleta reemplace silenciosamente cambios ajenos. El frontend guarda manualmente mediante REST y consulta el documento autoritativo cada 2,5 segundos. STOMP transporta presencia y operaciones del asistente. No se afirma que todo gesto de edición manual sea un comando STOMP.

### 2.3 IA y contexto compartido

El proveedor recibe el modelo, integrantes y contexto reciente autorizado. ASK, REVIEW y SUMMARY_CURRENT generan respuestas sin editar el UML; EDIT produce una propuesta. El servidor valida referencias y tipos antes de habilitar su confirmación. El contexto no es ilimitado: incluye hasta 20 mensajes recientes y 50 hechos de actividad.

### 2.4 NoSQL y avisos

MongoDB permite mantener el documento de proyecto con su modelo embebido. Las transacciones coordinan cambios que involucran actividad, sesiones o notificaciones [3]. Web Push complementa los avisos internos: necesita una suscripción del navegador y un proveedor de entrega, no solamente un WebSocket abierto.

### 2.5 Plataforma implementada

| Capa | Tecnología y responsabilidad |
| --- | --- |
| Presentación | Vue 3, TypeScript, Vuetify y Pinia. |
| Pizarra | Vue Flow y layout separado del modelo. |
| Backend | Java 21, Spring Boot 4.0.8 y Gradle Wrapper. |
| Persistencia | MongoDB replica set; transacciones e índices. |
| Seguridad | JWT, BCrypt y permisos OWNER/EDITOR. |
| Asistencia | Adaptadores llama.cpp y Bedrock; Whisper para voz. |
| Avisos del dispositivo | Service worker, PushManager, cifrado VAPID y cola persistente. |

Gemini fue indicado por el estudiante como una opción disponible. Aún no se confirmó si dispone de acceso API y el código no incorpora un adaptador Gemini. Disponer de la aplicación Gemini no acredita por sí mismo una integración del backend.

## Capítulo 3 Especificación de requisitos de software

### 3.1 Propósito y restricciones

Los requisitos siguientes se derivan de la transcripción del docente. Son una base de trabajo que debe contrastarse con la consigna original del primer parcial. Se utiliza el prefijo RF-SP para evitar sustituir identificadores heredados. Implementado significa código disponible; aceptado exige evidencia del escenario completo.

| ID | Requisito | Criterio de aceptación |
| --- | --- | --- |
| RF-SP-01 | Conservar el primer parcial | Recertificar su catálogo y ejecutar los artefactos generados. |
| RF-SP-02 | Identidad y permisos | Rechazar acceso de cuentas ajenas a un proyecto. |
| RF-SP-03 | Colaboración en tiempo real | Dos cuentas convergen tras cambios, conflicto y reconexión. |
| RF-SP-04 | Conversación IA grupal | Persistir mensajes y respuestas con autoría y visibilidad común. |
| RF-SP-05 | Edición por voz a pedido | Transcribir, proponer, confirmar y propagar una edición válida. |
| RF-SP-06 | Revisión del diseño | Explicar hallazgos sobre elementos existentes sin editar. |
| RF-SP-07 | Resumen de avances | Resumir hechos disponibles y reconocer cobertura limitada. |
| RF-SP-08 | Contexto con participantes | Relacionar autoría y actividad sin inventar hechos. |
| RF-SP-09 | NoSQL en nube | Conservar y retomar una sesión con almacenamiento remoto. |
| RF-SP-10 | Continuidad registrada | Recuperar diagrama, conversación y actividad al volver. |
| RF-SP-11 | Móvil informativo | Observar cambios y actividad sin edición del UML en esa vista. |
| RF-SP-12 | Avisos push | Recibir el aviso por un cambio ajeno y abrir el proyecto autorizado. |

### 3.2 Requisitos de calidad e interfaces

RNF-01 Seguridad: autenticar llamadas, validar permisos y mantener claves fuera del repositorio público.

RNF-02 Consistencia: validar el documento y la revisión antes de confirmar una modificación.

RNF-03 Recuperación: conservar datos tras recarga y reconciliar el estado al reconectar.

RNF-04 Privacidad: los avisos push muestran contenido genérico, no diagramas, mensajes o tokens.

RNF-05 Despliegue: utilizar HTTPS/WSS y MongoDB remoto con transacciones antes de aceptar nube.

No se fijan cifras de latencia, disponibilidad o usuarios simultáneos sin acuerdo ni medición. El API usa JSON; la voz se envía como WAV; XMI se importa con preview y validación. Las credenciales del proveedor permanecen en el backend.

### 3.3 Reglas de negocio

RN-01 La conversación IA es por proyecto y compartida, sin chats privados con el modelo.

RN-02 Consultar, revisar o resumir no cambia el diagrama.

RN-03 Una edición requiere solicitud, confirmación, permiso y baseRevision vigente.

RN-04 La consigna exige voz para pedir cambios de IA; aclarar con el docente si además admite texto.

RN-05 El observador móvil es un modo de interfaz y no un rol VIEWER persistido.

RN-06 Undo/Redo es de sesión; no se documenta como historial persistente entre recargas.

## Capítulo 4 Captura de requisitos

### 4.1 Actores y catálogo

| Actor | Responsabilidad |
| --- | --- |
| Visitante | Registrar una cuenta e iniciar sesión. |
| Propietario | Administrar su proyecto e invitar colaboradores. |
| Colaborador EDITOR | Modelar y consultar proyectos compartidos. |
| Integrante móvil | Observar el proyecto desde la interfaz informativa. |
| Proveedor de IA | Responder o proponer acciones estructuradas. |
| Transcripción y push | Convertir voz y entregar avisos del dispositivo. |

La numeración CU-01 a CU-31 del repositorio se conserva. La referencia utiliza otra numeración de once casos y no se copia para evitar conflictos. Los siete CU-SP siguientes amplían el catálogo; sus identificadores aún requieren aprobación académica.

Fuente: elaboración propia a partir del código y de los requisitos. Es un mapa de alcance. La fuente PlantUML conserva la notación de actores y casos de uso.

Figura 2. Mapa funcional de los casos del segundo parcial.

### 4.2 Especificaciones detalladas

#### CU-SP-01 Consultar a la IA grupal

| Campo | Especificación |
| --- | --- |
| Requisito relacionado | RF-SP-04 y RF-SP-08 |
| Actor principal | Integrante con permiso de edición |
| Precondiciones | Proyecto abierto y proveedor disponible. |
| Estado de aceptación | Implementación y pruebas controladas; falta proveedor real. |

Flujo principal:

1. Escribe una pregunta en la conversación común.

2. El backend registra la solicitud con autor y requestId.

3. Construye el contexto autorizado y consulta al proveedor.

4. Guarda la respuesta y la publica para los integrantes.

5. Los clientes reconcilian el historial compartido.

Alternativas y excepciones: Si el proveedor falla se informa y se permite reintentar. El mismo requestId evita duplicar una respuesta ya completada.

Postcondición: Mensaje y respuesta quedan en el historial del proyecto; el UML no cambia.

Criterio de aceptación: Dos cuentas ven el mismo intercambio con su autoría.

#### CU-SP-02 Solicitar revisión del diagrama

| Campo | Especificación |
| --- | --- |
| Requisito relacionado | RF-SP-06 |
| Actor principal | Integrante con acceso de edición |
| Precondiciones | Documento actual disponible y modelo IA operativo. |
| Estado de aceptación | Falta aceptación de calidad con un modelo real. |

Flujo principal:

1. Selecciona REVIEW y solicita la revisión.

2. El backend toma una instantánea y registra su revisión.

3. La IA analiza el contexto y devuelve observaciones.

4. Se filtran referencias inexistentes y hallazgos inválidos.

5. El sistema comparte la revisión y su vínculo con la instantánea.

Alternativas y excepciones: Una observación con referencia inventada se descarta. Una respuesta no estructurada puede presentarse como texto sin atribuir hallazgos inexistentes.

Postcondición: Existe una revisión compartida; no se aplica una corrección automática.

Criterio de aceptación: La revisión no incrementa la revisión del documento ni cambia sus elementos.

#### CU-SP-03 Solicitar un resumen de lo avanzado

| Campo | Especificación |
| --- | --- |
| Requisito relacionado | RF-SP-07 y RF-SP-08 |
| Actor principal | Integrante que retoma el trabajo |
| Precondiciones | Proyecto accesible y proveedor IA configurado. |
| Estado de aceptación | Falta escenario completo con dos cuentas e IA real. |

Flujo principal:

1. Abre la conversación común y selecciona SUMMARY_CURRENT.

2. El backend reúne UML, miembros, mensajes y actividad reciente.

3. Comunica al proveedor la cobertura y los límites del contexto.

4. Guarda y publica el resumen para el equipo.

5. El integrante contrasta el resumen con la actividad del proyecto.

Alternativas y excepciones: Si no hay hechos anteriores se informa. Si el historial es parcial, no se presenta como un relato exhaustivo.

Postcondición: Queda un resumen compartido sin modificaciones al UML.

Criterio de aceptación: Un integrante que llega tarde entiende los hechos disponibles sin autorías inventadas.

#### CU-SP-04 Solicitar y confirmar edición por voz

| Campo | Especificación |
| --- | --- |
| Requisito relacionado | RF-SP-05 |
| Actor principal | Propietario o colaborador EDITOR |
| Precondiciones | Micrófono autorizado, transcripción e IA disponibles. |
| Estado de aceptación | Pendiente voz/modelo reales y verificación de la traza grupal de la propuesta de voz. |

Flujo principal:

1. Solicita grabar una orden y concede permiso si corresponde.

2. El cliente captura audio y envía WAV para transcripción.

3. El planner interpreta el texto usando el catálogo actual.

4. Se validan referencias, intención, tipos y propuesta.

5. El integrante revisa y confirma la propuesta.

6. La autoridad comprueba permisos y baseRevision, persiste y propaga el cambio.

Alternativas y excepciones: Audio inválido, servicio caído, instrucción ambigua o revisión obsoleta generan rechazo. Cancelar la propuesta conserva el documento.

Postcondición: El cambio aceptado tiene revisión y autoría; los demás clientes recuperan el estado.

Criterio de aceptación: Demostrar voz real, preview, confirmación y convergencia sin escrituras autónomas.

#### CU-SP-05 Retomar una sesión registrada

| Campo | Especificación |
| --- | --- |
| Requisito relacionado | RF-SP-09 y RF-SP-10 |
| Actor principal | Integrante autorizado |
| Precondiciones | Existe un proyecto persistido al que tiene acceso. |
| Estado de aceptación | Implementado localmente; nube y recuperación entre dispositivos pendientes. |

Flujo principal:

1. Inicia sesión y abre el proyecto.

2. Recupera el documento y su revisión actual.

3. Consulta sesiones, actividad y novedades desde la última visita.

4. Puede consultar el resumen compartido de IA.

5. Registra la visita y continúa trabajando.

Alternativas y excepciones: Una cuenta ajena no accede. Un fallo de red no se presenta como pérdida confirmada de información.

Postcondición: Se recupera el trabajo autorizado y se conserva la continuidad registrada.

Criterio de aceptación: Pausar y retomar desde otro dispositivo con MongoDB remoto.

#### CU-SP-06 Observar el proyecto desde un móvil

| Campo | Especificación |
| --- | --- |
| Requisito relacionado | RF-SP-03 y RF-SP-11 |
| Actor principal | Integrante en movimiento |
| Precondiciones | Sesión iniciada y acceso al proyecto desde un teléfono. |
| Estado de aceptación | Modo responsive implementado; aceptación física pendiente. |

Flujo principal:

1. Abre la interfaz informativa móvil.

2. Consulta el diagrama y los participantes.

3. Recibe la evolución mediante sincronización y reconciliación.

4. Consulta conversación, actividad y avisos disponibles.

5. Al reconectar recupera la versión autoritativa.

Alternativas y excepciones: Sin conexión se comunica el estado y se intenta reconciliar. La interfaz no ofrece edición UML en esta experiencia.

Postcondición: El integrante puede seguir la sesión sin editar desde el modo móvil.

Criterio de aceptación: Probar un teléfono real, cambios de otra cuenta y reconexión.

#### CU-SP-07 Activar y recibir avisos push

| Campo | Especificación |
| --- | --- |
| Requisito relacionado | RF-SP-12 |
| Actor principal | Integrante con dispositivo compatible |
| Precondiciones | HTTPS, claves VAPID, sesión y soporte push configurados. |
| Estado de aceptación | Implementado y probado con transporte controlado; recepción real pendiente. |

Flujo principal:

1. Activa avisos desde el panel y concede permiso explícito.

2. El cliente registra una suscripción vinculada a su cuenta.

3. Un cambio de otro integrante crea aviso y trabajo en una transacción.

4. El trabajador envía el payload cifrado al proveedor.

5. El service worker verifica destinatario y muestra un aviso genérico.

6. Al pulsarlo abre el proyecto y verifica nuevamente el acceso.

Alternativas y excepciones: Permiso denegado conserva los avisos internos. HTTP 404/410 elimina la suscripción vencida; los otros fallos tienen reintentos acotados.

Postcondición: Se registra el resultado de envío y se puede consultar el proyecto autorizado.

Criterio de aceptación: Recepción visible en un teléfono, apertura correcta y desvinculación al salir.

## Capítulo 5 Análisis

### 5.1 Paquetes y responsabilidades

| Paquete o área | Responsabilidad |
| --- | --- |
| Identidad y acceso | Autenticación, pertenencia y permisos por proyecto. |
| Proyecto y validación | Documento UML y reglas del dominio. |
| Colaboración | Presencia y operaciones con revisión autoritativa. |
| Asistente | Conversación, contexto, routing y propuestas. |
| Actividad y sesiones | Hechos, continuidad, visitas y avisos. |
| Interoperabilidad y generación | XMI y producción de artefactos. |
| Push | Suscripciones, cola y trabajador de entrega. |

### 5.2 Modelo de dominio

Project contiene un ProjectDocument con UmlModel y DiagramLayout. El modelo agrupa clases y relaciones; las clases agrupan atributos y operaciones; cada operación conserva parámetros. Los mensajes IA se asocian por projectId y tienen autor, secuencia, tipo y revisión relacionada. Esta vista no implica una colección MongoDB por clase UML.

Fuente: elaboración propia a partir del código y de los requisitos. Las fuentes Mermaid detallan atributos y multiplicidades; no se representa un esquema SQL.

Figura 3. Vista resumida del dominio UML.

### 5.3 Análisis de persistencia y concurrencia

La persistencia usa proyectos y colecciones auxiliares para mensajes, membresías, actividad, sesiones, visitas y avisos. La revisión protege escrituras concurrentes. Una colección de trabajos push permite separar la transacción del documento del envío de red; así el fallo del proveedor no exige mantener abierta la transacción.

## Capítulo 6 Diseño

### 6.1 Arquitectura lógica

Fuente: elaboración propia a partir del código y de los requisitos. STOMP no sustituye la consulta autoritativa del documento ni la persistencia.

Figura 4. Componentes principales de la implementación.

Vue consume REST /api y STOMP /ws. El backend valida JWT y permisos antes de delegar en proyecto, asistente y actividad. El proveedor de IA devuelve datos no confiables que pasan por normalización y validación. MongoDB actúa como almacenamiento persistente y replica set para transacciones.

### 6.2 Secuencia de edición asistida

Fuente: elaboración propia a partir del código y de los requisitos. La voz se transcribe antes del planner. Una baseRevision obsoleta se rechaza antes de persistir.

Figura 5. Solicitud y confirmación de un cambio asistido.

### 6.3 Secuencia de avisos

Fuente: elaboración propia a partir del código y de los requisitos. SENT significa aceptación del proveedor, no prueba de visualización en el teléfono.

Figura 6. Suscripción y entrega de una notificación push.

### 6.4 Despliegue previsto

Fuente: elaboración propia a partir del código y de los requisitos. Topología pendiente de elegir y desplegar; no se han creado recursos de nube.

Figura 7. Propuesta de despliegue en nube.

### 6.5 Diseño de interfaz e interoperabilidad

La interfaz organiza proyectos, pizarra, inspector, conversación y herramientas de actividad. La vista móvil es informativa. Las propuestas requieren previsualización y confirmación. XMI representa el subconjunto soportado y valida las importaciones antes de sustituir el documento. Los diagramas de pantalla definitivos deben acompañarse de capturas de esta versión, no de interfaces de la referencia.

## Capítulo 7 Implementación

### 7.1 Frontend y colaboración

El frontend se implementa en Vue 3 con estado Pinia. El adaptador convierte el contrato del backend a elementos Vue Flow y conserva UUID, tipos, métodos y layout. El historial Undo/Redo utiliza instantáneas de sesión y se invalida con cambios externos. Autoorganizar todavía guarda posiciones por peticiones separadas; no se presenta como un BATCH atómico.

### 7.2 Backend y métodos UML

Spring Boot organiza autenticación, proyectos, validación, colaboración, asistencia, generación y persistencia. UmlOperation y UmlParameter añaden métodos de forma compatible con documentos antiguos. SET_CLASS_OPERATIONS modifica únicamente los métodos y conserva nombre y atributos de la clase. Se rechazan firmas ambiguas y cambios no pedidos.

### 7.3 Conversación y voz

GroupAssistant integra ASK, REVIEW, EDIT y SUMMARY_CURRENT; el backend persiste solicitudes y respuestas y publica eventos por proyecto. La voz usa Whisper y el mismo planner tras la transcripción. El acceso a un proveedor real sigue pendiente; no se utilizan respuestas simuladas como evidencia de inferencia.

### 7.4 Persistencia y seguridad

MongoDB conserva el trabajo en replica set local. Las contraseñas usan BCrypt y los endpoints validan JWT. El propietario administra invitaciones; el colaborador aceptado tiene permiso EDITOR. No existe un rol persistente VIEWER ni una administración completa de cambios y eliminación de colaboradores en esta versión.

### 7.5 Entrega push y generación

PushDeliveryService registra trabajos en la transacción del aviso, los reclama con lease y efectúa envíos fuera de esa transacción. Reintenta hasta ocho veces; elimina suscripciones vencidas y utiliza un índice TTL de siete días con BSON Date. La configuración permanece deshabilitada por defecto. Los ZIP con métodos conservan el diseño UML y su documentación, sin inventar implementaciones de negocio.

## Capítulo 8 Pruebas

### 8.1 Estrategia y criterios

Las pruebas de dominio verifican reglas deterministas; las de integración comprueban transacciones y aislamiento; las de interfaz verifican adaptación y estado. La aceptación de sistema necesita dos cuentas, proveedores reales, persistencia remota y un teléfono. No se calcula complejidad ciclomática ni cobertura si no se ha obtenido un grafo o reporte reproducible.

| Grupo de evidencia | Resultado registrado | Alcance real |
| --- | --- | --- |
| Backend del último incremento | 121 pruebas sin fallos | Push, actividad, avisos, chat y colaboración. |
| Cifrado adicional | 2 pruebas aprobadas | Claves efímeras y encabezados VAPID; sin red externa. |
| Frontend | 21 pruebas y build correctos | Contratos, estado y privacidad del worker. |
| Smoke STOMP | Crear, actualizar y borrar método temporal | Transporte local real en un proyecto QA. |
| IA, voz, nube y móvil | Pendientes | No se certifican por los tests controlados. |

Los números corresponden a ejecuciones previas documentadas, no a una nueva ejecución de suites al redactar este informe. No se suman a regresiones históricas como si todos fueran casos distintos.

### 8.2 Pruebas de aceptación pendientes

PA-01 Dos cuentas editan, provocan un conflicto de revisión y convergen después de reconectar.

PA-02 Ambas cuentas ven la misma pregunta y respuesta del proveedor real.

PA-03 Una orden por voz genera propuesta válida, se confirma y se refleja en ambas pizarras.

PA-04 Un integrante que llega tarde consulta un resumen sin hechos o autorías inventados.

PA-05 Reiniciar la aplicación y retomar desde otro dispositivo con MongoDB remoto.

PA-06 El teléfono recibe push por un cambio ajeno, abre el proyecto y deja de recibirlo después de desactivar o salir.

PA-07 Compilar y ejecutar las aplicaciones generadas para recertificar el primer parcial.

### 8.3 Registro de evidencia

Cada evidencia deberá incluir ID de requisito y CU, commit probado, fecha, entorno, pasos, resultado esperado y observado, participantes de prueba y archivo de respaldo. Un fallo queda abierto; no se sustituye por una captura de otro sistema ni por un estado histórico CERRADO.

## Capítulo 9 Costos riesgos y seguridad

### 9.1 Recursos y costos

No se ha seleccionado un plan de nube ni se han creado recursos facturables. El presupuesto debe separar alojamiento, base de datos, consumo de IA y conectividad. Las tarifas se documentarán al elegir proveedor; no se incluye un monto inventado. La cuenta personal de Gemini no equivale necesariamente a una clave API disponible.

### 9.2 Riesgos y mitigación

| Riesgo | Mitigación o tarea |
| --- | --- |
| Proveedor IA o voz no disponible | Confirmar acceso API o runtimes y realizar una prueba completa. |
| Pérdida de actualización concurrente | Validar baseRevision y recuperar el documento autoritativo. |
| Exposición de claves | Variables privadas del backend y revisión antes de publicar. |
| Aviso para cuenta incorrecta | Vinculación de cuenta en el worker y validación de destinatario. |
| Documentación divergente | Mantener matriz y diagramas con evidencia de la versión actual. |
| Nube y móvil sin aceptar | Reservar una sesión de prueba con dos cuentas y teléfono real. |

### 9.3 Protección del trabajo

Las sesiones y permisos se comprueban en el backend. El contexto del proveedor se limita al proyecto autorizado. Los avisos push son genéricos y no contienen tokens ni texto privado del diagrama. La publicación del código en GitHub no equivale al despliegue de la aplicación ni habilita compartir datos o credenciales personales.

## Resultados y conclusiones

La base académica queda alineada con la implementación Vue, Spring Boot y MongoDB y conserva el alcance incremental del segundo parcial. Se especifican siete casos nuevos con flujos y criterios observables. El soporte de métodos, conversación, continuidad y push tiene implementación, pero todavía se debe completar su aceptación real.

No corresponde declarar el proyecto terminado antes de configurar IA y voz, desplegar la persistencia NoSQL en nube, verificar la recepción móvil y recertificar el primer parcial. La documentación debe evolucionar junto con esas evidencias y no adelantarse a ellas.

## Recomendaciones

Confirmar la rúbrica, el nombre del docente, grupo y fecha de entrega.

Aprobar la numeración definitiva de CU-SP y contrastar la consigna del primer parcial.

Integrar el proveedor real elegido antes de producir capturas de una demo de IA.

Actualizar diagramas, pruebas y manual con la arquitectura realmente desplegada.

## Referencias

[1] Object Management Group. Unified Modeling Language 2.5.1. https://www.omg.org/spec/UML/2.5.1/About-UML

[2] Spring. Documentación oficial de Spring Boot. https://docs.spring.io/spring-boot/index.html

[3] MongoDB. Transactions. https://www.mongodb.com/docs/manual/core/transactions/

[4] Vue.js. Introduction. https://vuejs.org/guide/introduction.html

[5] Documento de referencia proporcionado por el estudiante: Documentacion_CASE_Leonardo_V9_FINAL_CON_INDICE_DIAGRAMAS.docx. Se utiliza para estructura y presentación; su arquitectura no se adopta como evidencia.

[6] Repositorio de la versión actual: https://github.com/Leo14fel/Segundo-2

[7] Consigna del segundo parcial: transcripción del docente aportada por el estudiante. Consigna original completa del primer parcial pendiente de contraste.

[8] Evidencia técnica del proyecto: CONTINUAR.md y docs/runtime/integraciones-segundo-parcial.md. Corte de revisión documental: 9 de noviembre de 2026.

## Anexos

### Anexo A Matriz de trazabilidad

| Requisito | Caso relacionado | Estado y evidencia faltante |
| --- | --- | --- |
| RF-SP-01 | Catálogo heredado | Recertificación pendiente |
| RF-SP-02 | CU-28 a CU-31 | Pruebas locales |
| RF-SP-03 | CU-06/07; SP-06 | Aceptación integral pendiente |
| RF-SP-04 | SP-01 | Falta proveedor real |
| RF-SP-05 | SP-04 | Flujo físico pendiente |
| RF-SP-06 | SP-02 | Falta proveedor real |
| RF-SP-07 | SP-03 | Aceptación pendiente |
| RF-SP-08 | SP-01/03 | Contexto implementado |
| RF-SP-09 | SP-05 | Nube por configurar |
| RF-SP-10 | SP-05 | Local; falta nube |
| RF-SP-11 | SP-06 | Falta teléfono real |
| RF-SP-12 | SP-07 | Desactivado; falta recepción real |

### Anexo B Instalación y ejecución local

1. Disponer de Java 21, Node 24 y Docker con MongoDB replica set.

2. Desde la raíz: docker compose -f compose.mongo.yml up -d --wait.

3. En backend: configurar JAVA_HOME y ejecutar gradlew.bat bootRun.

4. En frontend: npm ci si faltan dependencias y npm run dev.

5. Abrir http://127.0.0.1:4200; el backend usa 8082.

6. Crear cuentas de prueba desde el registro; no incluir contraseñas en el informe.

Estas instrucciones describen el entorno local; no son una guía de despliegue en nube. Revisar los puertos antes de iniciar procesos duplicados.

### Anexo C Manual de demostración

1. Iniciar sesión y abrir un proyecto propio o compartido.

2. Crear clases, atributos, un método con parámetros y una relación.

3. Guardar, recargar y comprobar persistencia; validar y exportar XMI.

4. Con una segunda cuenta, mostrar presencia, cambio remoto y rechazo de una revisión antigua.

5. Con IA configurada, ejecutar consulta, revisión, resumen y edición confirmada.

6. Desde un teléfono, observar cambios; probar push solo con HTTPS y claves configuradas.

7. Registrar pendientes sin sustituirlos por resultados simulados.

### Anexo D Inventario de diagramas editables

| Vista | Fuente del repositorio |
| --- | --- |
| Casos de uso | docs/formal/casos-uso-segundo-parcial.puml |
| Dominio | docs/formal/modelo-dominio-segundo-parcial.mmd |
| Componentes | docs/formal/forge-studio-componentes.mmd |
| Edición de métodos IA | docs/formal/ia-metodos-secuencia.mmd |
| Web Push | docs/formal/web-push-secuencia.mmd |

Las figuras de esta base son elaboraciones legibles para revisión. El mapa funcional no reemplaza el diagrama UML completo. Antes de la entrega, completar las vistas de análisis y comunicación que la rúbrica exija, usando la implementación actual.
