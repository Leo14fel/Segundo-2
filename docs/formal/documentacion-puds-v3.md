# Forge Studio Base PUDS V3

## Índice de diagramas

## 1 Perfil

### 1.1 Introducción

Forge Studio es una herramienta CASE web para construir y compartir diagramas de clases. El segundo parcial incorpora a la inteligencia artificial como un participante consultivo común al equipo: responde preguntas, revisa el modelo y resume avances, pero no aplica cambios por iniciativa propia.

Esta base se organiza por los flujos de trabajo del Proceso Unificado de Desarrollo de Software. Relaciona modelo de negocio, requisitos, casos de uso, análisis, diseño, implementación y pruebas. Describe Vue, Spring Boot y MongoDB y distingue la implementación local de la aceptación pendiente en nube, con proveedores reales y en teléfono.

Versión 0.3 de trabajo al 9 de noviembre de 2026. Las áreas D01 en adelante están reservadas para insertar los diagramas que se elaborarán en XML. Los nombres de archivo son una planificación; todavía no existen los XML ni se ha elegido su esquema de editor.

### 1.2 Objetivos

#### 1.2.1 Objetivo general

Desarrollar una herramienta CASE colaborativa con asistencia de IA grupal que permita modelar, conservar y consultar diagramas UML con autoría, validación y control de revisión, manteniendo las funciones obligatorias del primer parcial.

#### 1.2.2 Objetivos específicos

Recertificar los casos heredados con la interfaz Vue y los artefactos generados.

Compartir consultas, revisiones, resúmenes y propuestas de IA por proyecto.

Procesar órdenes de voz y aplicar cambios únicamente tras validación y confirmación.

Conservar sesiones continuas mediante persistencia NoSQL en nube.

Permitir consulta móvil y notificaciones push verificadas en un dispositivo real.

Mantener trazabilidad desde requisito y caso de uso hasta componente y prueba.

### 1.3 Descripción del problema

El trabajo distribuido pierde continuidad cuando el diagrama, las conversaciones y las decisiones quedan en herramientas o sesiones aisladas. Los integrantes que llegan después desconocen qué cambió y por qué; una IA utilizada de manera individual añade respuestas que el resto del equipo no puede revisar.

La situación se agrava con ediciones concurrentes, pérdida de conectividad y consultas desde dispositivos móviles. Se necesita una representación común del modelo, reglas de edición, autoría registrada y recuperación del contexto disponible, sin que una propuesta automática eluda la autoridad del proyecto.

### 1.4 Alcance

El alcance comprende identidad, proyectos, colaboración, clases, atributos, métodos, parámetros, relaciones, XMI, generación heredada, conversación IA, actividad, sesiones y avisos. No se afirma ejecución automática de cuerpos de negocio a partir de firmas UML. La aplicación Flutter generada y el observador móvil del CASE son productos distintos.

El móvil es una experiencia web informativa y no un rol VIEWER implementado en el backend. Undo/Redo permanece en la sesión del navegador. No se afirma que exista nube desplegada, Gemini integrado ni recepción push real mientras no se produzca su evidencia.

### 1.5 Organización del trabajo PUDS

| Fase | Artefactos y comprobación |
| --- | --- |
| Inicio | Perfil, alcance, actores y riesgos prioritarios. |
| Elaboración | Requisitos, casos de uso, paquetes y diseño de arquitectura. |
| Construcción | Incrementos implementados con pruebas y revisión de trazabilidad. |
| Transición | Demostración, aceptación real, despliegue y documentación actualizada. |

Las fases no equivalen a los capítulos ni a una declaración de cierre. Cada iteración puede recorrer los flujos de requisitos, análisis, diseño, implementación y pruebas. La prioridad se expresa como una propuesta de trabajo, sin inventar fechas o ciclos ya aceptados.

## 2 Marco teórico

### 2.1 Herramientas CASE y UML

Una herramienta CASE apoya actividades de ingeniería mediante modelos y transformaciones. UML aporta una notación para clases, atributos, operaciones y relaciones [1]. La aplicación implementa un subconjunto definido; no declara compatibilidad total con todo UML 2.5.1.

La semántica del modelo se mantiene separada de su layout. Un método conserva nombre, visibilidad, retorno y parámetros; la ausencia de retorno representa void. Una relación identifica ambos extremos y sus multiplicidades. Los identificadores permiten conservar referencias aunque cambie un nombre.

### 2.2 Colaboración y control de revisión

La revisión del proyecto evita que una escritura obsoleta reemplace silenciosamente cambios ajenos. El frontend guarda manualmente mediante REST y consulta el documento autoritativo cada 2,5 segundos. STOMP transporta presencia y operaciones del asistente. No se afirma que todo gesto de edición manual sea un comando STOMP.

### 2.3 IA compartida y procesamiento de voz

El proveedor recibe el modelo, integrantes y contexto reciente autorizado. ASK, REVIEW y SUMMARY_CURRENT generan respuestas sin editar el UML; EDIT produce una propuesta. El servidor valida referencias y tipos antes de habilitar su confirmación. El contexto no es ilimitado: incluye hasta 20 mensajes recientes y 50 hechos de actividad.

Whisper convierte voz en texto antes del planner. La petición del docente exige solicitar cambios mediante voz; debe precisarse si admite también texto. Los servicios de IA no deben modificar directamente la base de datos o el canvas.

### 2.4 Persistencia documental y notificaciones

MongoDB permite mantener el documento de proyecto con su modelo embebido. Las transacciones coordinan cambios que involucran actividad, sesiones o notificaciones [3]. Web Push complementa los avisos internos: necesita una suscripción del navegador y un proveedor de entrega, no solamente un WebSocket abierto.

