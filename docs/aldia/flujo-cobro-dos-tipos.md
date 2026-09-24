# Flujo de cobro: el lunes y lo que viene después

Fecha: 2026-09-24. Este documento no toca código.

Julián corrigió el alcance, así que arranco por ahí: el lunes se usa el sistema que ya está en producción. Tres cosas quedan para después del MVP:

- cobrar el abono y los trabajos extra por separado,
- tratar varias facturas como deudas distintas,
- la API.

El manual o el video corto para el cliente también queda para después. Esto no es ese manual.

## Qué se usa el lunes

El 2026-09-28 el MVP es la integridad del ciclo que la app ya corre en producción. El ciclo es así:

1. El dueño exporta la lista completa de clientes desde su programa de facturación y la importa una vez. La vuelve a importar solo cuando cambian mails o nombres.
2. Cada unos 15 días exporta quién le debe y lo sube como archivo de deudores.
3. Hay un monto por cliente y un mail por cliente.

Todo eso ya está en el código:

- `ClienteMaestro` guarda la clave, el nombre y el mail.
- `Ciclo` es cada archivo confirmado.
- `Envio` es un registro por `clave_union` dentro de ese ciclo. Tiene un `monto`, un estado de mail y, si la clave no aparece en el archivo siguiente, `saldado_en`.
- La plantilla imprime un solo `{{monto}}`.
- `POST /ciclos/confirmar` crea el ciclo y manda los mails.
- El preview no escribe nada.
- El rate limit sigue en 5 mails cada 30 segundos. Medimos 600 mails: tardaron 84 min 59 s.

`dedupe_deudores` también es parte de este modelo. Si la misma clave aparece dos veces, gana la última fila (monto, nombre y localidad). Lo fija el test `test_dedupe_deudores_conserva_la_ultima_fila`. `NuevoEnvioPage` avisa «se usó la última de cada una», pero deja el botón de envío habilitado.

`marcar_saldados` y `_cobrado_entre` comparan un monto por clave entre un ciclo y el siguiente. Si el monto baja, cuenta como cobro parcial. La racha (`ciclo_numero`) también es de la clave, no de un concepto.

El spec de cobranza del 2026-07-06 ya hablaba de «abono mensual más servicios adicionales», y lo guardó como un solo saldo. En el negocio del cliente, el abono se cobra más o menos del 1 al 5, y los trabajos (un tablero, un cambio de aceite) son importes aparte.

El lunes nada de eso cambia. El programa de facturación sigue entregando un solo saldo por consorcio y la app sigue pidiendo ese saldo. El ritmo del 1 al 5 lo maneja él, eligiendo cuándo confirma el envío. En este corte la app no aprende dos calendarios.

El pulido chico del login va después, cuando esta lógica ya esté segura. Hoy, cmdk, la tabla densa y el motion no entran el lunes.

## Robustecer: corregir los errores del mismo ciclo

Robustecer quiere decir corregir los errores de este ciclo. El grano no cambia: un monto y un mail. Todo lo que sigue son fallas del código de hoy, con un archivo de un saldo por cliente.

### Una fila que el parser tira se lee como pago

`parse_deudores` salta la fila si falta la clave, el nombre o el monto, si el monto no entra en `Decimal`, o si es ≤ 0. Después, `confirmar_ciclo` arma el conjunto de `marcar_saldados` solo con las filas que sobrevivieron.

¿Qué pasa entonces? Alguien que debía en el ciclo anterior y cuya fila se perdió recibe `saldado_en`, y el dashboard le baja la deuda.

Hay más casos parecidos:

- `str(clave).strip()` no rellena ceros. Una celda numérica `42` o `42.0` no cruza con el maestro `00000042`. Va a `SIN_EMAIL` con otra clave, y el envío de `00000042` queda saldado.
- El texto `150.000,50` se salta igual. Lo vimos en el E2E.
- Un archivo con solo encabezados parsea vacío. El botón dice «Enviar 0 mails» y, si confirmás, la cartera queda en cero.

### Volver a importar la lista de clientes puede vaciar los mails

`merge_maestro` hace upsert y no desactiva a quien ya no viene. Si la columna de mail no está en `MAESTRO_ALIASES` (`email`, `mail`, `correo`, `e-mail`) o la celda viene vacía, el mail guardado pasa a `None`. La única excepción es cuando `prefiere_no_recibir_email` ya es verdadero.

El archivo de cada 15 días no trae mail: el mail solo cambia con la lista de clientes. Y cuando hay match, el nombre del archivo de deudores no pisa al del maestro (`join_deudores` usa `cliente.nombre`).

