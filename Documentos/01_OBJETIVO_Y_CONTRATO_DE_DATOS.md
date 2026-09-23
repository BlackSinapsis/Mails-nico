# Objetivo y contrato de datos

Fecha: 13/09/2026. Las afirmaciones “confirmado” provienen del usuario; las demás son propuestas para validar antes de implementarlas.

## Objetivo confirmado

Una persona importa periódicamente, aproximadamente cada 15 días, un Excel exportado de su sistema de facturación con **todos los deudores**. El sistema mantiene un maestro de clientes, conserva el historial por cliente y permite enviar recordatorios y gestionar respuestas. Cuando un cliente desaparece del siguiente listado completo, el negocio interpreta que pagó o regularizó su deuda.

Debe seguir siendo fácil de operar, con buena UI y funciones útiles de CRM, evitando complejidad innecesaria. La evaluación y las propuestas deben quedar documentadas antes de crear tickets y migrar.

## Dos conjuntos lógicos, no necesariamente dos bases físicas

| Conjunto | Responsabilidad | Regla |
|---|---|---|
| Maestro de clientes | Identidad, nombre, contactos, administradora, estado comercial y preferencias de comunicación | Un cliente continúa existiendo aunque deje de deber |
| Cortes de deuda | Quién debe y cuánto según facturación en una fecha | Cada corte aceptado conserva su contenido y procedencia |
| Actividad de cobranza | Campañas, mensajes, respuestas, notas, promesas y revisión de comprobantes | Se vincula al cliente y al corte; no reemplaza los saldos importados |

Para el tamaño actual es suficiente una base relacional con tablas relacionadas. Separar “clientes” y “deudores” no obliga a operar dos servidores de base de datos.

## Fuentes de verdad

- **Saldo informado y salida de la lista:** Excel completo de facturación aceptado para un ámbito y fecha.
- **Dirección de contacto:** maestro, con procedencia de cambios y posibilidad de corrección manual.
- **Un correo enviado o recibido:** registro del motor de correo/proveedor.
- **Una promesa:** gestión registrada por la persona, con fecha e importe.
- **Un comprobante:** documento recibido, pendiente de interpretación. No puede borrar una deuda del corte.

No se exige incorporar conciliación bancaria para cumplir el objetivo inicial. El sistema puede cerrar un episodio mediante la regla de ausencia confirmada por el usuario, mostrando “Regularizado según el corte del 16/09”. Una conciliación explícita sería una capacidad posterior si se dispone de esos datos.

## Contrato propuesto del Excel

1. Una fila por cliente con el saldo total positivo al corte. Si el export real contiene una fila por factura, se necesita un contrato distinto: conservar documentos y agrupar explícitamente por cliente. No sumar duplicados a ciegas.
2. Clave de cliente estable del sistema de facturación, tratada como identificador. Normalización acordada: espacios, ceros a la izquierda y claves numéricas. Nunca unir únicamente por nombre o email.
3. Moneda y ámbito uniformes en el archivo. Inicialmente una empresa/cartera y ARS; estos dos supuestos requieren confirmación con el export real.
4. Fecha de corte explícita. Guardar además fecha/hora de carga, usuario, archivo original, hoja seleccionada, huella del archivo y versión de lectura.
5. Totales de control: filas leídas, vacías, válidas, rechazadas, duplicadas; clientes únicos y suma de saldo. Contrastar con el total que muestre el sistema de facturación, si existe.
6. Ninguna fila con identidad o monto inválido puede desaparecer silenciosamente de un corte considerado completo. Bloquear su aceptación hasta resolverla; permitir guardar el borrador y descargar errores.
7. El archivo íntegro se valida y publica de forma atómica: el dashboard ve el corte anterior o el nuevo, nunca una mezcla de filas de ambos.
8. Una importación sin deudores puede ser legítima. Distinguir “cero deudores declarado” de un archivo corrupto, una hoja equivocada o un parseo que rechazó todas las filas.

## Fechas y cobertura

| Concepto | Ejemplo | Uso |
|---|---|---|
| Fecha del corte | 01/09 | Momento al que corresponde el saldo |
| Carga aceptada | 04/09 a las 10:15 | Auditoría de la operación |
| Fecha de observación de regularización | 16/09 | Primer corte válido donde ya no aparece |
| Fecha exacta del pago | Desconocida en un listado de saldos | No inferir “pagó el día de la carga” |
| Última revisión del correo | 18/09 a las 09:00 | Frescura de la comunicación, independiente del saldo |

“Cada 15 días” describe la rutina, no permite inventar cortes faltantes. Si se carga el 01/09 y luego el 01/10, hubo dos observaciones separadas por 30 días. Los días intermedios no son deuda cero ni una observación adicional. Una alerta de próxima carga se calcula desde la última fecha de corte aceptada, con tolerancia configurable.

## Ausencia válida y ausencia ambigua

**Regla confirmada:** si el cliente estaba en el corte A y no aparece en B, siendo B completo, posterior, aceptado y del mismo ámbito, se cierra el episodio como regularizado según facturación.

**Protección propuesta:** un archivo parcial, pendiente, rechazado o de otro ámbito no produce ese cierre. La primera versión puede admitir únicamente cortes completos; no hace falta construir un sistema complejo de cargas parciales para protegerse de ellas.

La ausencia se interpreta solo dentro de una cobertura conocida. No corresponde declarar que un cliente recién incorporado al maestro estuvo siempre al día antes del primer período conocido.

## Operaciones diferentes con una UI simple

“Guardar corte” y “Enviar recordatorios” deben ser operaciones independientes. La interfaz puede ofrecer una continuación directa “Guardar y preparar mails”, pero debe permitir actualizar el historial aunque se decida no enviar o no haya destinatarios válidos. Un fallo de Gmail no invalida el Excel aceptado.

## Aspectos que todavía requieren el export real

- Si el saldo incluye vencidos, no vencidos, intereses, notas de crédito o varias monedas.
- Si la clave es única para toda la empresa y puede ser reutilizada.
- Si existen fecha de emisión/vencimiento y movimientos de pago exportables.
- Si “sin deudores” genera un archivo con encabezados, un reporte especial o ningún archivo.
- Qué campos del maestro se consideran obligatorios y cómo prevalecen correcciones manuales frente a una recarga.

Estas preguntas afectan al contrato de datos; no bloquean las conclusiones de la auditoría actual.