### 2.5 Proceso Unificado de Desarrollo de Software

PUDS articula el desarrollo mediante casos de uso, arquitectura e iteraciones. En este informe la captura de requisitos identifica necesidades; el análisis distribuye responsabilidades; el diseño concreta componentes, datos e interacciones; la implementación materializa esas decisiones; y las pruebas comprueban los escenarios. Cada vista debe corresponder con las demás.

## 3 Modelo de negocio

### 3.1 Contexto y participantes

El negocio considerado es la coordinación de un equipo de desarrollo que modela una solución de software. Participan quien organiza el proyecto, los colaboradores y el integrante que necesita consultar desde un móvil. El resultado de valor es un diseño compartido y trazable, acompañado de decisiones y propuestas accesibles al equipo.

### 3.2 Proceso de trabajo colaborativo

1. Preparar el proyecto y habilitar el acceso a los integrantes.

2. Abrir o recuperar el modelo actual.

3. Modelar y revisar cambios con reglas de concurrencia.

4. Consultar a la IA o solicitar una propuesta cuando haga falta.

5. Confirmar solo las propuestas válidas y compartir el estado resultante.

6. Registrar actividad y conservar el trabajo para retomarlo.

XML previsto: D01-actividad-modelo-negocio.xml. Representar inicio, participantes, decisiones, validación de cambios, consulta IA y continuidad de sesión.

[D01 Espacio reservado — Actividad del proceso de modelado colaborativo; XML previsto: D01-actividad-modelo-negocio.xml]

### 3.3 Entradas salidas y reglas

| Elemento | Descripción |
| --- | --- |
| Entradas | Necesidades del equipo, documento UML actual y solicitudes explícitas. |
| Salidas | Modelo confirmado, conversación común y hechos de actividad. |
| Reglas | Autorización, revisión vigente, validación del dominio y confirmación de propuestas. |
| Restricción | La aceptación de nube y móvil depende de configuración y prueba real. |

## 4 Flujo de trabajo Captura de requisitos

### 4.1 Encontrar actores y casos de uso

| Actor | Responsabilidad |
| --- | --- |
| Visitante | Registrarse e iniciar sesión. |
| Propietario | Crear el proyecto y administrar invitaciones. |
| Colaborador EDITOR | Modelar y consultar el proyecto compartido. |
| Integrante móvil | Observar el trabajo desde la interfaz informativa. |
| Proveedor de IA | Responder consultas y proponer acciones. |
| Transcripción y push | Convertir voz y entregar avisos. |

XML previsto: D02-actores.xml. Distinguir actores humanos y sistemas externos; el modo móvil no representa un permiso VIEWER del backend.

[D02 Espacio reservado — Identificación de actores del sistema; XML previsto: D02-actores.xml]

Se conserva la numeración CU-01 a CU-31 del catálogo existente. CU-SP-01 a CU-SP-07 identifica la ampliación del segundo parcial y no sustituye los identificadores anteriores.

| Casos heredados | Capacidades que se deben conservar |
| --- | --- |
| CU-01 a CU-04 | Proyectos, guardado, modelado y validación UML. |
| CU-05 a CU-07 | Deshacer/rehacer de sesión, colaboración y presencia. |
| CU-08 a CU-11 | Asistencia texto/voz/imagen e interoperabilidad XMI. |
| CU-12 a CU-19 | Modelo relacional, generación e interacción con aplicaciones generadas. |
| CU-20 a CU-27 | Estados históricos absorbidos/infraestructura/demo: contrastar con la consigna. |
| CU-28 a CU-31 | Registro, inicio de sesión, acceso e invitaciones. |

### 4.2 Priorización de casos de uso

Todos los CU-SP responden a capacidades solicitadas por el docente. Los incrementos propuestos ordenan la ejecución, no reducen la obligatoriedad ni declaran un ciclo cerrado. I1: recertificación y acceso; I2: asistencia real; I3: nube y aceptación móvil.

| Caso | Nombre | Prioridad | Actor e incremento |
| --- | --- | --- | --- |
| CU-SP-01 | Consultar a la IA grupal | Alta | Integrante autorizado · I2 |
| CU-SP-02 | Solicitar revisión del diagrama | Alta | Integrante autorizado · I2 |
| CU-SP-03 | Solicitar un resumen de lo avanzado | Alta | Integrante autorizado · I2 |
| CU-SP-04 | Solicitar y confirmar edición por voz | Alta | Integrante autorizado · I2 |
| CU-SP-05 | Retomar una sesión registrada | Alta | Integrante autorizado · I3 |
| CU-SP-06 | Observar el proyecto desde un móvil | Alta | Integrante autorizado · I3 |
| CU-SP-07 | Activar y recibir avisos push | Alta | Integrante autorizado · I3 |

### 4.3 Detalles de los casos de uso

Las fichas siguientes siguen los campos de la referencia: propósito, resumen, actores, actor iniciador, flujo de proceso, precondición, postcondición y excepción. Se añaden requisito relacionado, criterio y estado de aceptación para mantener trazabilidad.

#### CU-SP-01 Consultar a la IA grupal

