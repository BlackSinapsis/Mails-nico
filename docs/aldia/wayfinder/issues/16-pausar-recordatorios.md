# Pausar recordatorios

Type: task
Modo: AFK
Status: open
Blocked by: 15, 02
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/models/cliente_maestro.py`
- `backend/alembic/versions/0010_pausa.py`
- `backend/app/services/maestro_service.py`
- `backend/app/routers/maestro.py`
- `backend/app/schemas/maestro.py`
- `backend/tests/test_maestro.py`
- `frontend/src/pages/MaestroPage.tsx`
- `frontend/src/components/maestro/AgregarClienteModal.tsx`
- `backend/app/services/smtp_sender.py`

## Decisión cerrada

Q16 no se reabre. La pausa es a mano, con motivo, sin tocar el saldo. No hay un objeto de promesa ni de tarea. La migración es la `0010`, después de la `0009`. `smtp_sender.py` entra acá porque Cancelar envíos obsoletos ya cerró.

## Resultado

El operador deja de mandarle mails a un consorcio, con motivo y una fecha de revisión opcional. La pausa sobrevive a las importaciones.

## Criterios de aceptación

- Existen `pausado_desde`, `pausa_motivo` y `pausa_revisar_el`.
- La fecha de revisión es opcional. Si no se carga, se propone el próximo corte, a 15 días.
- Al vencer, el cliente sigue excluido. Levantar la pausa es una acción explícita.
- El diff del maestro no pisa la pausa. El merge tampoco.
- Excluir por pausa no cambia saldo ni racha.
- La revalidación en `smtp_sender.py` mira la pausa antes de cada mail. Ese archivo ya lo cerró Cancelar envíos obsoletos, que este ticket espera.
- No se crea un módulo de notas.

## Pregunta

¿Cómo se frena el mail de un consorcio sin darlo de baja y sin alterar lo que debe?
