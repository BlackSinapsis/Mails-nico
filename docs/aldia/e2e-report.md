# Informe E2E — Mails Nico

Validación de punta a punta sobre la rama `codex/handoff-analysis` (código de `master` más documentación). No se modificó la aplicación ni se envió correo real. SMTP e IMAP apuntaron a un servidor local que acepta cualquier login.

Capturas y video: `/cursor/stores/bc-e3888865-dbcf-40ea-ad14-c88145c1b21c/media/e2e/`. El recorrido principal está en `e2e-flujo-principal.mp4`.

## Entorno

- Backend: FastAPI en `127.0.0.1:8000`, SQLite `backend/dev.db`, Alembic al head, usuario `operario`.
- Frontend: Vite en `127.0.0.1:5173`.
- Correo: `smtp.mail.yahoo.com`, `imap.mail.yahoo.com`, `smtp.gmail.com` e `imap.gmail.com` resueltos a `127.0.0.1` y `::1`. Certificado local en el trust store. Puertos 587 (STARTTLS) y 993 (SSL). Los mensajes quedan en `/tmp/fake-mail/sent` y la bandeja de prueba en `/tmp/fake-mail/inbox`.
- El límite de 5 mails cada 30 segundos no se tocó. En el log del proceso aparece `Rate limit: esperando 30.0 segundos`.

## Pruebas automáticas

| Suite | Resultado |
|---|---|
| pytest backend | 190 passed, 82 warnings, 43.70 s |
| `npm run lint` | 6 errores (badge y button: react-refresh; input y textarea: interface vacía; `ciclos.ts`: dos `catch` vacíos) |
| `npm run build` | OK (`tsc -b` y Vite). El frontend no tiene script de tests. |

## Excel de ejemplo

Archivo usado tal cual: `/cursor/stores/bc-e3888865-dbcf-40ea-ad14-c88145c1b21c/datos/maestro_50_clientes.xlsx`.

| Dato | Valor |
|---|---|
| Hoja | `Clientes`, rango A1:D51, 50 filas de datos |
| Encabezados | `nro cliente`, `nombre`, `email`, `localidad` |
| Clave | texto, formato `@`, 8 dígitos, única. Primera: `00000001` Consorcio Acacias 120, `cliente01@example.com`, CABA. Última: `00000050` Consorcio Golondrinas 1933, `cliente50@example.com`, Caseros |
| Email | las 50 filas traen email |

El parser actual lo acepta limpio. Esos cuatro encabezados son alias que ya reconoce. No hace falta rellenar ceros: la clave ya llega como texto de 8 dígitos. La UI, al subirlo primero y sin tocarlo, dijo «50 nuevos, 0 actualizados de 50 clientes» y la fila de Acacias siguió mostrando `00000001`. Captura: `03-maestro-cargado.png`.

Los Excel de deudores de la prueba se armaron con esas mismas claves (`nro cliente`, `nombre`, `monto`), también en texto de 8 dígitos, salvo los casos a propósito: la clave numérica `13` (el maestro tiene `00000013`) y la clave `12` en el segundo corte. Esas dos no matchean. El parser hace `str(valor).strip()` y no aplica `zfill`.

Con monto mínimo de plantilla $1.000, el primer corte quedó así:

- Para enviar (9): `00000001`, `02`, `03`, `04` (la clave estaba duplicada, 8000 y después 9000; gana la última), `05`, `07`, `12`, `20` y el alta manual `00000099`.
- Sin email (3): `00000006` (el maestro sin columna email le borró el correo), clave `13`, y `99999999` (no está en el maestro).
- Filtrados (2): `00000008` dado de baja, `00000009` monto $450.
- Descartados en silencio, no aparecen en el preview: `00000010` con monto texto `150.000,50`; `00000011` con 0 y con -1500; filas con clave, nombre o monto vacíos, y monto `no-es-un-monto`.

Preview de la API: `para_enviar=9`, `sin_email=3`, `filtrados=2`, `total_deudores=14`, `duplicados=1`. El aviso de duplicado está. No hay lista de errores por fila ni descarga.

El archivo de ~600 filas (`deudores_volumen.xlsx`) repite esas columnas y agrega claves sintéticas `00000051`–`00000600` porque deduplicar contra solo 50 claves no mediría el rate limit. No se ejecutó esa campaña; ver Volumen.

## Flujos