| Campo | Especificación |
| --- | --- |
| Caso de uso | CU-SP-01 · Consultar a la IA grupal |
| Propósito | Compartir preguntas y respuestas de IA entre los integrantes del proyecto. |
| Resumen | Escribe una pregunta en la conversación común. Mensaje y respuesta quedan en el historial del proyecto; el UML no cambia. |
| Actores | Integrante con permiso de edición y proveedor IA. |
| Actor iniciador | Integrante con permiso de edición |
| Requisito relacionado | RF-SP-04 y RF-SP-08 |
| Precondición | Proyecto abierto y proveedor disponible. |
| Flujo de proceso | 1. Escribe una pregunta en la conversación común. / 2. El backend registra la solicitud con autor y requestId. / 3. Construye el contexto autorizado y consulta al proveedor. / 4. Guarda la respuesta y la publica para los integrantes. / 5. Los clientes reconcilian el historial compartido. |
| Postcondición | Mensaje y respuesta quedan en el historial del proyecto; el UML no cambia. |
| Excepción | Si el proveedor falla se informa y se permite reintentar. El mismo requestId evita duplicar una respuesta ya completada. |
| Criterio de aceptación | Dos cuentas ven el mismo intercambio con su autoría. |
| Estado de aceptación | Implementación y pruebas controladas; falta proveedor real. |

#### CU-SP-02 Solicitar revisión del diagrama

| Campo | Especificación |
| --- | --- |
| Caso de uso | CU-SP-02 · Solicitar revisión del diagrama |
| Propósito | Obtener observaciones sobre el diagrama sin modificarlo automáticamente. |
| Resumen | Selecciona REVIEW y solicita la revisión. Existe una revisión compartida; no se aplica una corrección automática. |
| Actores | Integrante con acceso de edición y proveedor IA. |
| Actor iniciador | Integrante con acceso de edición |
| Requisito relacionado | RF-SP-06 |
| Precondición | Documento actual disponible y modelo IA operativo. |
| Flujo de proceso | 1. Selecciona REVIEW y solicita la revisión. / 2. El backend toma una instantánea y registra su revisión. / 3. La IA analiza el contexto y devuelve observaciones. / 4. Se filtran referencias inexistentes y hallazgos inválidos. / 5. El sistema comparte la revisión y su vínculo con la instantánea. |
| Postcondición | Existe una revisión compartida; no se aplica una corrección automática. |
| Excepción | Una observación con referencia inventada se descarta. Una respuesta no estructurada puede presentarse como texto sin atribuir hallazgos inexistentes. |
| Criterio de aceptación | La revisión no incrementa la revisión del documento ni cambia sus elementos. |
| Estado de aceptación | Falta aceptación de calidad con un modelo real. |

#### CU-SP-03 Solicitar un resumen de lo avanzado

| Campo | Especificación |
| --- | --- |
| Caso de uso | CU-SP-03 · Solicitar un resumen de lo avanzado |
| Propósito | Recuperar el contexto disponible para quien se incorpora o retoma la sesión. |
| Resumen | Abre la conversación común y selecciona SUMMARY_CURRENT. Queda un resumen compartido sin modificaciones al UML. |
| Actores | Integrante que retoma el trabajo y proveedor IA. |
| Actor iniciador | Integrante que retoma el trabajo |
| Requisito relacionado | RF-SP-07 y RF-SP-08 |
| Precondición | Proyecto accesible y proveedor IA configurado. |
| Flujo de proceso | 1. Abre la conversación común y selecciona SUMMARY_CURRENT. / 2. El backend reúne UML, miembros, mensajes y actividad reciente. / 3. Comunica al proveedor la cobertura y los límites del contexto. / 4. Guarda y publica el resumen para el equipo. / 5. El integrante contrasta el resumen con la actividad del proyecto. |
| Postcondición | Queda un resumen compartido sin modificaciones al UML. |
| Excepción | Si no hay hechos anteriores se informa. Si el historial es parcial, no se presenta como un relato exhaustivo. |
| Criterio de aceptación | Un integrante que llega tarde entiende los hechos disponibles sin autorías inventadas. |
| Estado de aceptación | Falta escenario completo con dos cuentas e IA real. |

#### CU-SP-04 Solicitar y confirmar edición por voz

| Campo | Especificación |
| --- | --- |
| Caso de uso | CU-SP-04 · Solicitar y confirmar edición por voz |
| Propósito | Convertir una orden de voz en un cambio validado y confirmado del modelo. |
| Resumen | Solicita grabar una orden y concede permiso si corresponde. El cambio aceptado tiene revisión y autoría; los demás clientes recuperan el estado. |
| Actores | Propietario o colaborador EDITOR y servicios de transcripción e IA. |
| Actor iniciador | Propietario o colaborador EDITOR |
| Requisito relacionado | RF-SP-05 |
| Precondición | Micrófono autorizado, transcripción e IA disponibles. |
| Flujo de proceso | 1. Solicita grabar una orden y concede permiso si corresponde. / 2. El cliente captura audio y envía WAV para transcripción. / 3. El planner interpreta el texto usando el catálogo actual. / 4. Se validan referencias, intención, tipos y propuesta. / 5. El integrante revisa y confirma la propuesta. / 6. La autoridad comprueba permisos y baseRevision, persiste y propaga el cambio. |
| Postcondición | El cambio aceptado tiene revisión y autoría; los demás clientes recuperan el estado. |
| Excepción | Audio inválido, servicio caído, instrucción ambigua o revisión obsoleta generan rechazo. Cancelar la propuesta conserva el documento. |
| Criterio de aceptación | Demostrar voz real, preview, confirmación y convergencia sin escrituras autónomas. |
| Estado de aceptación | Pendiente voz/modelo reales y verificación de la traza grupal de la propuesta de voz. |

#### CU-SP-05 Retomar una sesión registrada

