# Neon puede dormir

Type: task
Modo: AFK
Status: open
Blocked by: 06, 10, 20, 27
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/core/database.py`
- `backend/app/main.py`
- `backend/app/services/imap_watcher.py`
- `backend/app/core/config.py`

## Decisión cerrada

Neon tiene que poder dormir. El techo puede llegar a USD 15 solo si la medición de CU-h no entra. Julián anota esa medición en Leer el panel de Neon antes de escribir este arreglo. No se muda la base. No se cambia la región. `render.yaml` ya lo cerró Render no vuelve a free.

## Resultado

El pool suelta conexiones ociosas y `/health` no abre una sesión. El watcher no mantiene la base despierta si no hay envíos recientes.

## Criterios de aceptación

- Este ticket no se empieza si Leer el panel de Neon no tiene la nota de CU-h, región y host.
- `/health` responde sin abrir una sesión de negocio. El chequeo de base queda en otro endpoint o en un intervalo largo.
- El pool suelta ociosas (`pool_recycle` o `NullPool`, el que deje dormir a Neon). El comentario dice cómo se verifica en el gráfico de CU-h.
- `DATABASE_URL` de producción se documenta en un comentario del config: host directo, sin `-pooler`, porque el lock del watcher es de sesión. No se reescribe el valor en el panel.
- El watcher no pollea si no hay envíos recientes. Primero headers y tamaño, no el RFC822 entero, con un tope de 1–2 MB. El poll de 10 minutos se mantiene salvo que la nota de Julián diga que Free no entra ni así. Bajarlo a 30 minutos solo con esa nota, y la hora de última revisión sigue siendo un dato de la pantalla, no de este archivo.
- No se elige otro proveedor.

## Pregunta

¿Qué hay que cambiar en el proceso para que Neon Free pueda suspenderse, después de leer los CU-h?
