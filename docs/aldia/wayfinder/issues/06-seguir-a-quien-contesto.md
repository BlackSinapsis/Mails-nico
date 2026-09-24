# Seguir a quien contestó

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/services/imap_watcher.py`
- `backend/tests/test_imap_watcher.py`

## Decisión cerrada

Q21 no se reabre. El poll sigue en 10 minutos. También lee a quien ya contestó, por si después manda el comprobante. Bajar el ritmo a 30 minutos, o leer solo encabezados, espera la medición de Neon.

## Resultado

El poll automático y el refresco manual reclasifican `CONTESTADO` dentro de la ventana de 30 días, no solo `NO_CONTESTADO`.

## Criterios de aceptación

- Un contestado que después manda un PDF adjunto pasa a comprobante. Una firma inline no lo hace. Usa el clasificador ya cerrado por La firma no es un pago: si ese ticket todavía no mergeó, este test inyecta el resultado.
- No se cambia el intervalo de 10 minutos.
- No se reescribe la descarga del RFC822. Eso es Neon puede dormir, y espera la nota de CU-h.
- La hora «Última revisión» en la pantalla es de Listas honestas y marcar pago.

## Pregunta

¿Cómo entra un comprobante que llegó después del primer «contestó»?
