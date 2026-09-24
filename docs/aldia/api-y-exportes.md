# Qué pedirle al programa de facturación

Esto son ideas para una segunda versión. El lunes el cobro sigue entrando por Excel.

Mails-nico no factura y no reemplaza ese programa.

Las preguntas para el dueño están en [preguntas-dueno.md](preguntas-dueno.md). De ahí salen tres datos que necesitamos para todo lo de abajo: el nombre del programa, si cada fila es un saldo o una factura, y si existe una conexión.

## El lunes

Siguen los dos archivos de siempre:

- **Deudores**, cada unos 15 días: `nro cliente`, `nombre`, `localidad`, `monto`. Es el archivo que abre el corte.
- **Lista de clientes**, cuando cambia un mail: el mismo número de cliente, el nombre y el correo. El mail sale de acá.

`POST /ciclos/desde-api` sigue respondiendo que no está hecho. Para ese día no se le pide ninguna conexión al programa de facturación.

## Qué vale la pena pedir después

Solo si el dueño confirma el nombre del programa y que puede exportar, o que ya tiene una conexión. El pedido va en este orden:

1. **Saldo abierto por cliente, con la fecha del corte.** El número de cliente va como texto, con los ceros de adelante, y trae nombre, localidad y monto. Es la misma lista que el Excel del lunes. Entraría por la puerta que ya está reservada, con la misma forma que el envío que hoy arma el cruce: número, nombre, lugar, monto, y el mail si ese programa lo tiene. La racha de ciclos la sigue calculando Mails-nico.
2. **La carga queda en un corte para revisar.** Mandar los mails sigue siendo otro clic del operario. La nota original de esa puerta decía que corriera el mismo camino que confirmar el ciclo, y hoy ese camino también manda. En la segunda versión, la conexión llena el corte y el que aprieta «enviar» sigue siendo una persona.
3. **El monto mínimo y qué texto usar**, solo si el programa de facturación ya los conoce. Son opcionales: el piso y la plantilla pueden seguir acá.
4. **Facturas abiertas**, si cada fila es una factura o si el abono y el trabajo extra tienen que verse por separado: número de factura, cliente, tipo (abono o extra), emisión, vencimiento y saldo.
5. **Pagos**, con fecha, cliente, factura si la hay, e importe. Con esto, «pagó» pasa a ser plata registrada. Deja de depender de «desapareció del Excel» o de «mandó un adjunto».
6. **Estado del contrato**: activo, de baja o en pausa. Así un edificio que ya no es cliente se filtra sin esperar a que toque el link de baja.
7. **A quién se le escribe**, si quiere mandarles a los dos: administración y consorcio, cada uno con su mail. La lista de clientes sigue teniendo el mail que ya tenemos; este dato agrega el segundo.
8. **Fecha de vencimiento** en el listado de deudores, si no pueden pasar el archivo de facturas. Con eso, «debe hace X» usa el vencimiento real.

Si el mismo número aparece varias veces, se le muestra al operario. Se suma por cliente recién cuando él diga que cada fila es una factura. Hasta esa respuesta, no se aplasta solo.

## Archivos que alimentarían el cobro

Sirven igual aunque no haya conexión: Excel o CSV, siempre con el mismo número de cliente.

| Archivo | Qué trae | Para qué sirve |
| --- | --- | --- |
| Deudores | el saldo del corte | el mail del lunes |
| Lista de clientes | nombre y mail | saber a quién se le escribe |
| Facturas abiertas | abono o extra, vencimiento, saldo | separar los dos cobros y ver la antigüedad real |
| Pagos | fecha e importe | decir que pagó cuando entró la plata |
| Estado del contrato | activo, de baja, en pausa | no escribirle a quien ya no es cliente |

El archivo de deudores sigue siendo el que abre el corte. Los otros corrigen cómo lo leemos. Ninguno es requisito para el lunes.

## Qué queda afuera

- Facturar, numerar comprobantes y hacer asientos. Eso vive en el programa de él.
- Código de Twenty. De ese producto miramos ideas, nada más: su licencia AGPL no entra en esta app.
- Un portal para que el consorcio pague, un aviso de si abrió el mail, un pronóstico de cobro y un informe armado por una máquina.
- Un archivo o una conexión que dispare los mails sin que alguien los confirme.
- Tomar el comprobante adjunto como si fuera plata acreditada.
- Encargar una conexión a medida antes de saber cómo se llama el programa y qué listas ya exporta.
