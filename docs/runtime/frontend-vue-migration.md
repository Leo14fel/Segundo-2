# Forge Studio: reconstrucción del frontend

Fecha: 2026-11-08.

El frontend ejecutable se sustituyó por Vue 3 + Vuetify + Pinia + Vue Flow, tomando los componentes, tema oscuro y organización visual del ZIP de referencia. No quedan dependencias Angular/JointJS ni componentes del frontend anterior en la aplicación ejecutable. El backend, la base y los contratos existentes se conservaron. El respaldo y la documentación histórica permanecen fuera del build.

## Verificación ejecutada

- Build TypeScript/Vite de producción correcto.
- 5 pruebas automatizadas: round-trip de tipos/identificadores/nulabilidad/layout, operaciones no soportadas, guardar/Undo/Redo, rechazo por revisión y cambio remoto.
- En navegador: login con cuenta local, crear proyecto, agregar/editar clase y atributo, relación con multiplicidades, Undo/Redo, recarga y reapertura del modelo persistido.
- Dos pestañas: presencia de dos sesiones y propagación de una clase nueva; Undo desde la segunda sesión restauró las dos clases originales.
- API a través del proxy nuevo: validación UML, exportación XMI, preview y apply del mismo XMI.
- Generación real de ZIP Spring/Angular/Flutter: HTTP 200 (386156 bytes en la prueba).

## Límites explícitos

- Undo/Redo pertenece a la sesión del navegador y se invalida con cambios externos. No sobrevive a recargas.
- Guardado REST con revisión optimista; STOMP para presencia y operaciones del Assistant. Consulta autoritativa cada 2,5 segundos para recibir guardados REST remotos.
- No se ejecutaron inferencias IA, transcripción ni visión porque requieren los runtimes locales. Sus llamadas, previews, confirmación STOMP y errores están integrados.
- La grabación convierte audio a WAV PCM mono 16 kHz antes de enviarlo. No se probó el micrófono físico ni se solicitaron permisos de grabación durante QA.
- Actividad, sesiones, conversación y notificaciones tienen consulta en el panel de herramientas; sus resultados se muestran en detalle. No son una réplica de las pantallas históricas Angular.
- El incremento posterior añadió métodos UML (operaciones), herramientas IA y XMI. VIEWER y cambios/eliminación de colaboradores siguen sin ofrecerse. Ver `integraciones-segundo-parcial.md`.
- El build advierte del tamaño del chunk de Vuetify (~608 kB sin gzip), sin errores de compilación.

## Ejecutar

Mantener MongoDB y Spring activos. En `frontend/`: `npm ci` y `npm run dev`. URL http://127.0.0.1:4200. También existe `npm start` como alias.
