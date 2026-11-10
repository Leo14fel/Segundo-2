# Notificaciones Web Push de Forge Studio

Implementación del 8 de noviembre de 2026. Estado: integrada y con pruebas automatizadas; falta aceptación en dispositivo real. No se ha solicitado permiso de notificaciones ni enviado un push a un teléfono durante esta implementación. Por defecto está desactivada.

## Flujo implementado

1. Un integrante activa **Herramientas → Actividad → Avisos → Activar notificaciones** en su navegador. El permiso se solicita únicamente por esa acción.
2. `PushManager` crea una suscripción. La API autenticada guarda endpoint y claves de cifrado asociados al usuario; otra cuenta no puede apropiarse de ese endpoint ni borrarlo.
3. Un cambio de diagrama o cierre de sesión genera las notificaciones existentes para los demás miembros. Dentro de la misma transacción MongoDB se agregan trabajos a `push_deliveries`, uno por suscripción y notificación.
4. Un trabajador reclama trabajos mediante `findAndModify` y un lease. Fuera de la transacción envía un payload cifrado con Web Push / VAPID. Se limita a 20 trabajos por pasada y 8 intentos por trabajo, con espera creciente.
5. Respuesta 2xx marca SENT; 404/410 elimina la suscripción vencida y marca DEAD. Los demás fallos se reintentan. Los trabajos vencen a los siete días mediante un índice TTL sobre un **BSON Date**; los demás instantes conservan los conversores históricos del proyecto.
6. El service worker comprueba la cuenta vinculada al dispositivo y muestra un texto genérico. Al pulsar, abre el proyecto en Actividad; la aplicación vuelve a comprobar autenticación y acceso. Cerrar sesión desvincula el worker e intenta eliminar la suscripción.

La entrega es al menos una vez: una caída después de enviar y antes de confirmar puede repetir un envío. `tag` usa el ID de la notificación para reemplazar el aviso equivalente en el dispositivo. No es una garantía de entrega inmediata o exactamente una vez.

## Preparar las claves

Desde la raíz del repositorio, con Node 24:

```powershell
node scripts/generate-push-keys.mjs
```

Genera una pareja P-256 en `backend/data/push.local.env`, ignorado por Git; nunca imprime las claves ni sobrescribe un archivo existente. Cambiar `SINAPUML_PUSH_SUBJECT` por un contacto real `mailto:...`, y activar `SINAPUML_PUSH_ENABLED=true` al preparar la prueba. Mantener la clave privada únicamente en el backend. Conservar la misma pareja entre reinicios; si se rota, desactivar y volver a activar los dispositivos.

En PowerShell, cargar esas variables **en la misma terminal que iniciará el backend**:

```powershell
Get-Content -LiteralPath backend/data/push.local.env | ForEach-Object {
    if ($_ -match '^(SINAPUML_PUSH_[A-Z_]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
    }
}
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot'
Set-Location backend
.\gradlew.bat bootRun
```

Si el backend ya ocupa 8082, detener su proceso identificado antes de iniciar otro. No requiere reiniciar MongoDB ni borrar sus datos. El servidor rechaza una configuración habilitada sin claves/contacto.

Para despliegue, pasar las cuatro variables `SINAPUML_PUSH_*` del ejemplo `deploy/aws/sinapuml.env.example` mediante la configuración privada del servidor. No incrustar la clave privada en variables `VITE_*`, JavaScript, ZIP público o documentación.

## Condiciones de navegador y red

- Web Push necesita un contexto seguro y soporte de Service Worker, PushManager y Notifications. `localhost` permite desarrollo de escritorio; entrar desde un teléfono mediante la IP LAN con HTTP no equivale a HTTPS.
- El móvil necesita una URL HTTPS accesible, sesión iniciada y un navegador que admita esta función. La instalación como aplicación y el funcionamiento en segundo plano dependen de la plataforma; el manifiesto e iconos están incluidos.
- Permitir salida HTTPS del backend hacia `fcm.googleapis.com`, `updates.push.services.mozilla.com` y `web.push.apple.com`. Solo se aceptan endpoints HTTPS de esos hosts exactos, sin credenciales ni redirecciones HTTP. Otros proveedores requerirán una configuración deliberada de `sinapuml.push.allowed-hosts`.
- No se almacenan JWT ni contenido privado en el service worker. El texto del aviso es siempre «Tienes novedades en un proyecto compartido». No se cachean APIs para acceso sin conexión.
- El sistema no necesita Firebase Admin ni una cuenta de Firebase para este transporte VAPID. La infraestructura de entrega sigue siendo la del navegador; la aplicación y MongoDB todavía requieren su propia configuración de nube.

Fundamento de las APIs: [PushManager.subscribe (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/PushManager/subscribe). Cifrado y VAPID: [webpush-java](https://github.com/web-push-libs/webpush-java).

## Aceptación pendiente con dos cuentas

1. Configurar claves estables, backend y HTTPS. Abrir la cuenta B en el teléfono y activar push desde Avisos. Comprobar que la API devuelve configuración habilitada.
2. Compartir un proyecto entre A y B. Mantener el teléfono en modo informativo y cerrar o pasar la aplicación a segundo plano.
3. A agrega o modifica una clase. Verificar una notificación persistida para B, un trabajo SENT y la recepción del aviso en el teléfono. El autor no recibe su propia notificación de actividad.
4. Pulsar el aviso: abre el proyecto autorizado en Actividad y recupera el diagrama actual. Repetir después de recargar e iniciar sesión.
5. Desactivar push y repetir un cambio: debe seguir apareciendo el aviso dentro de la aplicación, sin un nuevo envío a ese dispositivo. Cerrar sesión o cambiar de cuenta no debe mostrar avisos de la anterior.
6. Registrar navegador, sistema operativo, hora y evidencia. Un trabajo SENT confirma aceptación del proveedor, no que el teléfono lo haya mostrado.

El modo observador es una experiencia web móvil; no constituye una aplicación nativa publicada. La aceptación de push y el requisito de nube siguen abiertos hasta probarlos realmente.
