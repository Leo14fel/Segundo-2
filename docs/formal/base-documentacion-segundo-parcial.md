# Bases de documentación de Forge Studio

Segundo parcial de Ingeniería de Software

Versión 0.1 • Borrador de trabajo • 8 de noviembre de 2026

Estudiante: Felipez Sejas Leonardo Ismael. Docente, universidad, grupo y fecha de entrega: por completar con los datos oficiales.

Este documento establece la base para describir el sistema, relacionar los requisitos del docente con casos de uso y preparar los diagramas. Hay una implementación local con pruebas, pero la nube, la IA y voz reales y la recepción push en un teléfono todavía requieren configuración y aceptación. El borrador no certifica la entrega final.

## 1 Problema y objetivo

Los equipos que diseñan un modelo de clases a distancia necesitan una pizarra común, identificar los cambios de cada participante y recuperar el contexto al volver a una sesión. Una IA utilizada por separado por cada integrante fragmenta esa conversación y no garantiza que el equipo conozca las propuestas o decisiones.

El objetivo es una herramienta CASE colaborativa donde los integrantes modelen clases, atributos, métodos y relaciones, y consulten a una IA común que asesore y proponga cambios únicamente cuando se le solicite. El proyecto debe conservar las funciones del primer parcial e incorporar persistencia NoSQL en nube y consulta móvil con notificaciones.

## 2 Alcance y límites

- Identidad y proyectos: registro, inicio de sesión, proyectos propios y acceso mediante invitación.

- Modelado: clases, atributos, métodos con parámetros, relaciones, validación, importación y exportación XMI.

- Colaboración: presencia, revisiones del documento, conversación IA compartida, actividad y continuidad de sesiones.

- Generación heredada: modelo relacional y aplicaciones Spring, Angular y Flutter. La aplicación generada es un producto distinto de la herramienta de modelado.

- Experiencia móvil: observar el diagrama y su evolución, consultar actividad y recibir avisos, sin editar el UML desde esa interfaz.

No se considera implementado un despliegue de nube por tener scripts de configuración. El observador móvil es web; no se afirma que exista una aplicación nativa publicada. Las firmas UML no generan automáticamente cuerpos de lógica de negocio.

Gemini es una opción admitida por la consigna. El usuario indicó que dispone de Gemini, pero todavía no se comprobó acceso a su API y no existe un adaptador Gemini en esta versión. Los adaptadores actuales son llama.cpp y Amazon Bedrock; Whisper se utiliza para transcripción.

## 3 Actores y permisos

- Visitante: registra una cuenta e inicia sesión.

- Propietario: crea y administra su proyecto e invita colaboradores.

- Colaborador: usuario con membresía EDITOR que consulta y modifica proyectos compartidos.

- Integrante móvil: participante que usa la interfaz informativa. Es un modo de uso, no un rol VIEWER protegido por el backend.

- Proveedor IA: sistema externo que responde consultas o devuelve propuestas estructuradas.

- Servicio de transcripción y proveedor push: sistemas externos para convertir voz en texto y entregar avisos del dispositivo.

MongoDB se representa como almacenamiento interno de la arquitectura, no como actor humano. La IA es un actor externo técnico; no debe presentarse como propietaria del proyecto ni como usuaria que modifica libremente la base de datos.

## 4 Reglas y requisitos de calidad

- RN-01 La conversación con la IA pertenece al proyecto y es compartida; no se ofrecen conversaciones privadas con el modelo.

- RN-02 Una consulta, revisión o resumen no modifica el UML. Una edición necesita una propuesta, confirmación explícita, permisos y revisión vigente.

- RN-03 Una revisión obsoleta se rechaza. El cliente recupera el documento actual antes de intentar otro cambio.

- RN-04 La voz es una exigencia de la consigna para pedir cambios de IA. Debe comprobarse el flujo real y aclararse con el docente si también admite texto para esa edición.

- RN-05 El contexto de IA es acotado: documento, participantes, hasta 20 mensajes recientes y hasta 50 hechos de actividad. Un resumen debe reconocer esa cobertura.

- RNF-01 Proteger acceso a proyectos mediante JWT y permisos; mantener claves y contraseñas fuera del repositorio público.

- RNF-02 Conservar documento, actividad y notificaciones mediante transacciones de MongoDB replica set. En despliegue utilizar HTTPS y WSS.

- RNF-03 Recuperar datos al recargar o retomar una sesión y comprobar convergencia después de desconexiones.

- RNF-04 Mostrar errores y reintentos sin aplicar cambios parciales ni presentar una respuesta del proveedor como aceptada sin evidencia.

Los objetivos numéricos de latencia, usuarios simultáneos y disponibilidad quedan por acordar. No se incluyen cifras inventadas como requisitos aprobados.

## 5 Catálogo de casos de uso

Se conserva el catálogo heredado CU-01 a CU-31. Los siguientes identificadores CU-SP son provisionales para el segundo parcial y no sustituyen aquella numeración.

