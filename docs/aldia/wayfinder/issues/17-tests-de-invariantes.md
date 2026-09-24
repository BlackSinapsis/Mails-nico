# Tests de invariantes

Type: task
Modo: AFK
Status: open
Blocked by: 16
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/tests/test_invariantes_corte.py`
- `backend/tests/factories.py`

## Decisión cerrada

Cada regla del corte que el piloto puede romper tiene un test con el valor esperado escrito a mano. D-29. No se agrega `factory_boy` si las funciones de `factories.py` alcanzan.

## Resultado

Un archivo nuevo cubre las invariantes. No reescribe los servicios.

## Criterios de aceptación

- Un solo ciclo activo. Aceptar otro lo desactiva en la misma transacción.
- Un `FILTRADO` tiene motivo. Un `NO_CONTESTADO` no.
- La tabla de transiciones: a comprobante o rebote desde no contestado, y a comprobante desde contestado solo por el operador.
- Un comprobante no escribe `saldado_en`.
- Un Excel no vuelve `prefiere_no_recibir_email` a falso.
- La clave normalizada tiene 8 dígitos. El monto es `Decimal`.
- Excluir (mínimo, baja, pausa, sin email, no seleccionado) no cambia saldo ni racha.
- El preview no escribe.
- Los estados nuevos están en `domain.ts` porque los tickets anteriores ya los escribieron. Este ticket no edita `domain.ts`. Si falta uno, se anota en el test con el nombre del ticket dueño. No se abre una edición paralela.

## Pregunta

¿Qué tests demuestran que un corte no salda, no borra y no reclama de más?