| Flujo | Resultado |
|---|---|
| Login | Pasa. Credencial incorrecta muestra «Usuario o contraseña incorrectos» (`01-login-error.png`, `02-despues-de-login.png`). |
| Maestro, archivo real | Pasa. 50 clientes, claves de 8 dígitos intactas. |
| Maestro sin columna email | Falla el dato: actualiza `00000006` y el email pasa a «—» (`04-maestro-sin-columna-email.png`). |
| Maestro con celda de email vacía | Falla el dato: borra el email de `00000002`. Se restauró a mano a `cliente02@example.com` (`05-maestro-email-vacio.png`). |
| Alta, edición y baja manual | Pasa. Alta `00000099`, edición a `manual-editado@example.com`, baja de `00000008` visible como «Eliminado» en inactivos (`06`–`08`). |
| Plantilla | Pasa si se carga el logo y después se completan asunto y monto. Asunto persistido: «Aviso de saldo pendiente», mínimo `1000.00` (`09-plantilla.png`). Subir el logo reemplaza el estado del formulario con la respuesta del servidor y se lleva lo no guardado. |
| Configuración Yahoo y Gmail | Pasa contra el servidor local. SMTP e IMAP «conecta». Se dejó Yahoo activo antes de enviar (`10`, `11`). |
| Excel vacío | Pasa el rechazo: «El archivo está vacío». No deja confirmar (`12`). |
| Solo encabezados | El botón «Enviar 0 mails» queda habilitado. No pide confirmar «cartera sin deuda» (`13`). |
| `.xls` que no es un xlsx | 500 `zipfile.BadZipFile`. La UI dice «Failed to fetch» (`14`). |
| Preview del primer corte | Pasa con los números de arriba (`15`–`18`). |
| Confirmar y solapar | El primer corte se envió. El segundo se confirmó mientras el primero todavía mandaba. La UI no pide cancelar los pendientes; solo avisa que desaparecería más de la mitad (`19`, `20`). En la base, el ciclo 2 se creó a las 22:02:30 y marcó saldados a `00000012` y `00000020` en ese instante; esos mails salieron a las 22:02:56. |
| Enviados y reenvío | El rechazo SMTP de `cliente04` dejó un pendiente. «Reenviar» lo mandó después (`23`–`25`). |
| Seguimiento | Texto de Acacias marcado pago a mano. Aromos pasó a pago por adjunto. Cedros rebotó (`26`, `27`). El refresco manual tomó esas respuestas. No quedó captura de la solapa Rebotados: el script se cortó por un locator duplicado del aviso «No es una confirmación de acreditación», que está en la solapa y en el drawer. La base sí tiene `00000007` en `REBOTADO`. |
| Dashboard | Antes del corte vacío: deuda $255.500, 5 deudores, variación -$86.950,5 (25,4% menos). Tras atrasar el ciclo 1 a 2026-05-26, deuda +90 días $19.500 (`30`–`32`). |
| Corte sin filas confirmado | Deuda $0, 0 deudores, -$255.500 / 100% (`36`–`38`). |
| Perfil de cliente | No se abrió. El click en el primer «Consorcio» del dashboard no navegó a `/clientes/**`. |
| Unsubscribe | El token que se copió del mail estaba truncado en el primer `=` y respondió 400 `Link inválido`. `00000020` sigue sin la baja. El link completo no se llegó a abrir. |

## Estados que mienten

Los cuatro se reprodujeron en el navegador, sin cambiar la app. Severidad según lo que el operario puede hacer con lo que ve.

### 1. Un error de la API en Seguimiento se ve como «Sin registros» y los contadores en 0

Confirmado.

Con la API sana, el ciclo 2 (23/9/2026) muestra Arrayanes, Acacias, Aromos y Cedros. La base de ese corte tiene 1 no contestado con `message_id` (Arrayanes), 2 pagos (Acacias a mano, Aromos con adjunto) y 1 rebotado (Cedros). Captura sana: `46a-seguimiento-ciclo2-real.png`.

Repro:

1. Ingresar y abrir Seguimiento.
2. En el selector elegir «Ciclo #2 — 23/9/2026».
3. Hacer que `GET /ciclos/{id}/envios` responda 500 (en la prueba, el navegador interceptó esa URL; el servidor seguía sano y el mismo GET directo devolvía los cuatro registros).
4. Recargar y volver a elegir el ciclo 2.

