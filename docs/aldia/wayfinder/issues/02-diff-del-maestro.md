# Diff del maestro

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/services/maestro_service.py`
- `backend/app/routers/maestro.py`
- `backend/app/schemas/maestro.py`
- `backend/tests/test_maestro.py`
- `frontend/src/pages/MaestroPage.tsx`
- `frontend/src/components/upload/MaestroUploadModal.tsx`
- `frontend/src/components/maestro/AgregarClienteModal.tsx`
- `frontend/src/services/maestro.ts`

## Decisión cerrada

Reimportar la lista de clientes muestra el diff y no escribe hasta que el operador aplica. Un mail vacío no pisa un mail cargado. Lo editado a mano se conserva. `prefiere_no_recibir_email` y `activo` no se modifican desde el archivo.

## Resultado

Subir el Excel maestro muestra altas, cambios, conflictos con lo editado a mano y mails que quedarían vacíos. Aplicar recalcula el diff en el servidor.

## Criterios de aceptación

- Hay un preview que no escribe.
- Si el operador editó el mail a mano, el default es conservar ese valor.
- Un mail con valor no pasa a vacío. El caso del E2E (reimportar sin columna email, o con la celda vacía) deja de borrar el correo.
- Pausa, baja, `activo` y `prefiere_no_recibir_email` no se modifican desde el archivo. Hay un test.
- Si el padrón cambió entre el preview y aplicar, el servidor pide revisar de nuevo.
- La página distingue carga, vacío y error. El «0 clientes» no aparece mientras `GET /maestro` no volvió. La lista usa TanStack Query.
- Los botones de icono tienen al menos 24 px y un nombre en castellano.
- No se agregan columnas de pausa. Eso es Pausar recordatorios.

## Pregunta

¿Cómo se evita que una reimportación del maestro borre un mail sin que el operador lo vea?
