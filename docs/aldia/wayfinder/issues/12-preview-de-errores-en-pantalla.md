# Preview de errores en pantalla

Type: task
Modo: AFK
Status: open
Blocked by: 01, 03, 08
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/routers/ciclos.py`
- `backend/app/services/ciclo_service.py`
- `backend/app/schemas/ciclo.py`
- `backend/tests/test_preview_errores.py`
- `frontend/src/pages/NuevoEnvioPage.tsx`
- `frontend/src/components/upload/ExcelUploadModal.tsx`
- `frontend/src/components/upload/FileDropzone.tsx`
- `frontend/src/services/ciclos.ts`
- `frontend/src/types/domain.ts`
- `frontend/src/hooks/useCiclo.ts`
- `frontend/src/contexts/CicloContext.tsx`
- `frontend/src/contexts/ciclo-context-object.ts`
- `frontend/src/contexts/useCicloContext.ts`

## Decisión cerrada

Q15 no se reabre. El operador ve fila, columna, valor y motivo, y puede descargarlos. Un archivo sin deudores no ofrece «Enviar 0 mails» en silencio. La fecha de corte es obligatoria en esta pantalla. El preview no escribe.

## Resultado

Subir el Excel de deudores muestra los errores y no deja guardar si hay clave inválida, monto ilegible o clave repetida. La fecha propone hoy en Argentina y se puede editar.

## Criterios de aceptación

- El cuerpo de error es JSON con `errores[]`. Sin el sobre completo de RFC 9457. El `type` queda estable.
- Si falta una columna, el mensaje nombra «número de cliente» (o la columna que falte) y lista los encabezados.
- Un archivo sin filas de deuda exige una confirmación distinta, con el texto «Cartera sin deuda. Guardar igual». No queda habilitado un envío de cero mails.
- El preview dice «Datos al dd/mm, cargado hoy», con `formatFecha`. Los montos usan `formatPesos`.
- Avisa si pasaron más de 15 días desde el último corte.
- En el flujo normal no se acepta una fecha menor o igual a la del corte vigente. Esa regla, al guardar, la cierra Guardar el corte sin enviar. Acá la pantalla ya la muestra.
- La frase fija arriba del primer preview: «Este archivo tiene que ser la cartera completa. Quien no esté va a figurar como regularizado.»
- Soltar el archivo también se puede con un botón de elegir archivo.
- `domain.ts` lo escribe este ticket. Los siguientes que lo necesiten esperan.

## Pregunta

¿Cómo ve el operador la fila que no se puede importar, y cómo elige el día del corte, sin que el preview escriba en la base?
