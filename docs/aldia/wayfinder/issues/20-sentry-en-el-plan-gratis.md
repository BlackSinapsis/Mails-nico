# Sentry en el plan gratis

Type: task
Modo: AFK
Status: open
Blocked by: 09, 10
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `backend/requirements.txt`
- `backend/app/main.py`
- `frontend/src/main.tsx`
- `frontend/package.json`
- `frontend/package-lock.json`

## Decisión cerrada

Sentry entra en el plan Developer (USD 0). Sin mail ni token en el evento. Sin Grafana.

## Resultado

Un error del watcher o del envío llega a Sentry, en backend y en frontend.

## Criterios de aceptación

- `sentry-sdk` (MIT) y el SDK del frontend, en el cupo gratis.
- El evento no lleva email, nombre, monto, `Message-ID` ni token de baja. Hereda el filtro de Docs apagados y logs sin datos.
- `main.tsx` queda listo para que Rediseño visual y modo oscuro agregue la clase `dark` sin volver a inicializar el SDK a ciegas: la inicialización queda en un módulo chico si hace falta, y `main.tsx` igual está en Archivos de este ticket hasta que cierre.
- No se crea la cuenta de Sentry en el panel. Si falta el DSN, el proceso arranca igual.

## Pregunta

¿Dónde se ve el stack de un fallo del watcher sin cazar logs a mano?