| Campo | Especificación |
| --- | --- |
| Caso de uso | CU-SP-05 · Retomar una sesión registrada |
| Propósito | Continuar el trabajo sin perder el documento, conversación y actividad disponibles. |
| Resumen | Inicia sesión y abre el proyecto. Se recupera el trabajo autorizado y se conserva la continuidad registrada. |
| Actores | Integrante autorizado. |
| Actor iniciador | Integrante autorizado |
| Requisito relacionado | RF-SP-09 y RF-SP-10 |
| Precondición | Existe un proyecto persistido al que tiene acceso. |
| Flujo de proceso | 1. Inicia sesión y abre el proyecto. / 2. Recupera el documento y su revisión actual. / 3. Consulta sesiones, actividad y novedades desde la última visita. / 4. Puede consultar el resumen compartido de IA. / 5. Registra la visita y continúa trabajando. |
| Postcondición | Se recupera el trabajo autorizado y se conserva la continuidad registrada. |
| Excepción | Una cuenta ajena no accede. Un fallo de red no se presenta como pérdida confirmada de información. |
| Criterio de aceptación | Pausar y retomar desde otro dispositivo con MongoDB remoto. |
| Estado de aceptación | Implementado localmente; nube y recuperación entre dispositivos pendientes. |

#### CU-SP-06 Observar el proyecto desde un móvil

| Campo | Especificación |
| --- | --- |
| Caso de uso | CU-SP-06 · Observar el proyecto desde un móvil |
| Propósito | Permitir seguimiento del proyecto desde un móvil sin edición UML en esa vista. |
| Resumen | Abre la interfaz informativa móvil. El integrante puede seguir la sesión sin editar desde el modo móvil. |
| Actores | Integrante en movimiento. |
| Actor iniciador | Integrante en movimiento |
| Requisito relacionado | RF-SP-03 y RF-SP-11 |
| Precondición | Sesión iniciada y acceso al proyecto desde un teléfono. |
| Flujo de proceso | 1. Abre la interfaz informativa móvil. / 2. Consulta el diagrama y los participantes. / 3. Recibe la evolución mediante sincronización y reconciliación. / 4. Consulta conversación, actividad y avisos disponibles. / 5. Al reconectar recupera la versión autoritativa. |
| Postcondición | El integrante puede seguir la sesión sin editar desde el modo móvil. |
| Excepción | Sin conexión se comunica el estado y se intenta reconciliar. La interfaz no ofrece edición UML en esta experiencia. |
| Criterio de aceptación | Probar un teléfono real, cambios de otra cuenta y reconexión. |
| Estado de aceptación | Modo responsive implementado; aceptación física pendiente. |

#### CU-SP-07 Activar y recibir avisos push

| Campo | Especificación |
| --- | --- |
| Caso de uso | CU-SP-07 · Activar y recibir avisos push |
| Propósito | Avisar de cambios ajenos y facilitar la apertura del proyecto autorizado. |
| Resumen | Activa avisos desde el panel y concede permiso explícito. Se registra el resultado de envío y se puede consultar el proyecto autorizado. |
| Actores | Integrante con dispositivo compatible y proveedor push. |
| Actor iniciador | Integrante con dispositivo compatible |
| Requisito relacionado | RF-SP-12 |
| Precondición | HTTPS, claves VAPID, sesión y soporte push configurados. |
| Flujo de proceso | 1. Activa avisos desde el panel y concede permiso explícito. / 2. El cliente registra una suscripción vinculada a su cuenta. / 3. Un cambio de otro integrante crea aviso y trabajo en una transacción. / 4. El trabajador envía el payload cifrado al proveedor. / 5. El service worker verifica destinatario y muestra un aviso genérico. / 6. Al pulsarlo abre el proyecto y verifica nuevamente el acceso. |
| Postcondición | Se registra el resultado de envío y se puede consultar el proyecto autorizado. |
| Excepción | Permiso denegado conserva los avisos internos. HTTP 404/410 elimina la suscripción vencida; los otros fallos tienen reintentos acotados. |
| Criterio de aceptación | Recepción visible en un teléfono, apertura correcta y desvinculación al salir. |
| Estado de aceptación | Implementado y probado con transporte controlado; recepción real pendiente. |

### 4.4 Estructurar el modelo de casos de uso

El modelo debe delimitar Forge Studio, distinguir los actores y relacionar los casos heredados con la ampliación CU-SP. Usar include solo para comportamiento obligatorio reutilizado y extend para una ampliación condicionada; no utilizarlos como simples flechas de orden temporal.

XML previsto: D03-casos-uso-general.xml. Representar el límite del sistema y los casos agrupados por identidad, modelado, colaboración, asistencia y observación móvil.

[D03 Espacio reservado — Modelo general de casos de uso; XML previsto: D03-casos-uso-general.xml]

### 4.5 Requisitos y restricciones de aceptación

| ID | Requisito | Comprobación observable |
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

RNF-01 Seguridad: autenticar llamadas, validar permisos y mantener claves fuera del repositorio público.

RNF-02 Consistencia: validar el documento y la revisión antes de confirmar una modificación.

RNF-03 Recuperación: conservar datos tras recarga y reconciliar el estado al reconectar.

RNF-04 Privacidad: los avisos push muestran contenido genérico, no diagramas, mensajes o tokens.

RNF-05 Despliegue: utilizar HTTPS/WSS y MongoDB remoto con transacciones antes de aceptar nube.

No se fijan cifras de latencia, disponibilidad o usuarios simultáneos sin acuerdo ni medición. El API usa JSON; la voz se envía como WAV; XMI se importa con preview y validación. Las credenciales del proveedor permanecen en el backend.

RN-01 La conversación IA es por proyecto y compartida, sin chats privados con el modelo.

RN-02 Consultar, revisar o resumir no cambia el diagrama.

RN-03 Una edición requiere solicitud, confirmación, permiso y baseRevision vigente.

RN-04 La consigna exige voz para pedir cambios de IA; aclarar con el docente si además admite texto.

RN-05 El observador móvil es un modo de interfaz y no un rol VIEWER persistido.

