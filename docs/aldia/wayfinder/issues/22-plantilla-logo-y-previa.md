# Plantilla, logo y previa

Type: task
Modo: AFK
Status: open
Blocked by: 04, 23
Fase: 2 · CRM
Tamaño: M
Archivos:
- `frontend/src/pages/PlantillaPage.tsx`
- `frontend/src/services/plantilla.ts`
- `backend/app/routers/plantilla.py`
- `backend/app/services/db_config.py`
- `backend/app/models/plantilla.py`
- `backend/app/schemas/plantilla.py`
- `backend/tests/test_plantilla.py`
- `backend/tests/test_plantilla_logo_upload.py`

## Decisión cerrada

La pantalla de la plantilla entra en la capa 2. El HTML que se previsualiza es el que ya escapa Escapar el HTML del mail. Subir el logo no se lleva lo que el operador escribió y todavía no guardó.

## Resultado

Al editar asunto, cuerpo, color y logo se ve el mail como lo va a ver el consorcio. El formulario no se pisa al subir el archivo.

## Criterios de aceptación

- La previa usa asunto, cuerpo, color y logo actuales, con un consorcio de ejemplo. Iframe con sandbox, sin scripts. Sin `react-email`.
- Se actualiza al escribir, con un debounce corto, sin animar el documento.
- El upload del logo conserva asunto y monto mínimo todavía no guardados.
- Montos de ejemplo con `formatPesos`. Textos en voseo.
- La pantalla se lee en 390 px. El oscuro del shell se respeta. No se edita `index.css`.
- El tope de 2 MB del logo se mantiene.

## Pregunta

¿Cómo ve el operador el mail mientras lo edita, sin perder lo que todavía no guardó?
