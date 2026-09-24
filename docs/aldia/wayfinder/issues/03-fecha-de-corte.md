# Fecha de corte

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/models/ciclo.py`
- `backend/alembic/versions/0007_fecha_corte.py`
- `backend/app/services/dashboard_service.py`
- `backend/app/schemas/ciclo.py`
- `backend/tests/test_dashboard.py`
- `backend/tests/test_antiguedad.py`

## Decisión cerrada

Q23 no se reabre. Cada corte tiene un día de datos, distinto de `creado_en`. Antigüedad, +90 y «deudor desde» usan ese día. La migración es la `0007`. Las siguientes migraciones esperan a que esta esté aplicada.

## Resultado

`fecha_corte` se guarda aparte de `creado_en`. El dashboard deja de tratar el instante de la carga como el día del Excel.

## Criterios de aceptación

- La columna entra nullable. El código nuevo la escribe. No se exige en el mismo release en que aparece.
- `batch_alter_table`. Un solo head. El `downgrade` está escrito o el PR dice por qué no.
- Evolución, +90 y deudor desde usan `fecha_corte` cuando existe. El rótulo de +90 es «saldo con continuidad mayor a 90 días». No se calcula DSO.
- El selector de fecha en la pantalla y la regla de «misma fecha y mismo archivo no crean dos ciclos» son de Preview de errores en pantalla y de Guardar el corte sin enviar. Este ticket no edita el router ni `NuevoEnvioPage`.
- SQLite de tests y PostgreSQL de producción aceptan la revisión.

## Pregunta

¿De qué fecha salen la antigüedad y la evolución: del día que dice el operador o del instante de la carga?
