# Sistema de movimiento

Type: task
Modo: AFK
Status: open
Blocked by: 23
Fase: 2 · CRM
Tamaño: M
Archivos:
- `frontend/src/index.css`

## Decisión cerrada

El movimiento es corto, con ease-out, y quieto si el sistema pide menos movimiento. No hay Framer Motion. No se animan las filas, el cambio de ruta ni la paleta.

## Resultado

Paneles, diálogos y botones de acción usan dos duraciones y una curva, definidas en CSS.

## Criterios de aceptación

- `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`. Duraciones 150 ms y 200 ms.
- El diálogo, con `prefers-reduced-motion`, pasa a opacidad o a estático. Sin zoom.
- El botón de acción puede usar `scale(0.98)` en cerca de 120 ms. No las filas ni el sidebar.
- No hay entrada escalonada de filas, ni ticker de números, ni dibujo del gráfico al entrar.
- La barra de progreso conserva el ancho a 300 ms y `motion-reduce: transition none`.
- No se agrega la librería `motion`. Si una interacción de esta lista no entra en CSS, se justifica en el PR. Ninguna de las de arriba lo necesita.
- No se editan las páginas. El panel que usa estas clases es Panel y línea de tiempo.

## Pregunta

¿Qué CSS alcanza para que los diálogos y los botones se muevan igual, y el resto quede quieto?
