# Docs apagados y logs sin datos

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `backend/app/core/logging_config.py`
- `backend/app/main.py`
- `backend/app/services/smtp_sender.py`

## Decisión cerrada

En producción no se publican `/docs` ni el schema. El log no lleva email, nombre, monto, `Message-ID` ni el token de baja. Sentry es otro ticket y espera a este, porque los dos tocan `main.py`.

## Resultado

Un envío se puede seguir por `envio_id` o `ciclo_id`. El path de la baja se loguea como ruta, no como token.

## Criterios de aceptación

- Con el entorno de producción, `docs_url`, `redoc_url` y el schema público quedan apagados.
- `smtp_sender` no loguea email ni `Message-ID`. El rate limit de 5 cada 30 segundos no se toca.
- El access log no guarda el valor de `/unsubscribe/{token}`.
- No se agrega `structlog`. No se agrega el SDK de Sentry en este ticket.
- `main.py` queda libre para Sentry en el plan gratis cuando este ticket esté `resolved`.

## Pregunta

¿Qué deja de verse en público y en los logs antes de un ciclo real?
