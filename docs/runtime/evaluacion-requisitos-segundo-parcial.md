# Evaluación del alcance solicitado por el docente

Fecha: 8 de noviembre de 2026. Fuente de requisitos: transcripción proporcionada por el usuario. Revisión estática del código y de la evidencia de la migración Vue; no se ejecutó una nueva aceptación integral en esta revisión.

> Actualización: la matriz refleja los incrementos documentados en `integraciones-segundo-parcial.md`. Chat grupal, continuidad, observador móvil, métodos UML y Web Push tienen implementación. Modelos/voz reales, recepción push en teléfono y nube siguen pendientes de aceptación. Ver `CONTINUAR.md` en la raíz para retomar el trabajo.

## Conclusión

Conviene recuperar y verificar el alcance obligatorio antes de agregar funciones opcionales. La migración a Vue no demuestra por sí sola equivalencia con el primer parcial. La documentación histórica que declara todos los ciclos cerrados no certifica el nuevo frontend.

## Matriz de cumplimiento

| Exigencia | Evidencia actual | Pendiente |
| --- | --- | --- |
| Conservar todo el primer parcial | Backend y generadores conservados; modelo manual, XMI y ZIP probados en la migración | Recertificar cada CU con el frontend Vue y ejecutar las aplicaciones generadas; revisar si métodos UML pertenecían al alcance original |
| Pizarra multiusuario | Presencia STOMP y dos pestañas verificadas; guardado REST con revisión y consulta cada 2,5 s | Prueba con dos cuentas, conflictos simultáneos, reconexión y convergencia; decidir si migrar edición manual a operaciones STOMP para mayor fidelidad al protocolo previo |
| IA grupal, no privada | GroupAssistant, mensajes persistidos por proyecto/autor, STOMP y reconciliación HTTP | Aceptación con dos cuentas y proveedor real |
| IA identifica participantes y contexto | UML, miembros, mensajes recientes y hasta 50 hechos de actividad con autores y cobertura explícita | Probar respuestas reales sobre quién hizo qué y los límites del historial |
| Preguntar, revisar, editar y resumir | Vue integra ASK, REVIEW, EDIT, SUMMARY_CURRENT y propuestas compartidas confirmables | Aceptación de calidad y propagación con proveedor real |
| IA actúa solo a pedido | Interacción explícita y confirmación de propuestas | Demostrar ausencia de escrituras autónomas, validación de revisión y propagación del Apply a todos |
| Voz como orden de edición | Grabación y conversión WAV implementadas; endpoint de voz existente | Probar micrófono, transcripción y edición completas; precisar si el docente exige voz para toda edición de IA o también permite texto |
| Clases, atributos, métodos y relaciones | Dominio, inspector, validación, persistencia, XMI, actividad y herramientas IA de métodos implementados | Probar métodos con voz/modelo real; las firmas no generan cuerpos de negocio automáticamente |
| IA local opcional / nube utilizable | Adaptadores llama.cpp y Bedrock existentes | Configurar y demostrar al menos un proveedor real. No hace falta implementar tres proveedores distintos |
| Persistencia NoSQL en nube | MongoDB replica set local y URI configurable | Desplegar MongoDB y aplicación en nube, probar continuidad y recuperación. La configuración AWS escrita no es evidencia de despliegue activo |
| Pausar y retomar con registro | UI de actividad/sesiones/visitas, continuidad y avisos con lectura y paginación | Demostrar continuidad entre dispositivos en nube |
| Móvil informativo sin edición | Modo observador responsive, diagrama en vivo, chat y avisos; sin edición del UML | Aceptación en teléfono físico y contraste de permisos |
| Push móvil | PushManager, service worker, suscripciones, cola MongoDB y envío cifrado VAPID implementados y probados con transporte controlado | Configurar claves/HTTPS y demostrar recepción en teléfono; ver `web-push.md` |

## Casos de uso heredados

- CU-01–04: crear, abrir/guardar, modelar y validar UML.
- CU-05–07: Undo/Redo, colaboración y presencia.
- CU-08–11: texto/voz/imagen a UML e import/export XMI.
- CU-12–16: modelo relacional, Spring/JPA, CRUD/Auth, OpenAPI/Postman y Domain Manifest.
- CU-17–19: generar aplicaciones Angular/Flutter e interacción con sus datos mediante IA/voz. La app móvil generada no sustituye al observador móvil de la herramienta CASE.
- CU-20–23: absorbidos por CU-19 según documentación histórica.
- CU-24–25: runtimes de voz e IA.
- CU-26: descartado históricamente; confirmar que esa decisión siga siendo válida frente al alcance actual.
- CU-27: demo reproducible; recertificar tras la migración.
- CU-28–31: registro, login, ownership e invitaciones.

Los nuevos escenarios de chat grupal, revisión contextual, resumen para quien llega tarde, continuidad y observación móvil/push deben quedar trazados sin asignar números definitivos que contradigan el catálogo existente.

## Orden recomendado

1. Congelar una matriz de requisitos obligatorios y criterios de aceptación basada en esta transcripción y el primer parcial.
2. Recertificar lo heredado: el script de aceptación ya usa `npm test` del frontend Vue; faltan pruebas integrales de las aplicaciones generadas.
3. Configurar un proveedor IA y voz reales y probar la conversación compartida y métodos con dos participantes.
4. Preparar credenciales de nube/NoSQL con la cuenta que el usuario elija; todavía no tiene nube configurada.
5. Configurar claves push/HTTPS y aceptar la experiencia móvil y la recepción real de notificaciones.
6. Desplegar aplicación y NoSQL en nube con HTTPS/WSS y comprobar pausa/reanudación.
7. Ejecutar demo integral, reunir evidencias y cerrar documentación con la arquitectura realmente entregada.

La documentación debe avanzar desde el primer paso como matriz y registro de decisiones; los diagramas finales, capturas y estados CERRADO se actualizan después de aceptar los flujos. No conviene añadir funciones cosméticas mientras existan estas brechas obligatorias.

## Límites conocidos de la versión Vue

- Undo/Redo usa instantáneas en memoria y se invalida con cambios externos; no mantiene el mismo historial de comandos del frontend anterior.
- Autoorganizar guarda una posición por petición; no es un único BATCH atómico.
- Actividad, sesiones y notificaciones ya cuentan con vistas operativas, lectura y paginación; queda aceptación integral entre dispositivos.
- Hay adaptadores y acciones heredados de la referencia que solo lanzan errores de no soportado; limpiar los no utilizados después de consolidar los flujos definitivos.
- Las pruebas Vue y la generación de un ZIP no certifican todos los casos de uso ni que el contenido generado compile o funcione.
