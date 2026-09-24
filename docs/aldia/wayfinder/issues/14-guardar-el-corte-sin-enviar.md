# Guardar el corte sin enviar

Type: task
Modo: AFK
Status: open
Blocked by: 12, 13, 10
Fase: 1 · Integridad
Tamaño: L
Archivos:
- `backend/app/services/ciclo_service.py`
- `backend/app/routers/ciclos.py`
- `backend/app/services/smtp_sender.py`
- `backend/app/models/envio.py`
- `backend/app/schemas/envio.py`
- `backend/alembic/versions/0009_no_seleccionado.py`
- `backend/tests/test_ciclos.py`
- `backend/tests/test_smtp_sender.py`
- `frontend/src/pages/NuevoEnvioPage.tsx`
- `frontend/src/types/domain.ts`
- `frontend/src/components/upload/ProgresoEnvio.tsx`
- `frontend/src/hooks/useCiclo.ts`
- `frontend/src/contexts/CicloContext.tsx`
- `frontend/src/services/ciclos.ts`

## Decisión cerrada

Guardar y enviar son dos actos. La confirmación de envío es manual. El tope es 150 mails por envío, por Yahoo. El rate limit sigue en 5 cada 30 segundos. La misma fecha y el mismo archivo no crean dos ciclos. Desde el teléfono también se puede mandar el lote. La escritura del corte sale del router y hace un solo commit. La migración es la `0009`, después de la `0008`.

## Resultado

«Guardar corte» actualiza historial y dashboard y no manda mails. «Enviar recordatorios» es otra acción, sobre las filas que el operador eligió, como máximo 150.

## Criterios de aceptación

- Los botones se llaman «Guardar corte» y «Enviar recordatorios».
- Guardar hace un solo commit en el servicio. El router no arma el corte ni hace `commit`. Si falla, el corte anterior sigue vigente.
- El dashboard del corte nuevo se puede abrir sin haber mandado un mail.
- Checkbox por fila. Los no elegidos quedan `NO_SELECCIONADO`, fuera de «Reenviar todos», y no se ven como fallo. Excluir no cambia saldo ni racha.
- El servidor rechaza un envío de más de 150. El proveedor de ese tope es Yahoo.
- El segundo clic no crea otro ciclo. El botón se deshabilita al enviarlo y el servidor igual rechaza el duplicado.
- Cerrar el navegador no corta un envío ya empezado. La barra se reconstruye desde filas persistidas.
- En 390 px de ancho se puede guardar y se puede confirmar el envío. Escritorio primero.
- El ritmo de 5 cada 30 segundos no se saltea. Los tests de envío inyectan el transporte.
- `test_dedupe_deudores_conserva_la_ultima_fila` ya lo habrá cambiado Filas, clave repetida y tope del Excel. No lo vuelvas a la última fila.

## Pregunta

¿Cómo se separa «entró la deuda» de «se mandó el mail», con un tope de 150 y la confirmación a mano?
