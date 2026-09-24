# El logout invalida la sesión

Type: task
Modo: AFK
Status: open
Blocked by: 03
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/models/user.py`
- `backend/app/core/security.py`
- `backend/app/core/dependencies.py`
- `backend/app/services/auth.py`
- `backend/app/routers/auth.py`
- `backend/app/schemas/auth.py`
- `backend/tests/test_auth.py`
- `backend/tests/test_security.py`
- `backend/tests/test_change_credentials.py`
- `backend/alembic/versions/0008_tokens_valid_after.py`
- `frontend/src/hooks/useAuth.ts`
- `frontend/src/services/auth.ts`

## Decisión cerrada

El logout no se borra: invalida el token. La clave del seed no se rota. La cookie `HttpOnly` espera. La migración es la `0008`, después de la `0007`.

## Resultado

Cerrar sesión y cambiar la clave dejan de servir los tokens ya emitidos.

## Criterios de aceptación

- El usuario tiene `tokens_valid_after`. `get_current_user` rechaza un JWT emitido antes.
- Logout y cambio de clave actualizan ese instante.
- Aunque el refresh se rote, hay un techo absoluto de una semana.
- El default del código y el ejemplo del `.env` dicen la misma duración de access token.
- El token sigue en `localStorage`.
- No se edita `LoginPage.tsx`. No se cambia la clave de `seed_user.py`.
- No se toca `0007_fecha_corte.py`.

## Pregunta

¿Cómo se corta una sesión copiada, si hoy el logout solo borra el token en el navegador?