Resultado: el selector sigue diciendo «Ciclo #2 — 23/9/2026» y el subtítulo habla del ciclo histórico, pero las cuatro solapas quedan en (0) y el cuerpo dice «Sin registros.». No hay banner de error. El `catch` de la carga y del cambio de ciclo solo hace `console.error`. Captura: `46-seguimiento-error-como-vacio.png`.

«Refrescar ahora» sí escribe el error en pantalla. La mentira es la carga inicial y el cambio de ciclo: un fallo y una bandeja vacía se ven iguales.

Severidad alta. Un corte con pagos y rebotes puede leerse como que nadie respondió.

### 2. El maestro muestra «0 clientes» mientras carga

Confirmado.

`MaestroPage` arranca con la lista vacía y pinta `{cantidad} clientes registrados` antes de que vuelva `GET /maestro`. No hay estado de carga.

Repro:

1. Ingresar.
2. Demorar `GET /maestro` (en la prueba, la respuesta quedó retenida).
3. Abrir Maestro de Clientes y mirar el primer pintado.

Resultado: título «0 clientes registrados» y tabla vacía, con los botones de agregar y actualizar ya activos (`44-maestro-cero-mientras-carga.png`). Al soltar la respuesta, el mismo encabezado pasa a «50 clientes registrados» y aparecen las filas, con `00000001` intacto (`45-maestro-despues-de-cargar.png`). La API tenía 51 filas y 50 activas; una está inactiva y el default no la muestra.

Severidad media. Con red lenta parece que el maestro está vacío. Se corrige solo cuando llega la respuesta.

### 3. Durante un envío activo sigue visible el ciclo anterior y «Reenviar todos» queda habilitado

Confirmado. No se apretó el botón.

Repro:

1. Confirmar un corte con dos envíos buenos (`00000017` Olivos, `00000018` Palmeras) y uno rechazado por el SMTP de prueba (`00000010` Fresnos, `cliente10@example.com`). Al terminar, Para enviar muestra Fresnos y «Reenviar todos (1)», y Enviados muestra Olivos y Palmeras.
2. Sin recargar, confirmar otro Excel de 6 claves (`00000027`–`00000032`).
3. Mirar la pantalla mientras la barra dice «Enviando mails...».

Resultado, con la barra en «2 / 6» (el rate limit del proceso todavía contaba los tres envíos del corte anterior y pausó 30 segundos):

- Para enviar sigue listando Consorcio Fresnos 453, $17.000, con «Reenviar» y «Reenviar todos (1)» habilitado (`47-envio-activo-ciclo-previo-y-reenviar.png`).
- Enviados sigue listando Olivos y Palmeras. Hortensias y el resto del corte nuevo no están (`48-enviados-del-ciclo-previo-durante-envio.png`).
- El subtítulo sigue diciendo «Ciclo actual antes de confirmar el envío de mails».

`enviosActivo` no se vuelve a pedir hasta el `done` del SSE. Al confirmar se limpia el preview y la página vuelve a pintar esa lista vieja.

El botón masivo pega a `POST /ciclos/activo/reenviar-fallidos`, que mira el ciclo activo del servidor, no las filas que se ven. El «(1)» y Fresnos no describen ese lote. El «Reenviar» de la fila pega a `POST /envios/{id}/reenviar` con el id viejo. Ese endpoint no exige que el ciclo del envío siga activo; `revalidar_para_reenvio` solo mira el maestro. No se hizo el click, así que el reenvío paralelo no se ejecutó.

Severidad alta. En medio de una campaña la pantalla mezcla el corte viejo con la barra del nuevo, y las dos acciones de reenvío siguen prendidas.

### 4. El drawer dice «Ciclo #N» con la racha, no con el número de corte

Confirmado.

El selector de Seguimiento usa `Ciclo.numero`. El drawer usa `envio.ciclo_numero`, que es la racha de cortes consecutivos debiendo (`_ciclos_consecutivos_deudor`: arranca de cero si no hay envío previo, si el último fue pago o si tiene `saldado_en`).

Repro:

1. Abrir Seguimiento, solapa No contestados.
2. Elegir el ciclo 4. Naranjos (`00000015`) aparece por primera vez en ese corte: la racha es 1 y el corte es el 4.
3. Abrir la ficha.

Resultado: el selector dice «Ciclo #4 — 23/9/2026» y el drawer dice «00000015 · Ciclo #1» (`49-drawer-ciclo-es-racha.png`). La API del mismo envío trae `ciclo_numero: 1` y el ciclo tiene `numero: 4`.

