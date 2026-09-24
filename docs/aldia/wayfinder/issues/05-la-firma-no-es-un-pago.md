# La firma no es un pago

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `backend/app/services/reply_classifier.py`
- `backend/tests/test_reply_classifier.py`

## Decisión cerrada

Una firma pegada en el HTML no es un comprobante. PAGO no escribe `saldado_en` ni cambia el saldo.

## Resultado

Solo cuenta un adjunto de verdad, y el remitente tiene que ser el mail del consorcio.

## Criterios de aceptación

- Se clasifica como comprobante una parte con `Content-Disposition: attachment` y tipo `application/pdf` o `image/*`. Lo `inline` se ignora.
- El From tiene que coincidir con el mail del envío antes de cambiar el estado.
- El cambio no escribe `saldado_en`.
- Hay un test: HTML con `image/png` inline sigue en `CONTESTADO`.
- La misma tabla de transiciones que usa el operador: a comprobante o rebote desde no contestado. El salto `CONTESTADO` → `PAGO` a mano no vive en este archivo.

## Pregunta

¿Qué respuesta puede marcar un comprobante sin que el logo de la firma alcance?