RN-06 Undo/Redo es de sesión; no se documenta como historial persistente entre recargas.

## 5 Flujo de trabajo Análisis

### 5.1 Análisis de la arquitectura

#### 5.1.1 Identificar paquetes

| Paquete | Responsabilidad |
| --- | --- |
| Identidad y acceso | JWT, credenciales y permisos por proyecto. |
| Proyecto y validación | Documento UML y reglas del dominio. |
| Colaboración | Presencia y operaciones con revisión. |
| Asistente | Contexto, conversación, routing y propuestas. |
| Actividad y sesiones | Registro, visitas, continuidad y avisos. |
| Interoperabilidad y generación | XMI y producción de artefactos. |
| Push | Suscripciones, cola y entrega. |

XML previsto: D04-paquetes-analisis.xml. Ubicar los siete paquetes y sus responsabilidades sin confundir paquetes lógicos con servidores físicos.

[D04 Espacio reservado — Identificación de paquetes de análisis; XML previsto: D04-paquetes-analisis.xml]

#### 5.1.2 Relaciones entre paquetes

Los servicios de proyecto usan la validación y el acceso; el asistente consulta contexto y prepara propuestas; la aplicación de operaciones pasa por colaboración y proyecto. La actividad genera hechos y avisos; push consume trabajos persistidos, sin ejecutar el envío dentro de la transacción UML.

XML previsto: D05-relaciones-paquetes.xml. Mostrar dependencias y evitar que la IA escriba directamente en persistencia o el canvas.

[D05 Espacio reservado — Relaciones entre paquetes de análisis; XML previsto: D05-relaciones-paquetes.xml]

### 5.2 Relacionar paquetes con casos de uso

| Caso | Paquetes principales |
| --- | --- |
| CU-SP-01/02/03 | Asistente, identidad, proyecto y actividad. |
| CU-SP-04 | Asistente, colaboración, proyecto y validación. |
| CU-SP-05 | Proyecto, actividad, sesiones e identidad. |
| CU-SP-06 | Proyecto, colaboración y actividad. |
| CU-SP-07 | Actividad, notificaciones y push. |

XML previsto: D06-encapsulamiento-casos.xml. Relacionar cada CU-SP con sus responsabilidades y conservar la referencia a los casos heredados.

[D06 Espacio reservado — Encapsulamiento de casos de uso por paquetes; XML previsto: D06-encapsulamiento-casos.xml]

### 5.3 Analizar casos de uso

Las vistas de comunicación describen participantes y mensajes numerados. Deben corresponder con el flujo de la ficha; no sustituyen las secuencias de diseño del capítulo 6.

#### 5.3.1 Comunicación de CU-SP-01

XML previsto: D07-comunicacion-SP01.xml. Mostrar actor, interfaz, control y entidades participantes, con mensajes numerados y el manejo de la excepción principal.

[D07 Espacio reservado — Comunicación de CU-SP-01 consultar a la ia grupal; XML previsto: D07-comunicacion-SP01.xml]

#### 5.3.2 Comunicación de CU-SP-02

XML previsto: D08-comunicacion-SP02.xml. Mostrar actor, interfaz, control y entidades participantes, con mensajes numerados y el manejo de la excepción principal.

[D08 Espacio reservado — Comunicación de CU-SP-02 solicitar revisión del diagrama; XML previsto: D08-comunicacion-SP02.xml]

#### 5.3.3 Comunicación de CU-SP-03

XML previsto: D09-comunicacion-SP03.xml. Mostrar actor, interfaz, control y entidades participantes, con mensajes numerados y el manejo de la excepción principal.

[D09 Espacio reservado — Comunicación de CU-SP-03 solicitar un resumen de lo avanzado; XML previsto: D09-comunicacion-SP03.xml]

#### 5.3.4 Comunicación de CU-SP-04

XML previsto: D10-comunicacion-SP04.xml. Mostrar actor, interfaz, control y entidades participantes, con mensajes numerados y el manejo de la excepción principal.

[D10 Espacio reservado — Comunicación de CU-SP-04 solicitar y confirmar edición por voz; XML previsto: D10-comunicacion-SP04.xml]

#### 5.3.5 Comunicación de CU-SP-05

XML previsto: D11-comunicacion-SP05.xml. Mostrar actor, interfaz, control y entidades participantes, con mensajes numerados y el manejo de la excepción principal.

[D11 Espacio reservado — Comunicación de CU-SP-05 retomar una sesión registrada; XML previsto: D11-comunicacion-SP05.xml]

#### 5.3.6 Comunicación de CU-SP-06

XML previsto: D12-comunicacion-SP06.xml. Mostrar actor, interfaz, control y entidades participantes, con mensajes numerados y el manejo de la excepción principal.

[D12 Espacio reservado — Comunicación de CU-SP-06 observar el proyecto desde un móvil; XML previsto: D12-comunicacion-SP06.xml]

#### 5.3.7 Comunicación de CU-SP-07

XML previsto: D13-comunicacion-SP07.xml. Mostrar actor, interfaz, control y entidades participantes, con mensajes numerados y el manejo de la excepción principal.

[D13 Espacio reservado — Comunicación de CU-SP-07 activar y recibir avisos push; XML previsto: D13-comunicacion-SP07.xml]

### 5.4 Modelo de dominio

Project contiene un ProjectDocument con UmlModel y DiagramLayout. El modelo agrupa clases y relaciones; las clases agrupan atributos y operaciones; cada operación conserva parámetros. Los mensajes IA se asocian por projectId y tienen autor, secuencia, tipo y revisión relacionada. Esta vista no implica una colección MongoDB por clase UML.

