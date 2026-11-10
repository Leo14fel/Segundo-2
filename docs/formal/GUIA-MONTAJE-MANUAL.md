# SinapUML: montaje manual de los diagramas

## Qué abrir

- `Documentacion_PUDS_V4.docx`: base PUDS sin diagramas insertados. Conserva los 25 espacios D01–D25. Es una versión anterior: las frases sobre XML futuros deben actualizarse cuando termines de insertarlos.
- `diagramas/SinapUML-PUDS-Academico-V2.drawio`: maestro editable con 39 pestañas.
- `diagramas/index.html`: galería para elegir las vistas.
- `ubicacion-diagramas.csv`: correspondencia con las secciones del Word y archivos de cada figura.

Los XML individuales y el maestro son copias independientes. Elegí uno como fuente de tus cambios y guardá una copia antes de editar. Estas vistas son borradores editables: revisá la notación y el contenido antes de incluirlos en tu entrega.

## Flujo de trabajo

1. Extraé el ZIP completo. Abrí el Word y guardá una copia con otro nombre.
2. Abrí el maestro `.drawio` en draw.io Desktop. Elegí una pestaña y ajustá textos, distribución o flechas.
3. Exportá solamente esa pestaña a PNG, con fondo blanco y recorte al contenido. Revisá la imagen completa antes de insertarla. Podés empezar con los PNG incluidos; si el texto queda chico, simplificá o dividí el diagrama dentro de draw.io y volvé a exportar.
4. En Word, buscá el código D01, D02, etc. del espacio reservado y reemplazá el cuadro por la imagen. Insertala «En línea con el texto», centrada y con proporciones bloqueadas. Eliminá el cuadro vacío y las notas «Espacio para insertar» y «XML previsto» de esa figura.
5. Mantené A4. Para una vista ancha, creá saltos de sección antes y después y aplicá orientación horizontal solamente a esa sección. Usá una figura por página si hace falta. Evitá cambiar todo el documento de orientación.
6. Conservá el pie numerado existente para D01–D25; cambiá su texto si corresponde. Para las vistas adicionales usá Referencias → Insertar título, etiqueta «Figura». No escribas a mano la numeración.
7. Al terminar, seleccioná el documento con Ctrl+A y actualizá los campos con F9. Actualizá el índice completo y el índice de figuras. Exportá un PDF y revisá cada página al 100 %.

## Dónde ubicar las vistas adicionales

Las 25 vistas D01–D25 ya tienen reserva en V4. Las otras 14 son ampliaciones y necesitan espacio nuevo:

- `CU-SP-01` a `CU-SP-07`: debajo de la ficha del caso correspondiente, en 4.3 Detallar casos de uso.
- `AC-SP-01` a `AC-SP-07`: en 5.3 Analizar casos de uso, antes de su comunicación D07–D13, respectivamente.

Las secuencias D19–D25 son extensas. Si no se leen en A4 horizontal, dividilas en draw.io en puntos sin mensajes cortados, repetí los participantes y marcá «Parte 1» y «Parte 2». No achiques la imagen hasta que el texto resulte ilegible.

## Lista de revisión

- Actores fuera del límite del sistema; nombres coherentes con el caso de uso.
- `include` apunta al comportamiento incluido; `extend` apunta al caso base y tiene una condición.
- Comunicación con mensajes numerados; secuencia con flechas, retornos y participantes legibles.
- Análisis BCE como modelo conceptual: sus controles no son necesariamente clases implementadas.
- Arquitectura coherente con Vue, Spring Boot y MongoDB. La nube sigue propuesta hasta desplegarla.
- Ninguna línea o palabra cortada; pies junto a sus imágenes; sin reservas vacías ni títulos huérfanos.
- Incorporar diagramas no demuestra aceptación de IA, voz, nube ni recepción push. Mantener sus estados reales.

## Google Docs

El documento conectado es el borrador inicial de las bases, no el Word PUDS V4 ni la versión de 77 páginas. Se corrigió a SinapUML, se actualizaron los datos académicos conocidos y se uniformaron los títulos, conservando su contenido y tabla. Para trabajar con la estructura PUDS completa, usá la base Word incluida; si preferís Google Docs, subí una copia a tu propia cuenta y verificá su conversión antes de insertar imágenes. Los permisos del documento remoto no se cambiaron.