Cuando los dos números coinciden, la etiqueta parece el corte. En el ciclo 2, Acacias tiene racha 2 y el corte también es el 2. Ahí no se nota.

Severidad media. En un histórico, «Ciclo #1» se lee como el primer corte del sistema y es la racha de esa deuda.

## Otros bugs del recorrido

| Qué | Esperado | Qué pasó | Severidad |
|---|---|---|---|
| Maestro sin columna email o con celda vacía | No pisar un email existente con vacío (Q20) | `00000006` y `00000002` quedaron sin email | Alta |
| Filas inválidas del Excel de deudores | Bloquear el corte y listar fila, columna, valor y motivo; descargar el listado (Q15) | Se descartan en silencio. El duplicado solo avisa y usa la última fila | Alta |
| Clave numérica y monto argentino | Normalizar a 8 dígitos y aceptar `150.000,50` (Q15) | `13` no matchea `00000013`. `150.000,50` desaparece | Alta |
| Archivo solo con encabezados | Confirmación explícita de cartera sin deuda (Q15) | «Enviar 0 mails» habilitado. Confirmado, el dashboard pasó a $0 | Alta |
| Corte nuevo con envíos en curso | Cancelar pendientes y pedirlo en la UI; revalidar antes de cada mail (Q18) | No pregunta. Mails del corte anterior salieron después de `saldado_en` | Alta |
| `.xls` inválido | 422 con mensaje claro | 500 y «Failed to fetch» | Media |
| Logo de la plantilla | Conservar lo escrito y todavía no guardado | El upload reemplaza el formulario | Media |
| Fecha de corte | Obligatoria, distinta de `creado_en` (Q23) | No hay campo. Antigüedad y +90 usan `creado_en` | Media |
| Pausa y selección de destinatarios (Q16, Q17) | Pausa por cliente y checkbox de envío | No están en la UI | Confirmado, no implementado |

## Decisiones Q15–Q23

Contra `docs/grilling-decisiones-15-23.md` y el prep `internal/grilling-15-23-prep.md`.

| Decisión | Veredicto |
|---|---|
| Q15 filas inválidas, bloqueo, listado, `zfill`, monto argentino, cartera sin deuda | Confirmado que el producto no hace eso. El archivo vacío sí se rechaza; el de solo encabezados no. |
| Q16 pausa | Confirmado que no está. |
| Q17 selección manual | Confirmado que no está. «Reenviar todos» sigue siendo el reintento de fallidos, no una selección. |
| Q18 cancelar pendientes y revalidar | Confirmado que no está. El solapamiento mandó mails ya saldados. Esta pasada suma que la UI deja el corte anterior y el reenvío habilitado durante el envío nuevo. |
| Q19 resultado incierto | No reproducido como corte de red después de un 250. Queda el riesgo abierto: un SMTP 550 deja el envío sin `message_id` y entra en reenvío. |
| Q20 no pisar email manual ni vaciar email | Confirmado el fallo. El merge pisa el email, incluido el vacío. La baja voluntaria no se probó como campo preservado en este recorrido; la baja de UI es `activo=false`. |
| Q21 polling 10 min, seguir también a contestados, `/health` sin DB | El refresco manual actualizó no contestados. El poll contra 600 mensajes de la bandeja tardó 26,7 s (sección Volumen) y solo reclasificó `NO_CONTESTADO`. `/health` responde `{"status":"ok","database":"ok"}` y toca la base. No se vio seguimiento de un contestado que después manda comprobante. |
| Q22 soporte | Fuera del producto. No se probó. |
| Q23 fecha de corte | Confirmado que no está. Atrasar `creado_en` del ciclo 1 a mayo movió el +90 a $19.500. |

Nada de Q15–Q18, Q20 ni Q23 quedó refutado: el comportamiento deseado no está, y el recorrido lo muestra.

## Volumen

Se corrió con los Excel ya armados: `maestro_volumen.xlsx` (las 50 claves del ejemplo más `00000051`–`00000600`) y `deudores_volumen.xlsx` (600 filas, las mismas claves). El límite de 5 mails cada 30 segundos no se tocó. El maestro respondió «600 nuevos». El preview dijo 600 para enviar de 600 deudores. El monto mínimo de la plantilla se puso en 0 solo en esta base de prueba, para que las 600 salieran.

