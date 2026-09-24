# Tabla densa de registros

Type: task
Modo: AFK
Status: open
Blocked by: 18, 19, 23, 20, 16
Fase: 2 · CRM
Tamaño: L
Archivos:
- `frontend/src/pages/SeguimientoPage.tsx`
- `frontend/src/components/seguimiento/TablaRegistros.tsx`
- `frontend/package.json`
- `frontend/package-lock.json`
- `backend/app/models/vista_guardada.py`
- `backend/app/models/__init__.py`
- `backend/alembic/versions/0011_vista_guardada.py`
- `backend/app/routers/seguimiento.py`
- `backend/app/schemas/seguimiento.py`
- `backend/tests/test_seguimiento_router.py`
- `frontend/src/types/domain.ts`

## Decisión cerrada

La capa 2 incluye la tabla densa de Twenty y Attio. No el kanban. `@tanstack/react-table` es MIT. 600 filas sin virtualizar alcanzan hasta que filtrar se mida lento. La migración es la `0011`, después de la `0010`.

## Resultado

Seguimiento se lee en una tabla densa: se ordena, se filtra, se guardan vistas y se actúa sobre varias filas. El saldo no cambia al cambiar de vista.

## Criterios de aceptación

- Header sticky, orden por columna, filtro, densidad cómoda y compacta. La fila abre el registro. El drawer lo termina Panel y línea de tiempo: esta tabla deja el enlace y no reescribe `EnvioDrawer.tsx`.
- Vistas con nombre: al menos Sin respuesta, Contestó, Comprobante, Rebotó, Sin email, Pausados. Cada una muestra su conteo. El operador puede guardar filtro, orden y columnas.
- Barra de selección: conteo, suma de montos que manda el servidor, y acciones de pausar o levantar pausa. `Esc` limpia la selección. Una acción masiva no modifica el saldo ni la racha.
- Carga, vacío y error siguen siendo los de Listas honestas y marcar pago.
- En 390 px se puede scrollear la tabla y abrir una fila.
- `package.json` espera a Sentry. `domain.ts` espera al dashboard.

## Pregunta

¿Cómo se trabaja la lista de consorcios con orden, filtro y vistas, sin convertirla en un kanban?