- CU-SP-01 Consultar a la IA en la conversación grupal — RF-SP-04 y RF-SP-08.

- CU-SP-02 Solicitar una revisión del diagrama — RF-SP-06.

- CU-SP-03 Solicitar un resumen de lo avanzado — RF-SP-07 y RF-SP-08.

- CU-SP-04 Solicitar y confirmar una edición mediante voz — RF-SP-05.

- CU-SP-05 Retomar una sesión con actividad registrada — RF-SP-09 y RF-SP-10.

- CU-SP-06 Observar el proyecto desde un móvil — RF-SP-03 y RF-SP-11.

- CU-SP-07 Activar y recibir notificaciones push — RF-SP-12.

### CU-SP-04 Solicitar y confirmar una edición mediante voz

Actor principal: propietario o colaborador con permiso de edición. Actores de apoyo: servicio de transcripción y proveedor IA. Precondiciones: sesión iniciada, acceso al proyecto, micrófono autorizado y proveedores disponibles.

1. El integrante solicita grabar una orden de edición.

1. La interfaz captura el audio, lo convierte a WAV y lo envía al servicio de transcripción.

1. El sistema procesa el texto con el modelo y el catálogo de elementos del proyecto.

1. El backend resuelve referencias, valida la intención y devuelve una propuesta asociada a baseRevision.

1. El integrante revisa la propuesta y confirma su aplicación.

1. La autoridad colaborativa comprueba permisos y revisión, persiste el cambio y registra la actividad.

1. Los clientes recuperan el estado confirmado y muestran el mismo diagrama.

Alternativas: permiso de micrófono denegado, transcripción fallida, proveedor no disponible, orden ambigua o revisión obsoleta. En estos casos se informa el problema y no se aplica la propuesta.

Postcondición de éxito: documento actualizado con autoría y revisión coherentes. Si se cancela la propuesta, el documento queda intacto. Pendiente: aceptación con voz y modelo reales y comprobación de que el equipo puede consultar la traza de la orden y la propuesta.

### CU-SP-03 Solicitar un resumen de lo avanzado

Actor principal: integrante con acceso. Precondición: proyecto abierto y proveedor IA disponible.

1. El integrante abre la conversación común y selecciona el resumen.

1. El backend reúne el documento, los participantes y el contexto reciente con su cobertura.

1. La IA devuelve un resumen; el sistema guarda y publica la respuesta para el grupo.

1. Los participantes consultan la misma respuesta sin alterar el UML.

Alternativas: sin actividad previa se informa esa condición; ante contexto insuficiente no se inventan hechos; ante fallo del proveedor se conserva el trabajo y se permite reintentar. Pendiente: demostrar el caso con un integrante que llega tarde y un proveedor real.

Para detallar los demás casos se usará esta plantilla: objetivo, actores, requisito relacionado, precondiciones, disparador, flujo principal, alternativas, postcondiciones y evidencia de aceptación.

## 6 Arquitectura y modelo de información

El frontend Vue 3 utiliza Vuetify, Pinia y Vue Flow. Accede al backend Spring Boot mediante REST y STOMP. El backend es la autoridad para permisos, validación, revisiones y persistencia. El guardado manual usa REST con revisión optimista y reconciliación cada 2,5 segundos; las operaciones del asistente y la presencia emplean STOMP.

MongoDB replica set conserva proyectos, membresías, mensajes IA, actividad, sesiones, visitas, notificaciones y la cola push. El documento UML embebe clases, atributos, métodos, parámetros, relaciones y layout; las clases UML no son colecciones independientes.

El asistente construye un contexto acotado y llama al proveedor configurado. Sus propuestas pasan por normalización y validación antes de su confirmación. La infraestructura de transcripción y los modelos son procesos o servicios externos, no parte del ejecutable Spring.

Push utiliza una suscripción vinculada al usuario, una cola transaccional y un trabajador con cifrado VAPID y reintentos. El service worker muestra texto genérico y comprueba el destinatario. La configuración está desactivada hasta disponer de claves estables y una prueba válida.

## 7 Plan de diagramas

- Casos de uso: delimitar Forge Studio, separar actores humanos y servicios externos, y relacionar CU-SP con los requisitos.

- Modelo de dominio: proyecto y documento UML, clases, atributos, métodos y parámetros; distinguirlo del esquema físico de MongoDB.

- Componentes: usar docs/formal/forge-studio-componentes.mmd como base de la arquitectura implementada.

- Secuencia de edición IA: usar docs/formal/ia-metodos-secuencia.mmd; representar propuesta, confirmación y conflicto de revisión.

- Secuencia push: usar docs/formal/web-push-secuencia.mmd; representar suscripción, transacción, envío y apertura del proyecto.

- Despliegue: dibujar la topología prevista y marcarla como propuesta hasta elegir nube, configurar MongoDB remoto y comprobar HTTPS/WSS.

