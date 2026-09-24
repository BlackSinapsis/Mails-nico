# Listas honestas y marcar pago

Type: task
Modo: AFK
Status: open
Blocked by: 15, 16, 09
Fase: 1 · Integridad
Tamaño: L
Archivos:
- `frontend/src/pages/SeguimientoPage.tsx`
- `frontend/src/components/envios/EnvioDrawer.tsx`
- `frontend/src/components/envios/EnvioCard.tsx`
- `frontend/src/pages/ConfiguracionPage.tsx`
- `frontend/src/services/seguimiento.ts`
- `frontend/src/services/envios.ts`
- `frontend/src/lib/estado.ts`
- `backend/app/routers/seguimiento.py`
- `backend/app/schemas/seguimiento.py`
- `backend/tests/test_seguimiento_router.py`
- `frontend/src/types/domain.ts`

## Decisión cerrada

Un error de red no se ve como «Sin registros». «Marcar como pago» pide confirmación con el nombre y el efecto. No hay toast de deshacer. El drawer dice el corte, no la racha. Q17: la selección de la campaña ya está en Guardar el corte sin enviar. Acá la lista dice el motivo de cada excluido.

## Resultado

Seguimiento y configuración distinguen carga, vacío y error. Buscar por nombre, clave o mail filtra la lista ya cargada. La confirmación de comprobante a mano es un diálogo.

## Criterios de aceptación

- Mientras carga, hay skeleton. Si la API falla, hay una frase y «Reintentar». El cero aparece solo cuando de verdad no hay filas. TanStack Query. El error no se traga en un `catch` vacío.
- «No se envió» incluye el motivo. Eliminado del padrón y dado de baja por el link son dos frases. Pausa, monto mínimo, sin email y no seleccionado también.
- El drawer dice el número de corte y la fecha, no `ciclo_numero`.
- Se muestra «Última revisión hh:mm» aunque no haya nada nuevo.
- El diálogo de «Marcar como pago» nombra al consorcio y dice que el estado pasa a comprobante marcado a mano, y que no acredita el saldo. Confirmar espera al servidor. Si falla, el estado no cambia. No se usa un deshacer.
- El servidor solo acepta `CONTESTADO` → `PAGO`.
- Hay un campo que filtra la lista ya cargada, sin animar las filas.
- En 390 px se puede abrir una ficha y leer el estado. El punto más el texto salen de `estado.ts`.
- Montos con `formatPesos`.

## Pregunta

¿Cómo se evita que un error de red, un motivo escondido o un clic en «marcar como pago» dejen el saldo mentido?