### Confirmar y mandar son el mismo clic, y la cola anterior no se entera

Entre el 1 y el 5, él puede querer cargar el saldo nuevo y mandar los mails después del día 5. Hoy no puede: `confirmar_ciclo` escribe el ciclo y llama a `enviar_ciclo` de una. Además no mira `ids_en_proceso`.

Resultado: si sube un segundo archivo el mismo día, se marca `saldado_en` y los mails del ciclo viejo siguen saliendo igual. En el E2E quedaron saldados a las 22:02:30 y se enviaron a las 22:02:56.

Dos detalles más:

- `POST /envios/{id}/reenviar` no exige que el ciclo siga activo.
- Mientras se envía, la pantalla sigue mostrando el corte anterior hasta el `done` del SSE.

### Un adjunto cierra el saldo entero de esa clave

`reply_classifier` trata como `PAGO` cualquier `image/*`, `application/pdf` o parte con `attachment`. Una firma con imagen alcanza.

Cuando eso pasa, `_ciclos_consecutivos_deudor` corta la racha. La ficha queda «al día» (`deudor_desde` vacío), mientras `resumen` sigue sumando el monto del ciclo activo.

`_poll_inbox` solo reclasifica `NO_CONTESTADO`. Si alguien contesta con texto y después manda el comprobante, ese comprobante no se lee.

Y la baja: el GET `/unsubscribe/{token}` la aplica apenas algo abre el link. El merge no la revive.

### El HTML del nombre no está escapado

`_render_cuerpo` pega el nombre sobre la plantilla con `autoescape=False`, y `mail_cobro.html` marca el cuerpo como `safe`.

### Lo que tiene que estar antes de un mail real del lunes

Todo sobre este mismo modelo:

- Las filas ilegibles bloquean el corte y no entran al conjunto que salda.
- La clave numérica se normaliza a 8 dígitos.
- El monto argentino se lee bien.
- Un archivo sin deudores pide una confirmación distinta de «Enviar 0 mails».
- La lista de clientes muestra el diff y un vacío no pisa un mail cargado.
- Cargar el corte y mandar son dos actos separados.
- Un corte nuevo frena lo que todavía no salió.
- La firma no es un pago.
- El nombre va escapado.
- La baja no ocurre en el GET.

El primer envío real sigue siendo un lote chico. La cola de 600 tarda del orden de 85 minutos, y un `SIGKILL` no la retoma.

## Una excepción que se nombra, pero no se construye

Puede pasar que el export de deudores traiga una fila por factura y no un saldo por cliente. En ese caso, sumar esas filas en el único `monto` es un arreglo chico del modelo de hoy. Separar el abono de los trabajos extra no es ese arreglo.

El cambio chico vive en `dedupe_deudores`. En vez de quedarse con la última fila, suma los montos de la misma clave y deja un solo `DeudorRow`. El preview muestra las partes y el total. Sigue habiendo un `Envio`, un mail, un `marcar_saldados` por clave y un KPI. No hace falta tabla nueva.

No se construye para el lunes. Se construye solo si, al ver el archivo real, las filas repetidas son facturas del mismo saldo y no un error del export.

Hoy, sin ese archivo, la última fila pisa y el aviso no frena el envío. Un ejemplo: dos filas de $45.000 y $8.000 salen como un mail de $8.000, con `duplicados = 1`. Y si una de las dos ni siquiera parsea (monto en texto, monto ≤ 0), `duplicados` queda en 0 y el otro importe desaparece antes del dedupe.

Eso es justo lo que la suma evitaría. También es lo que ya cubre el bloqueo de filas ilegibles, para el caso de la fila rota. La suma no se adelanta.

## Después del MVP: el rediseño

Cuando haga falta cobrar el abono y los trabajos como deudas distintas, o cuando el programa de facturación mande una API u otras exportaciones, el grano deja de ser `Envio.monto`.

Ese rediseño incluye:

- un concepto con su propio vencimiento (el abono cierra alrededor del día 5; un tablero o un cambio de aceite, no),
- saldar una factura y seguir reclamando la otra,
- una racha por deuda,
- un mail que liste las partidas.

Con la API hay un riesgo. `POST /ciclos/desde-api` hoy responde 501 y tiene la forma de un `EnvioParsed`: una clave y un monto. Ese es el contrato del mail de hoy. Si lo implementamos así y después partimos los conceptos, hay que tirar esa integración.

### Cuánto trabajo es