XML previsto: D14-modelo-dominio.xml. Incluir proyecto, documento, clases, atributos, métodos, parámetros, relaciones, mensajes y vínculos de autoría. Es una vista conceptual, no una colección por clase UML.

[D14 Espacio reservado — Modelo de dominio de Forge Studio; XML previsto: D14-modelo-dominio.xml]

## 6 Flujo de trabajo Diseño

### 6.1 Diseño de arquitectura física y lógica

#### 6.1.1 Arquitectura lógica

La presentación Vue consume los servicios REST y STOMP de Spring Boot. El backend organiza acceso, proyecto, colaboración, asistente, actividad, generación y push. MongoDB conserva el estado; los proveedores de IA, voz y entrega son servicios externos al dominio.

XML previsto: D15-arquitectura-logica.xml. Detallar capas y componentes, contratos REST/STOMP y validación autoritativa; separar IA y transcripción.

[D15 Espacio reservado — Arquitectura lógica del sistema; XML previsto: D15-arquitectura-logica.xml]

#### 6.1.2 Arquitectura física

En desarrollo existen procesos separados: Vite en 4200, Spring Boot en 8082 y MongoDB en 27017. Los runtimes locales previstos usan 8092, 8093 y 8094. La topología de nube aún debe elegirse y comprobarse con HTTPS/WSS y MongoDB remoto.

XML previsto: D16-arquitectura-fisica.xml. Distinguir nodos y procesos locales de la propuesta de nube; rotular como propuesto todo recurso todavía no desplegado.

[D16 Espacio reservado — Arquitectura física y despliegue previsto; XML previsto: D16-arquitectura-fisica.xml]

### 6.2 Diseño de datos lógico y físico

#### 6.2.1 Diseño lógico

El proyecto contiene el documento UML actual. La conversación, actividad, sesiones, visitas, membresías y avisos se relacionan por identificadores. Los métodos y parámetros están embebidos en las clases del documento. No se incorpora un diseño relacional SQL para describir la persistencia del CASE.

XML previsto: D17-datos-logico.xml. Representar agregados, identificadores, referencias y composición del documento, con distinción entre modelo UML y registros operativos.

[D17 Espacio reservado — Modelo lógico documental; XML previsto: D17-datos-logico.xml]

#### 6.2.2 Diseño físico MongoDB

MongoDB usa un replica set para transacciones. El diseño físico debe identificar las colecciones, claves, índices únicos y relaciones por IDs. El TTL de los trabajos push usa BSON Date; otros instantes conservan los conversores definidos por el proyecto.

XML previsto: D18-datos-fisico-mongodb.xml. Mostrar projects, membresías, mensajes, actividad, sesiones, visitas, avisos, suscripciones y cola push, con índices relevantes.

[D18 Espacio reservado — Diseño físico de persistencia MongoDB; XML previsto: D18-datos-fisico-mongodb.xml]

### 6.3 Diseño de casos de uso

Cada secuencia representa el orden temporal, las validaciones y las alternativas de su caso. Consulta, revisión y resumen no guardan cambios UML; una propuesta de edición requiere confirmación y revisión vigente. Los resultados simulados no se presentan como aceptación real.

#### 6.3.1 Secuencia de CU-SP-01

XML previsto: D19-secuencia-SP01.xml. Incluir actor, frontend, backend y almacenamiento o proveedor correspondiente; representar flujo principal y fragmentos de excepción aplicables.

[D19 Espacio reservado — Secuencia de CU-SP-01 consultar a la ia grupal; XML previsto: D19-secuencia-SP01.xml]

#### 6.3.2 Secuencia de CU-SP-02

XML previsto: D20-secuencia-SP02.xml. Incluir actor, frontend, backend y almacenamiento o proveedor correspondiente; representar flujo principal y fragmentos de excepción aplicables.

[D20 Espacio reservado — Secuencia de CU-SP-02 solicitar revisión del diagrama; XML previsto: D20-secuencia-SP02.xml]

#### 6.3.3 Secuencia de CU-SP-03

XML previsto: D21-secuencia-SP03.xml. Incluir actor, frontend, backend y almacenamiento o proveedor correspondiente; representar flujo principal y fragmentos de excepción aplicables.

[D21 Espacio reservado — Secuencia de CU-SP-03 solicitar un resumen de lo avanzado; XML previsto: D21-secuencia-SP03.xml]

#### 6.3.4 Secuencia de CU-SP-04

XML previsto: D22-secuencia-SP04.xml. Incluir actor, frontend, backend y almacenamiento o proveedor correspondiente; representar flujo principal y fragmentos de excepción aplicables.

[D22 Espacio reservado — Secuencia de CU-SP-04 solicitar y confirmar edición por voz; XML previsto: D22-secuencia-SP04.xml]

#### 6.3.5 Secuencia de CU-SP-05

XML previsto: D23-secuencia-SP05.xml. Incluir actor, frontend, backend y almacenamiento o proveedor correspondiente; representar flujo principal y fragmentos de excepción aplicables.

[D23 Espacio reservado — Secuencia de CU-SP-05 retomar una sesión registrada; XML previsto: D23-secuencia-SP05.xml]

#### 6.3.6 Secuencia de CU-SP-06

XML previsto: D24-secuencia-SP06.xml. Incluir actor, frontend, backend y almacenamiento o proveedor correspondiente; representar flujo principal y fragmentos de excepción aplicables.

[D24 Espacio reservado — Secuencia de CU-SP-06 observar el proyecto desde un móvil; XML previsto: D24-secuencia-SP06.xml]

#### 6.3.7 Secuencia de CU-SP-07

XML previsto: D25-secuencia-SP07.xml. Incluir actor, frontend, backend y almacenamiento o proveedor correspondiente; representar flujo principal y fragmentos de excepción aplicables.

