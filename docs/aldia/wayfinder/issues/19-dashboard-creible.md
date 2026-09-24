# Dashboard creíble

Type: task
Modo: AFK
Status: open
Blocked by: 03, 16, 08, 18
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/services/dashboard_service.py`
- `backend/app/schemas/dashboard.py`
- `backend/app/routers/dashboard.py`
- `backend/tests/test_dashboard.py`
- `backend/tests/test_antiguedad.py`
- `frontend/src/pages/DashboardPage.tsx`
- `frontend/src/pages/ClientePerfilPage.tsx`
- `frontend/src/components/dashboard/EvolucionChart.tsx`
- `frontend/src/services/dashboard.ts`
- `frontend/src/types/domain.ts`

## Decisión cerrada

El dashboard se queda. Hoy va a convivir al lado, en otro ticket. Un comprobante no apaga la deuda. El click del consorcio abre `/clientes/{clave}`.

## Resultado

Las cifras se pueden explicar con el Excel del corte. La ficha no dice «Al día» si el corte tiene saldo.

## Criterios de aceptación

- Si el corte tiene saldo, la ficha no dice «Al día» y la columna no dice «Pagó». El comprobante no corta «deudor desde» ni la racha.
- La variación se abre en cuatro renglones (salió, bajó, subió, entró) que suman el saldo nuevo. Si el corte anterior estaba en cero, el texto lo dice. `cobrado` deja de viajar en el JSON.
- Un punto por corte, en `fecha_corte`, sin curva que invente meses, sin degradé, sin selector de año y sin animación de entrada.
- «Recordatorio» significa mails con `message_id`. «No se envió» trae el motivo.
- «Saldado histórico» pasa a «Saldo al salir de cartera».
- El título lleva la fecha del corte y aclara que el saldo incluye sin mail y filtrados.
- Hay una descarga del corte vigente con `openpyxl`.
- El nombre del consorcio es un enlace a `/clientes/{clave}`.
- `formatPesos` y `formatFecha`. TanStack Query. Carga, vacío y error.
- Recharts entra con `React.lazy` en esta ruta. El login no lo descarga.
- La pausa se ve en la ficha. El botón de pausar que ya esté en el maestro no se duplica editando `MaestroPage.tsx`.

## Pregunta

¿Qué números puede mirar el operador para cobrar, sin que un comprobante o un agregado mensual le mientan?
