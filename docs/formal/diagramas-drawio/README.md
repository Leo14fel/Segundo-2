# SinapUML · Diagramas PUDS

Versión documental del 9 de noviembre de 2026. Los 25 diagramas corresponden a las reservas D01–D25 del Word V4. Son una base revisada contra el código, pendiente de validación académica del docente.

## Abrir y editar

1. Extraer el ZIP completo antes de abrir sus archivos.
2. En draw.io Desktop: Archivo → Abrir y elegir `SinapUML-PUDS.drawio`.
3. Cambiar de diagrama con las 25 pestañas inferiores. Textos, formas, conectores y posiciones son editables.
4. Para trabajar por separado, abrir cualquiera de los archivos `Dxx-*.xml` con draw.io.
5. Guardar una copia antes de cambiar el modelo; los XML individuales y el archivo maestro son instantáneas, sin sincronización automática entre ellos.

## Imágenes para la documentación

- `png/`: imágenes con fondo blanco, exportadas por draw.io; útiles para revisar e insertar en Word.
- `svg/`: imágenes vectoriales para ampliar sin pixelación. Si Word admite SVG, preferir este formato.
- `index.html`: galería local con enlaces a cada imagen y XML; funciona sin subir archivos a un servicio.
- `manifest.json`: inventario de archivos y dimensiones de los lienzos.

Insertar cada imagen en la reserva del mismo código del Word y conservar su pie de figura. Diagramas extensos, especialmente D14, D18, D22 y D25, necesitan una página completa o una sección horizontal; no reducirlos a un recuadro de tres pulgadas si el texto pierde legibilidad. Actualizar los índices después de insertarlos. El Word V4 se conserva sin modificar.

## Convenciones y alcance

Los casos CU-SP-01 a CU-SP-07 conservan la numeración de la documentación. Los casos heredados del primer parcial se agrupan en D03 por legibilidad; esta vista no sustituye su catálogo ni acredita su recertificación.

En D07–D13 los enlaces muestran números de mensaje. La lista inferior especifica orden, emisor, receptor y acción, incluidos los mensajes al propio objeto; no se usa la posición espacial para representar el tiempo. Proyecto y registros es una abstracción de análisis, mientras las secuencias de diseño sí identifican MongoDB.

En D14 el rombo lleno indica composición, y las multiplicidades aparecen cerca de los extremos. D17 representa agregados documentales; D18 muestra colecciones e índices seleccionados, sin sugerir una colección por clase UML ni claves foráneas SQL.

En secuencias, línea discontinua representa una respuesta; las líneas de vida son verticales. Los fragmentos alt muestran un escenario principal y una alternativa; opt identifica el resumen opcional de CU-SP-05. Los participantes de backend agrupan servicios y controles de acceso; las flechas hacia MongoDB se ejecutan desde el servidor.

La nube de D16 es una propuesta: no hay proveedor ni cuenta configurados. El móvil es un modo informativo de interfaz, no un rol VIEWER persistido. Push está desactivado por defecto; SENT acredita aceptación del proveedor, no recepción física. No se afirma Gemini integrado ni aceptación de IA/voz reales.

La ruta de voz devuelve la propuesta al solicitante y comparte la operación confirmada. La difusión grupal completa de la propuesta de voz está pendiente de verificar/completar. D10 y D22 lo señalan; no se inventó un chat de voz grupal que el código actual no demuestra.

## Fuentes y mantenimiento

Se contrastó el documento PUDS V4 y el código de ProjectAssistantService, ProjectAssistantContextService, AssistantVoiceService, AssistantPlanService, editor-sync.ts, ProjectTools.vue, continuidad/sesiones, PushDeliveryService y MongoPersistenceConfiguration. Estas vistas no ejecutan pruebas de aceptación ni cambian código de la aplicación.

Constructor reproducible: `scripts/build-puds-drawio.py`. Exportador local: `scripts/export-puds-drawio.ps1` (requiere draw.io Desktop). Si se regenera el XML, volver a exportar y revisar las imágenes; el constructor puede reemplazar las ediciones manuales hechas en sus archivos de salida.

## Correspondencia con el documento

| Código | Vista | Sección PUDS |
| --- | --- | --- |
| D01 | Actividad del modelado colaborativo | 3.2 Modelo de negocio |
| D02 | Actores de SinapUML | 4.1 Actores |
| D03 | Modelo general de casos de uso | 4.4 Casos de uso |
| D04 | Paquetes de análisis | 5.1.1 Paquetes |
| D05 | Dependencias entre paquetes | 5.1.2 Dependencias |
| D06 | Casos de uso y responsabilidades | 5.2 Paquetes y casos |
| D07 | Comunicación · CU-SP-01 | 5.3.1 Comunicación |
| D08 | Comunicación · CU-SP-02 | 5.3.2 Comunicación |
| D09 | Comunicación · CU-SP-03 | 5.3.3 Comunicación |
| D10 | Comunicación · CU-SP-04 | 5.3.4 Comunicación |
| D11 | Comunicación · CU-SP-05 | 5.3.5 Comunicación |
| D12 | Comunicación · CU-SP-06 | 5.3.6 Comunicación |
| D13 | Comunicación · CU-SP-07 | 5.3.7 Comunicación |
| D14 | Modelo de dominio | 5.4 Dominio |
| D15 | Arquitectura lógica | 6.1.1 Arquitectura lógica |
| D16 | Arquitectura física y despliegue | 6.1.2 Arquitectura física |
| D17 | Modelo lógico documental | 6.2.1 Datos lógicos |
| D18 | Persistencia física MongoDB | 6.2.2 Datos físicos |
| D19 | Secuencia · CU-SP-01 | 6.3.1 Secuencia |
| D20 | Secuencia · CU-SP-02 | 6.3.2 Secuencia |
| D21 | Secuencia · CU-SP-03 | 6.3.3 Secuencia |
| D22 | Secuencia · CU-SP-04 | 6.3.4 Secuencia |
| D23 | Secuencia · CU-SP-05 | 6.3.5 Secuencia |
| D24 | Secuencia · CU-SP-06 | 6.3.6 Secuencia |
| D25 | Secuencia · CU-SP-07 | 6.3.7 Secuencia |
