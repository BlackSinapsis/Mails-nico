# Baja por POST

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `backend/app/routers/unsubscribe.py`
- `backend/tests/test_unsubscribe_router.py`
- `backend/tests/test_security_unsubscribe_token.py`

## Decisión cerrada

Abrir el link no da de baja. El POST, con un botón, sí. El header del mail lo escribe Escapar el HTML del mail.

## Resultado

`GET /unsubscribe/{token}` muestra una página y no cambia datos. El POST aplica `prefiere_no_recibir_email`. El POST one-click del RFC 8058 también.

## Criterios de aceptación

- El GET no escribe. El prefetch de un antivirus no silencia al consorcio.
- El HMAC actual se mantiene. Un token truncado sigue en 400.
- El log de este router no lleva mail, nombre ni token. El access log que guarda el path lo corrige Docs apagados y logs sin datos.
- Un Excel no vuelve el flag a falso. Hay un test en este router o se apoya en el del diff del maestro, sin editar `maestro_service.py`.

## Pregunta

¿Cómo se evita que un antivirus dé de baja a un consorcio?