[D25 Espacio reservado — Secuencia de CU-SP-07 activar y recibir avisos push; XML previsto: D25-secuencia-SP07.xml]

### 6.4 Diseño de interfaces

El escritorio presenta proyectos, pizarra, inspector, conversación común y herramientas. El móvil ofrece una vista informativa. Las propuestas muestran preview y confirmación. Los wireframes o capturas definitivos se añadirán después de verificar esta versión, sin reutilizar pantallas de otro proyecto como evidencia.

## 7 Flujo de trabajo Implementación

### 7.1 Herramientas de desarrollo de la aplicación web

| Capa | Herramienta y uso |
| --- | --- |
| Frontend | Vue 3, TypeScript, Vuetify, Pinia y Vue Flow. |
| Backend | Java 21, Spring Boot 4.0.8 y Gradle Wrapper. |
| Persistencia | MongoDB replica set y configuración mediante entorno. |
| Seguridad | JWT, BCrypt y permisos OWNER/EDITOR. |
| IA y voz | Adaptadores llama.cpp y Bedrock; Whisper para transcripción. |
| Notificaciones | Service worker, PushManager, cifrado VAPID y cola. |

### 7.2 Implementación de la arquitectura del sistema

El frontend se implementa en Vue 3 con estado Pinia. El adaptador convierte el contrato del backend a elementos Vue Flow y conserva UUID, tipos, métodos y layout. El historial Undo/Redo utiliza instantáneas de sesión y se invalida con cambios externos. Autoorganizar todavía guarda posiciones por peticiones separadas; no se presenta como un BATCH atómico.

MongoDB conserva el trabajo en replica set local. Las contraseñas usan BCrypt y los endpoints validan JWT. El propietario administra invitaciones; el colaborador aceptado tiene permiso EDITOR. No existe un rol persistente VIEWER ni una administración completa de cambios y eliminación de colaboradores en esta versión.

### 7.3 Implementación de la arquitectura de los subsistemas

#### 7.3.1 Modelado y validación

Spring Boot organiza autenticación, proyectos, validación, colaboración, asistencia, generación y persistencia. UmlOperation y UmlParameter añaden métodos de forma compatible con documentos antiguos. SET_CLASS_OPERATIONS modifica únicamente los métodos y conserva nombre y atributos de la clase. Se rechazan firmas ambiguas y cambios no pedidos.

#### 7.3.2 Asistente y conversación

GroupAssistant integra ASK, REVIEW, EDIT y SUMMARY_CURRENT; el backend persiste solicitudes y respuestas y publica eventos por proyecto. La voz usa Whisper y el mismo planner tras la transcripción. El acceso a un proveedor real sigue pendiente; no se utilizan respuestas simuladas como evidencia de inferencia.

El usuario dispone de Gemini, pero falta confirmar acceso a la API. Esta versión no contiene un adaptador Gemini ni una prueba de inferencia real con ese proveedor.

#### 7.3.3 Push e interoperabilidad

PushDeliveryService registra trabajos en la transacción del aviso, los reclama con lease y efectúa envíos fuera de esa transacción. Reintenta hasta ocho veces; elimina suscripciones vencidas y utiliza un índice TTL de siete días con BSON Date. La configuración permanece deshabilitada por defecto. Los ZIP con métodos conservan el diseño UML y su documentación, sin inventar implementaciones de negocio.

## 8 Flujo de trabajo Pruebas

### 8.1 Plan y niveles de prueba

Las pruebas de dominio verifican reglas deterministas; las de integración comprueban transacciones y aislamiento; las de interfaz verifican adaptación y estado. La aceptación de sistema necesita dos cuentas, proveedores reales, persistencia remota y un teléfono. No se calcula complejidad ciclomática ni cobertura si no se ha obtenido un grafo o reporte reproducible.

Los números corresponden a ejecuciones previas documentadas, no a una nueva ejecución de suites al redactar este informe. No se suman a regresiones históricas como si todos fueran casos distintos.

| Evidencia registrada | Resultado y límite |
| --- | --- |
| Backend del incremento previo | 121 pruebas sin fallos; no es una nueva ejecución al redactar. |
| Cifrado VAPID adicional | 2 pruebas aprobadas con claves efímeras, sin tráfico externo. |
| Frontend | 21 pruebas y build correctos. |
| Smoke STOMP | Crear, actualizar y borrar un método temporal en un proyecto QA. |
| IA, voz, nube y móvil | Aceptación real pendiente; no demostrada por transportes controlados. |

### 8.2 Pruebas de aceptación

PA-01 Dos cuentas editan, provocan un conflicto de revisión y convergen después de reconectar.

PA-02 Ambas cuentas ven la misma pregunta y respuesta del proveedor real.

PA-03 Una orden por voz genera propuesta válida, se confirma y se refleja en ambas pizarras.

PA-04 Un integrante que llega tarde consulta un resumen sin hechos o autorías inventados.

PA-05 Reiniciar la aplicación y retomar desde otro dispositivo con MongoDB remoto.

PA-06 El teléfono recibe push por un cambio ajeno, abre el proyecto y deja de recibirlo después de desactivar o salir.

PA-07 Compilar y ejecutar las aplicaciones generadas para recertificar el primer parcial.

### 8.3 Trazabilidad y registro de resultados

Cada evidencia deberá incluir ID de requisito y CU, commit probado, fecha, entorno, pasos, resultado esperado y observado, participantes de prueba y archivo de respaldo. Un fallo queda abierto; no se sustituye por una captura de otro sistema ni por un estado histórico CERRADO.