| Medición | Resultado |
|---|---|
| Primer mail | 22:20:16 UTC |
| Último mail | 23:45:14 UTC |
| Duración de punta a punta | 5098,6 s (84 min 59 s), 600 archivos SMTP y 600 `message_id` |
| Pausas del rate limit | 119 huecos entre tandas de 5. 116 midieron 30,04 s de mediana y de media |
| Huecos largos, sin línea de log en el medio | 339 s, 625 s y 635 s. Estiran el reloj de pared. Sin ellos, 119 pausas de 30 s son 59 min 30 s |
| Memoria del proceso | 221 muestras cada 15 s, mientras iban 550 de 600: RSS entre 116 y 127 MB. El mismo proceso siguió hasta el mail 600 |
| SQLite | Antes de enviar, con el maestro ya cargado: 196.608 bytes, 0 envíos. Al terminar: 516.096 bytes, 600 envíos. Crecimiento: 319.488 bytes |

Recarga a mitad, con la barra en «5 / 600» (`40-volumen-progreso.png`, `41-volumen-tras-reload.png`): al recargar, la barra volvió sola a «Enviando mails... 5 / 600» y el texto dijo que 595 mails seguían mandándose y no aparecen en Para enviar para no mandarlos dos veces. El envío no se cayó con la recarga. `42-volumen-fin.png` es el momento en que el arnés dejó de esperar (550/600, tope de 80 minutos). El proceso siguió y completó los 600.

Reinicio:

- `SIGTERM` sobre el proceso de los 600, cerca del mail 575: el puerto 8000 dejó de aceptar (el login del arnés recibió conexión rechazada) pero ese mismo proceso siguió mandando hasta el 600 y recién ahí terminó. No hizo falta que un proceso nuevo retomara la cola: la vació el que ya estaba.
- `SIGKILL` en un corte aparte de 8 mails (`00000001`–`00000008`), matado cuando había 5 `message_id`: el proceso murió en el acto. A los 25 s de levantar el backend de nuevo seguían 5 enviados y 0 archivos SMTP nuevos. La UI ofreció «Reenviar todos (3)» para Ceibos, Cedros y Cerezos (`43-volumen-tras-reinicio.png`). Un kill brusco no reanuda lo que faltaba.

IMAP: con 600 mensajes en la bandeja de prueba, uno por cada `message_id`, `_poll_inbox` tardó 26,660 s y pasó los 600 a `CONTESTADO`. Una pasada anterior, cuando solo había 550 enviados, tardó 24,476 s y clasificó esos 550; los 50 todavía sin `message_id` quedaron `NO_CONTESTADO`. El watcher solo mira `NO_CONTESTADO`.

## Cierre de lo que faltaba

### Perfil de cliente

`/clientes/00000001` abre directo. El click desde el dashboard, en el recorrido anterior, no navegaba. La ficha de Consorcio Acacias 120 muestra la clave `00000001`, «Al día», `cliente01@example.com`, CABA, Activo. Deuda actual «—», saldado histórico $200.000, respuestas 1 de 2. La tabla tiene el ciclo #2 del 23/09/2026 por $200.000, «Pagó», saldado ese día, y el ciclo #1 del 26/05/2026 por $185.000,50, «Sin respuesta», también saldado el 23/09/2026. Captura: `50-perfil-cliente.png`.

### Unsubscribe con el token completo

El link se sacó del `.eml` decodificando el quoted-printable, no cortándolo en el primer `=`. El token tiene 100 caracteres y, en claro, es `00000005` más 64 hex del HMAC. Abrir `http://127.0.0.1:8000/unsubscribe/[token redactado]` mostró «Listo, diste de baja tu suscripción». En la base, Consorcio Azaleas 268 pasó `prefiere_no_recibir_email` de 0 a 1. Captura: `52-unsubscribe.png`. El token truncado del intento anterior seguía siendo un 400.

### Rebotados

En Seguimiento, solapa Rebotados, selector «Ciclo #2 — 23/9/2026»: la solapa dice Rebotados (1) y la tarjeta es Consorcio Cedros 342, `cliente07@example.com`, $10.000, estado Rebotado. Captura: `51-seguimiento-rebotados.png`.

## Qué no quedó probado

- El click de «Reenviar todos» o del «Reenviar» de una fila mientras otro corte seguía mandando. Sí quedó el botón habilitado y las filas del corte anterior en pantalla.
