# Render no vuelve a free

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `render.yaml`

## Decisión cerrada

El backend sigue en Render Starter. Un blueprint no puede volver el servicio al plan que bloquea el SMTP. El pool de Neon no se toca acá.

## Resultado

`render.yaml` dice `starter`, o no fija el plan. No dice `free`.

## Criterios de aceptación

- El único archivo escrito es `render.yaml`.
- No se cambia `DATABASE_URL`, el health ni el watcher.
- No se aplica el blueprint contra la cuenta de Juan. Eso lo mira él en el panel, y no lo aplica mientras el archivo diga `free`.

## Pregunta

¿Cómo se evita que el archivo del repo vuelva a pedir el plan que bloquea el puerto 587?