| Requisito | Caso relacionado | Estado actual |
| --- | --- | --- |
| RF-SP-01 | Catálogo heredado | Recertificación pendiente |
| RF-SP-02 | CU-28 a CU-31 | Pruebas locales |
| RF-SP-03 | CU-06/07 y SP-06 | Aceptación integral pendiente |
| RF-SP-04 | SP-01 | Falta proveedor real |
| RF-SP-05 | SP-04 | Flujo físico pendiente |
| RF-SP-06 | SP-02 | Falta proveedor real |
| RF-SP-07 | SP-03 | Aceptación pendiente |
| RF-SP-08 | SP-01/03 | Contexto implementado |
| RF-SP-09 | SP-05 | Nube por configurar |
| RF-SP-10 | SP-05 | Local; falta nube |
| RF-SP-11 | SP-06 | Falta teléfono real |
| RF-SP-12 | SP-07 | Desactivado; falta recepción real |

## 9 Conclusiones

La base académica queda alineada con la implementación Vue, Spring Boot y MongoDB y conserva el alcance incremental del segundo parcial. Se especifican siete casos nuevos con flujos y criterios observables. El soporte de métodos, conversación, continuidad y push tiene implementación, pero todavía se debe completar su aceptación real.

No corresponde declarar el proyecto terminado antes de configurar IA y voz, desplegar la persistencia NoSQL en nube, verificar la recepción móvil y recertificar el primer parcial. La documentación debe evolucionar junto con esas evidencias y no adelantarse a ellas.

## 10 Recomendaciones

Confirmar la rúbrica, el nombre del docente, grupo y fecha de entrega.

Aprobar la numeración definitiva de CU-SP y contrastar la consigna del primer parcial.

Integrar el proveedor real elegido antes de producir capturas de una demo de IA.

Actualizar diagramas, pruebas y manual con la arquitectura realmente desplegada.

Completar primero los XML vinculados a D01–D25, revisar su coherencia con las fichas y luego insertarlos en las reservas. La aceptación final requiere evidencias actuales, no solo una documentación formalmente organizada.

## 11 Bibliografía

[1] Object Management Group. Unified Modeling Language 2.5.1. https://www.omg.org/spec/UML/2.5.1/About-UML

[2] Spring. Documentación oficial de Spring Boot. https://docs.spring.io/spring-boot/index.html

[3] MongoDB. Transactions. https://www.mongodb.com/docs/manual/core/transactions/

[4] Vue.js. Introduction. https://vuejs.org/guide/introduction.html

[5] Documento de referencia proporcionado por el estudiante: Documentacion_CASE_Leonardo_V9_FINAL_CON_INDICE_DIAGRAMAS.docx. Se utiliza para estructura y presentación; su arquitectura no se adopta como evidencia.

[6] Repositorio de la versión actual: https://github.com/Leo14fel/Segundo-2

[7] Consigna del segundo parcial: transcripción del docente aportada por el estudiante. Consigna original completa del primer parcial pendiente de contraste.

[8] Evidencia técnica del proyecto: CONTINUAR.md y docs/runtime/integraciones-segundo-parcial.md. Corte de revisión documental: 9 de noviembre de 2026.

[9] Referencia de estructura PUDS aportada por el estudiante: documentacion parcial 2.pdf, sistema académico de otra asignatura. Se aprovecha su orden de flujos; no se trasladan actores, datos o resultados ajenos a Forge Studio.

## 12 Anexos

### Anexo A Inventario para diagramas XML

Los archivos siguientes están previstos y aún no generados. El esquema XML del editor se confirmará al producirlos. Una vez exportado cada diagrama como imagen legible, se reemplazará el espacio de su código Dxx y se actualizarán los índices en Word.

| Código | Tipo | Archivo XML previsto |
| --- | --- | --- |
| D01 | Actividad | D01-actividad-modelo-negocio.xml |
| D02 | Actores | D02-actores.xml |
| D03 | Casos de uso | D03-casos-uso-general.xml |
| D04 | Paquetes | D04-paquetes-analisis.xml |
| D05 | Paquetes | D05-relaciones-paquetes.xml |
| D06 | Paquetes y casos | D06-encapsulamiento-casos.xml |
| D07 | Comunicación | D07-comunicacion-SP01.xml |
| D08 | Comunicación | D08-comunicacion-SP02.xml |
| D09 | Comunicación | D09-comunicacion-SP03.xml |
| D10 | Comunicación | D10-comunicacion-SP04.xml |
| D11 | Comunicación | D11-comunicacion-SP05.xml |
| D12 | Comunicación | D12-comunicacion-SP06.xml |
| D13 | Comunicación | D13-comunicacion-SP07.xml |
| D14 | Dominio | D14-modelo-dominio.xml |
| D15 | Arquitectura lógica | D15-arquitectura-logica.xml |
| D16 | Arquitectura física | D16-arquitectura-fisica.xml |
| D17 | Datos lógico | D17-datos-logico.xml |
| D18 | Datos físico | D18-datos-fisico-mongodb.xml |
| D19 | Secuencia | D19-secuencia-SP01.xml |
| D20 | Secuencia | D20-secuencia-SP02.xml |
| D21 | Secuencia | D21-secuencia-SP03.xml |
| D22 | Secuencia | D22-secuencia-SP04.xml |
| D23 | Secuencia | D23-secuencia-SP05.xml |
| D24 | Secuencia | D24-secuencia-SP06.xml |
| D25 | Secuencia | D25-secuencia-SP07.xml |

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

### Anexo D Evidencias que faltan incorporar

Adjuntar capturas y registros de las pruebas PA-01 a PA-07 con commit, fecha, entorno y resultado observado. Añadir la URL de despliegue solo cuando exista y haya sido comprobada. El nombre del docente, grupo y fecha de entrega se completarán con datos confirmados de esta materia.
