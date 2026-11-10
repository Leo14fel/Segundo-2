# SinapUML · Diagramas académicos V2

Nueva versión basada en las siete capturas proporcionadas por el estudiante. Conserva la versión anterior y el Word V4. Fecha: 9 de noviembre de 2026.

## Uso

Abrir `SinapUML-PUDS-Academico-V2.drawio` en draw.io Desktop mediante Archivo → Abrir. Contiene 39 pestañas: 25 vistas D01–D25, siete detalles CU-SP y siete realizaciones de análisis AC-SP. También hay XML individuales y exportaciones PNG/SVG. `index.html` es una galería local.

Los códigos D01–D25 mantienen su correspondencia con las reservas del Word. Los detalles CU-SP corresponden a las fichas de 4.3; AC-SP amplía las realizaciones del capítulo de análisis. Para incorporar estas vistas adicionales hay que añadir sus figuras e índice en una siguiente versión del Word.

## Criterios aplicados de las referencias

- Presentación académica sobria, fondo blanco y marcos identificados por caso de uso.
- Casos de uso con actores, include y extend únicamente cuando la semántica del flujo lo justifica. La autenticación existente se trata como precondición; no se inventan roles de administrador, vendedor o cliente.
- Comunicación con símbolos boundary, control y entity, mensajes próximos a sus enlaces y dirección indicada en el texto. Las operaciones son abstracciones de análisis, no nombres nuevos de endpoints.
- Realizaciones de análisis en tres compartimentos, separando datos y operaciones de interfaz/control. No se atribuyen métodos CRUD ficticios a las entidades.
- Arquitectura lógica en capas; despliegue con nodos tridimensionales y artefactos contenidos.
- Secuencias con líneas de vida, mensajes, retornos, fragmentos alternativos y barras de activación. Las barras indican ejecución conceptual; no representan hilos medidos en runtime.

La tecnología sigue siendo Vue, Java/Spring Boot y MongoDB. No se copian PostgreSQL, Prisma, Node backend, Railway, Aiven ni Vercel de las capturas. La nube es propuesta; Gemini no está integrado; voz/IA reales y recepción push física siguen pendientes. El modo móvil no es un rol VIEWER persistido. Las propuestas de voz se devuelven al solicitante; se comparte el cambio confirmado, y la difusión completa de la propuesta de voz necesita verificación.

## Correspondencia del análisis con la implementación

Los controles de AC-SP son abstracciones para la documentación PUDS y no clases adicionales implementadas. Su responsabilidad se distribuye en:

- AC-SP-01: ProjectAssistantService.send(ASK), ProjectAssistantContextService, ProjectAssistantMessageStore.
- AC-SP-02: ProjectAssistantService.send(REVIEW), validFindings, AssistantReview.
- AC-SP-03: ProjectAssistantService.send(SUMMARY_CURRENT), ProjectAssistantContextService.
- AC-SP-04: ProjectTools.vue, AssistantVoiceService.plan, AssistantPlanService.planVoice, colaboración.
- AC-SP-05: ProjectContinuityService, ProjectSessionService, ProjectService.
- AC-SP-06: editor-sync.ts, API de proyecto, presencia STOMP, modo observer.
- AC-SP-07: PushSubscriptionService, PushDeliveryService, service worker.

## Edición y mantenimiento

Los XML individuales y el maestro son copias independientes, sin sincronización automática. Guardar una copia antes de modificar. El constructor `scripts/build-puds-drawio-v2.py` regenera su carpeta y puede reemplazar ediciones manuales. Exportar con `scripts/export-puds-drawio.ps1 -DiagramDirectory docs/formal/diagramas-drawio-v2`. Los diagramas extensos requieren página completa o sección horizontal en Word; no reducirlos a un espacio donde sus textos queden ilegibles.

Las referencias orientan notación y estructura. No acreditan que el docente haya validado estos nuevos modelos ni sustituyen pruebas reales de la aplicación.
