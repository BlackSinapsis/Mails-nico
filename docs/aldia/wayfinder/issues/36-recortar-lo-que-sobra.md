# Recortar lo que sobra

Type: task
Modo: AFK
Status: open
Blocked by: 20, 25, 23, 33
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `frontend/package.json`
- `frontend/package-lock.json`
- `backend/requirements.txt`
- `frontend/src/components/ui/collapsible.tsx`
- `frontend/src/components/ui/scroll-area.tsx`
- `frontend/src/hooks/useEnvios.ts`
- `backend/scripts/init_dev_db.py`
- `backend/runtime.txt`

## Decisión cerrada

Salen dependencias que nadie importa. No salen el logout, el punto de estado, ni `date-fns`. `react-hook-form` se queda: el login ya lo usa. Zod se queda. `cmdk` y TanStack Table se quedan. `POST /ciclos/desde-api` (501) se queda. No se implementa.

## Resultado

El árbol queda sin paquetes que ningún import use, después de que la capa 2 ya sumó los suyos.

## Criterios de aceptación

- Se sacan, si siguen sin imports: `qrcode.react`, `pytest-asyncio`, el extra `anyio[trio]`, Collapsible, ScrollArea, `useEnvios` si sigue sin uso, `init_dev_db.py`, `runtime.txt`, el README de plantilla de Vite y los SVG de scaffold.
- No se borra el endpoint de logout. No se borra `ESTADO_DOT`. No se reemplaza `date-fns`.
- No se unifican tablas de Nuevo envío.
- Pytest y el build siguen verdes.
- `package.json` y `requirements.txt` esperan a Sentry, a la tabla y al menú de comandos.

## Pregunta

¿Qué se puede borrar, una vez que la paleta y la tabla ya están, sin llevarse una regla del piloto?