Los archivos nuevos de casos de uso y dominio se guardan como fuentes editables en docs/formal/. No se presentan como diagramas finales aprobados ni como capturas de un despliegue existente.

## 8 Verificación y evidencias

La evidencia registrada en los incrementos previos incluye una ejecución de 121 pruebas backend de push, actividad, notificaciones, chat y colaboración; dos pruebas adicionales de cifrado/VAPID; y 21 pruebas frontend con build correcto. Esos resultados no se suman a regresiones históricas como si fueran casos distintos ni sustituyen una aceptación integral.

Existe una prueba STOMP real de creación, actualización y eliminación de un método temporal en un proyecto QA. Las pruebas de conversación y entrega push usan transporte controlado. No acreditan calidad de inferencia, reconocimiento de voz física o visualización del aviso en un teléfono.

Cada evidencia nueva debe registrar caso de uso, requisito, versión o commit probado, fecha, entorno, participantes de prueba, pasos, resultado esperado, resultado observado y archivo de respaldo. Una prueba fallida permanece abierta.

Prioridades: confirmar acceso a Gemini API y su integración; probar conversación y voz con dos cuentas; configurar nube/NoSQL/HTTPS; aceptar push en móvil; y recertificar los casos heredados y las aplicaciones generadas.

## 9 Estructura del informe final y fuentes

1. Portada con datos académicos confirmados y control de versión.

1. Problema, objetivos, alcance y reglas de negocio.

1. Requisitos funcionales y no funcionales con trazabilidad.

1. Actores y especificaciones de casos de uso.

1. Análisis y modelo de dominio.

1. Diseño de componentes, secuencias y despliegue.

1. Implementación y decisiones técnicas.

1. Pruebas, evidencias, limitaciones y pendientes.

1. Manual de instalación, uso y demostración.

1. Conclusiones, referencias y anexos de diagramas.

Fuente de requisitos: transcripción del docente proporcionada por el estudiante en este chat. La equivalencia completa del primer parcial se contrastará con su consigna original antes de cerrar el informe.

Fuentes técnicas: CONTINUAR.md; docs/runtime/evaluacion-requisitos-segundo-parcial.md; docs/runtime/integraciones-segundo-parcial.md; docs/runtime/web-push.md; y docs/puds/use-cases.md. Los cierres históricos de ese catálogo no certifican automáticamente el frontend Vue actual.

Repositorio de trabajo: https://github.com/Leo14fel/Segundo-2

## 10 Matriz inicial de requisitos y aceptación

La matriz relaciona requisito, comprobación observable, caso de uso y brecha actual. Todos los estados son de trabajo; no constituyen aprobación del docente.

| Requisito | Aceptación observable | Caso de uso | Estado actual |
| --- | --- | --- | --- |
| RF-SP-01 Conservar el primer parcial | Ejecutar el catálogo heredado con Vue y comprobar los proyectos generados. | CU-01 a CU-31 | Recertificación pendiente |
| RF-SP-02 Identidad y permisos | Dos cuentas solo acceden a proyectos propios o compartidos y se rechazan accesos ajenos. | CU-28 a CU-31 | Implementación con pruebas locales |
| RF-SP-03 Colaboración en tiempo real | Dos cuentas convergen tras cambios, conflicto de revisión y reconexión. | CU-06 y CU-07; CU-SP-06 | Aceptación integral pendiente |
| RF-SP-04 IA grupal | Ambas cuentas ven los mismos mensajes y respuestas persistidos, con autoría. | CU-SP-01 | Implementado; falta proveedor real |
| RF-SP-05 Edición por voz a pedido | Orden por voz crea una propuesta; solo confirmar modifica y propaga el UML. | CU-08; CU-SP-04 | Flujo real pendiente |
| RF-SP-06 Revisión del diseño | La IA explica hallazgos sobre elementos existentes sin cambiar el documento. | CU-SP-02 | Implementado; falta proveedor real |
| RF-SP-07 Resumen para quien llega tarde | La IA resume hechos disponibles y comunica el límite del contexto. | CU-SP-03 | Implementado; aceptación pendiente |
| RF-SP-08 Contexto con participantes | Respuesta y registro permiten identificar autores y actividad sin inventar hechos. | CU-SP-01 y CU-SP-03 | Contexto implementado y acotado |
| RF-SP-09 NoSQL en nube | Aplicación y MongoDB remoto conservan la sesión al detener y retomar el trabajo. | CU-SP-05 | Nube por configurar |
| RF-SP-10 Continuidad registrada | Abrir otro dispositivo recupera diagrama, chat y actividad de la sesión. | CU-SP-05 | Implementación local; falta nube |
| RF-SP-11 Móvil informativo | El teléfono observa cambios y actividad, sin controles de edición del UML. | CU-SP-06 | Implementado; falta teléfono real |
| RF-SP-12 Avisos push | Otro integrante modifica el diagrama; el móvil recibe y abre el aviso autorizado. | CU-SP-07 | Implementado y desactivado; falta recepción real |