El arreglo de la suma, si alguna vez hace falta, es local: parser, preview y el test del dedupe.

El rediseño, en cambio, cruza todo lo que lee el saldo. Hay que tocar:

- `excel_parser`, `excel_joiner` y `marcar_saldados`,
- `dashboard_service` (`resumen`, `_cobrado_entre`, `deudor_desde_por_clave`, `morosos`),
- la ficha del cliente y seguimiento,
- `email_generator` y la plantilla.

La racha deja de ser un entero en `Envio.ciclo_numero` calculado con el último envío de esa clave.

Los envíos viejos no se pueden partir: un histórico de un monto no dice cuánto era abono y cuánto era aceite. Las partidas nuevas empiezan el día del cambio. Lo anterior queda como campaña de un saldo.

El envío en sí no se reescribe. SMTP, el rate limit, el `message_id` y el watcher sirven mientras siga habiendo un mail por cliente y por ciclo.

### Cómo crecerían las tablas

**`clientes_maestro` sigue siendo la persona**: clave, nombre, mail, localidad, `prefiere_no_recibir_email`, `activo`. El tipo de cargo no va ahí. La baja del link sigue siendo del consorcio entero.

**`ciclos` sigue siendo el corte**: el archivo de una quincena (o, más adelante, la carga por API) y la campaña de mails de ese corte.

**Hace falta una tabla nueva de partidas abiertas**, hija del cliente y no del envío. Por ejemplo `partidas`, con: `clave_union`, tipo (`abono` o `trabajo`), concepto, número de comprobante del programa de facturación, monto, saldo, vencimiento, estado y `saldada_en`.

- La identidad de la partida es el comprobante, no la clave.
- Cada 15 días el archivo (o la API) hace upsert de partidas y marca saldada la que ya no viene.
- `saldado_en` en `envios` se queda para leer los ciclos viejos. En los ciclos nuevos el saldo vive en la partida.

El riesgo de la migración es tener las dos cosas como verdad al mismo tiempo. Apenas exista la partida, hay que dejar de escribir `Envio.saldado_en` como sustituto del saldo.

**`envios` sigue siendo el mail**: uno por cliente y por ciclo, con `message_id`, estado de respuesta y el `monto` igual a la suma que se pidió.

Al lado va una tabla chica, `envio_partidas` (`envio_id`, `partida_id`, monto incluido), que dice qué deudas entraron en ese sobre. Sin eso, un `PAGO` del watcher sigue cerrando al cliente entero, que es lo que hoy hace `classify` sobre un solo envío.

Agregar un `tipo` a `envios` no alcanza. Una fila no puede tener dos vencimientos ni dos saldos, y el dedupe volvería a tirar una de las dos.

### Partida, envío y ciclo

La deuda y el mail son cosas distintas:

- la **partida** es lo que debe,
- el **envío** es lo que se le escribió, con su `message_id`,
- el **ciclo** es el momento en que se miró la cartera y se armó la campaña.

Sumar facturas dentro de `dedupe_deudores` aplasta las partidas antes de guardarlas. Sirve como puente si el archivo trae varias filas y el producto sigue pidiendo un solo número. No sirve como modelo del abono y del trabajo.

El watcher puede seguir clasificando el mail. Asignar un comprobante a una partida concreta es una regla aparte, con el número de comprobante o con una elección del operario. No hace falta un segundo IMAP.

La API, cuando exista, carga partidas y después usa el mismo cruce para llegar a un mail. Otras exportaciones (pagos ya acreditados, lista de clientes con mail) reemplazan la suposición de «no vino en el Excel, entonces pagó». Hasta entonces, el Excel de un saldo por cliente sigue siendo la fuente de verdad del lunes.

### Qué no se reconstruye

- La cola SMTP, el tope de 5 cada 30 segundos y el advisory lock del watcher.
- El cruce por `message_id` / `In-Reply-To`. Sigue habiendo un mail por cliente.
- El maestro como fuente del mail, la regla de no pisar `prefiere_no_recibir_email`, y el preview que no escribe.
- La plantilla Jinja y premailer. Se le agrega el listado de partidas; no se cambia de motor.
- El login, el cifrado de credenciales y el ciclo como unidad de la campaña.
- Los `envios` históricos. Se leen con `saldado_en` y un monto. No se migran a partidas inventadas.

Y el lunes tampoco se reconstruye nada. El sistema de una lista de clientes, un Excel de los que deben, un monto y un mail queda en producción, con la integridad de arriba. El rediseño arranca cuando el archivo real, o la API, traiga comprobantes que haya que cobrar por separado.
