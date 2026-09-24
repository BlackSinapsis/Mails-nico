# Pesos y fechas de Argentina

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `frontend/src/lib/formato.ts`
- `frontend/src/lib/formato.test.ts`

## Decisión cerrada

Hay una sola función de pesos y las fechas de corte se muestran en hora de Argentina. No se agrega una librería de i18n. Sigue `date-fns`.

## Resultado

`formatPesos` y `formatFecha` viven en `frontend/src/lib/formato.ts`. Las pantallas las importan cuando les toca el archivo. Este ticket no edita páginas.

## Criterios de aceptación

- `formatPesos` usa `es-AR`, ARS, siempre dos decimales. `5000.50` se ve como moneda con `,50`, no como `5.000,5`.
- `formatFecha` formatea un día de calendario en `America/Argentina/Buenos_Aires`, `dd/MM/yyyy`. Un instante acepta `HH:mm`.
- El test cubre los dos. No se suma Vitest al `package.json` si eso obliga a tocar el lock: el test puede ser un assert mínimo que el ticket de etiquetas no pisa. Si hace falta el script `test`, se anota y se deja el lock para Etiquetas, foco y estado visible, que es el dueño de `package.json` en la frontera.
- Quien edite una pantalla después importa estas funciones y no copia otra.

## Pregunta

¿Dónde vive el formato de un monto y de un día de corte para que todas las pantallas usen el mismo?
