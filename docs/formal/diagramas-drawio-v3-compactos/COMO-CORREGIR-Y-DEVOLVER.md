# Cómo corregir y devolver los diagramas

1. Abrí `SinapUML-PUDS-Compactos-V3.drawio` y guardá una copia como `SinapUML-Corregido.drawio`. Corregí esa copia, sin regenerar los archivos con scripts.
2. Empezá por CU-SP-01 y sus vistas AC-SP-01, D07 y D19. Contrastá actor, objetivo, responsabilidades y mensajes con la ficha 4.3.1 del Word. Después repetí la revisión para los demás casos.
3. Corregí conectores, nombres, textos o distribuciones usando las formas nativas de draw.io. Conservá los códigos y el número de parte. Las clases de análisis son conceptos de diseño; no deben confundirse con nombres exactos de clases implementadas.
4. Revisá el resultado en `index.html` o en una impresión al 100 %. Las exportaciones incluidas corresponden al borrador: después de editar el maestro deben regenerarse. El maestro y los XML individuales no se actualizan mutuamente.
5. Completá `control-revision.csv`: cambios realizados y cuáles están listos para insertar. Si preferís, podés comunicar los códigos y cambios por el chat.
6. Devolvé `SinapUML-Corregido.drawio` y el CSV o tus observaciones. Con esa fuente se podrán exportar las imágenes definitivas y reemplazar las reservas del Word.

## Tamaño para la documentación

- Documento A4 vertical con los márgenes actuales.
- Cada lámina se ajustará proporcionalmente dentro de **16 cm de ancho y 11.3 cm de alto**; son máximos, no dimensiones que deban forzarse.
- `tamano-insercion.csv` indica las dimensiones proporcionadas para cada PNG. La letra estimada a ese tamaño está alrededor de 9 puntos. Si agregás texto y deja de leerse, dividí la vista o simplificá los rótulos.
- No deformar las imágenes, cortar mensajes ni reducir una vista extensa hasta perder legibilidad. Las partes comparten código y repiten participantes cuando corresponde.
- Los títulos y notas extensas se incorporarán como texto de Word. Los pies se numerarán con campos de figura y se actualizarán ambos índices.
- Las imágenes PNG son para revisar el borrador. La exportación definitiva se hará desde el archivo corregido, con calidad suficiente para imprimir.

## Antes de marcar listo

Comprobar las direcciones de include y extend, los extremos de generalización y composición, las multiplicidades y el orden de mensajes. Revisar las condiciones de los escenarios alternativos y la notación de fragmentos que requiera el docente. Distinguir nube propuesta, implementación local y aceptación real. Las secuencias continúan su numeración entre partes y no deben leerse como escenarios independientes sin su contexto.

El informe V7 conserva sus espacios vacíos deliberadamente. Las nuevas figuras se montarán cuando estén corregidas; no se reutilizará el formato A3 del montaje anterior.
