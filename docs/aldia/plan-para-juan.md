# Para la reunión con Juan

Lo cerramos el 23/09/2026. La campaña de 600 ya está medida: el detalle está en [Medir la campaña de 600](wayfinder/issues/41-campana-de-600-medida.md) y en la sección Volumen de [e2e-report.md](e2e-report.md).

Para tener a mano:

- El mapa: [mapa-wayfinder.md](mapa-wayfinder.md)
- Los tickets: [wayfinder/issues/](wayfinder/issues/)
- Lo que falta votar: [decisiones-pendientes.md](decisiones-pendientes.md)

El corte del lunes 28/09 está en [flujo-cobro-dos-tipos.md](flujo-cobro-dos-tipos.md): se sigue usando lo que ya está en producción, con un monto y un mail por cliente, y primero se arreglan los errores.

## Dónde está el producto

La app ya manda recordatorios en producción. Sube el Excel de deudores, lo cruza con el maestro, manda el mail por Yahoo o Gmail y sigue las respuestas.

El problema es que el operador no puede confiar en todo lo que ve:

- Reimportar el maestro puede vaciar un mail.
- Una fila mala del Excel se salta, y eso puede dar por saldado a alguien que seguía debiendo.
- Guardar el corte y mandar los mails son el mismo clic.
- Un corte nuevo no frena lo que todavía no salió.
- Una firma con imagen se anota como pago.
- El link de baja se aplica con solo abrirlo.
- El dashboard dice «Pagó» o «Al día» cuando todavía hay saldo.

Eso es lo que hay que arreglar antes de cambiar las pantallas.

Además, Julián pidió el 23/09 que el producto se sienta como una herramienta de trabajo a la altura de Twenty, Attio y Linear. O sea, más de lo que el piloto necesita para mostrar bien los montos: una UI más moderna y con movimiento cuidado. El recorte de «solo lo que cabe en USD 50 de funciones» se quedaba corto para esa experiencia.

La plata sigue igual: unos USD 50 por mes al cliente, y USD 10 de infraestructura, salvo que Neon no duerma y acepten llegar a 15.

De Twenty no se copia código. La app queda cerrada. Las librerías nuevas son MIT, Apache-2.0 o BSD.

## La campaña de 600, medida

La corrimos sobre una base de prueba SQLite, sin tocar el rate limit de 5 mails cada 30 segundos. El maestro respondió «600 nuevos» y el preview dijo 600 para enviar de 600. El monto mínimo de la plantilla se puso en 0 solo en esa base, para que salieran las 600.

El primer mail salió a las 22:20:16 UTC y el último a las 23:45:14 UTC. Quedaron 600 archivos SMTP y 600 `message_id`.

**Cuánto tardó**

- Reloj de pared: 5098,6 s, o sea 84 min 59 s.
- El piso que pone el rate limit: 119 huecos entre tandas de 5. 116 de esos huecos midieron 30,04 s, de mediana y de media. Sin los tres huecos largos, 119 pausas de 30 s son 59 min 30 s.
- Hubo tres huecos largos, sin ninguna línea de log en el medio: 339 s, 625 s y 635 s. Son los que estiran el reloj. Todavía no sabemos la causa.

**Cuánto ocupó**

- Memoria: 221 muestras cada 15 s, mientras iban 550 de 600. El RSS estuvo entre 116 y 127 MB. El mismo proceso siguió hasta el mail 600.
- SQLite, con el maestro ya cargado y antes de enviar: 196.608 bytes y 0 envíos. Al terminar: 516.096 bytes y 600 envíos. Creció 319.488 bytes.

**Qué pasó cuando lo interrumpimos**

- Recargamos la página con la barra en «5 / 600». Volvió a «Enviando mails... 5 / 600» y avisó que 595 mails seguían mandándose y que no aparecen en Para enviar, para no mandarlos dos veces. El envío no se cayó. El arnés dejó de esperar en 550/600 (tenía un tope de 80 minutos), pero el proceso completó los 600.
- Con un `SIGTERM` cerca del mail 575, el puerto 8000 dejó de aceptar conexiones. Ese mismo proceso siguió hasta el 600 y recién ahí terminó. No hizo falta levantar otro.
- Con un `SIGKILL`, en un corte aparte de 8 mails (`00000001` a `00000008`), matado cuando había 5 `message_id`, el proceso murió en el acto. A los 25 s de levantarlo seguía habiendo 5 enviados y 0 archivos SMTP nuevos. La UI ofreció «Reenviar todos (3)» para Ceibos, Cedros y Cerezos. Conclusión: un kill brusco no retoma lo que faltaba. En esta corrida no hubo ningún mail duplicado.

**Lectura de respuestas (IMAP)**

- `_poll_inbox` con 600 mensajes, uno por `message_id`, tardó 26,660 s y pasó los 600 a `CONTESTADO`.
- Con 550 enviados tardó 24,476 s y clasificó esos 550. Los 50 sin `message_id` quedaron en `NO_CONTESTADO`.
- El watcher solo mira `NO_CONTESTADO`. El refresco manual actualizó los no contestados (Q21: 26,7 s).
- `/health` responde `{"status":"ok","database":"ok"}` y toca la base.
- No probamos el caso de alguien que contesta y después manda el comprobante.
- Nada de esto es una lectura de CU-h de Neon.

## Capa 1: los arreglos que van primero

Son 16 tickets y se construyen primero.

Sobre el tamaño: **S** es un cambio local, **M** es una pantalla o una migración con su prueba, y **L** son varios flujos. No son días de calendario.

| Ticket | Tamaño | Qué queda hecho |
| --- | --- | --- |
| [Diff del maestro](wayfinder/issues/02-diff-del-maestro.md) | M | Se ve qué cambiaría en la lista de clientes antes de aplicarlo. Un mail vacío no pisa uno cargado. |
| [Errores de fila y tope](wayfinder/issues/01-filas-clave-repetida-y-tope.md) | M | Una clave o un monto mal, o una clave repetida, bloquean. Se pueden descargar. Un Excel enorme se rechaza. |
| [Fecha de corte](wayfinder/issues/03-fecha-de-corte.md) | S | El día del Excel no es el momento de la carga. |
| [Guardar sin enviar](wayfinder/issues/14-guardar-el-corte-sin-enviar.md) | L | El historial se actualiza sin mandar mails. Después se elige a quién escribir. |
| [Cancelar obsoletos](wayfinder/issues/15-cancelar-envios-obsoletos.md) | M | Un corte nuevo frena lo que no salió, y lo avisa. |
| [Pausa](wayfinder/issues/16-pausar-recordatorios.md) | M | Se deja de escribirle a un consorcio sin tocar el saldo. |
| [Listas honestas](wayfinder/issues/18-listas-honestas-y-marcar-pago.md) | M | Un error de red no parece «nadie contestó». El resultado del envío no desaparece. |
| [Dashboard creíble](wayfinder/issues/19-dashboard-creible.md) | M | Un comprobante no apaga la deuda. Esta pantalla se queda. El clic en el consorcio abre `/clientes/{clave}` (la ficha por URL ya abre). |
| [Buscar y seguir contestados](wayfinder/issues/06-seguir-a-quien-contesto.md) | M | Filtro en la lista. Un comprobante que llega después de un «contestó» se lee. |
| [Baja y backup](wayfinder/issues/07-baja-por-post.md) | M | El GET no da de baja. Una restauración ya se ensayó. |
| [La firma no es un pago](wayfinder/issues/05-la-firma-no-es-un-pago.md) | S | Solo cuenta un adjunto de verdad, del mail del consorcio. |
| [HTML del mail](wayfinder/issues/04-escapar-el-html-del-mail.md) | S | Un nombre con etiquetas no arma un link. |
| [Logout](wayfinder/issues/13-el-logout-invalida-la-sesion.md) | M | Cerrar sesión mata el token. La clave de producción no entra acá. |
| [Confirmar marcar como pago](wayfinder/issues/18-listas-honestas-y-marcar-pago.md) | S | Un diálogo que dice qué va a pasar. Sin un deshacer de mentira. |
| [Medir 600](wayfinder/issues/41-campana-de-600-medida.md) | S | Cerrado. 84 min 59 s de reloj, piso de 59 min 30 s, tres huecos sin causa. |
| [Ensayo con el operador](wayfinder/issues/37-ensayar-los-dos-cortes.md) | M | Dos cortes acompañados, el primero con un lote chico. |

En paralelo, y también antes de dar el piloto por cerrado:

- tests de las reglas,
- una sola forma de mostrar pesos y fechas,
- etiquetas y foco,
- Sentry en el plan gratis,
- logs sin datos,
- el pool configurado para que Neon pueda dormir,
- el blueprint en Starter,
- el CI,
- sacar el frontend de Vercel Hobby y pasarlo a Cloudflare Pages.

Leer el panel de Neon le toca a quien tenga la cuenta.

La clave de producción sigue en pausa por decisión de Julián. No es un ticket.

## Capa 2: la experiencia que pidió Julián

Son 7 tickets. Empiezan cuando la integridad ya está escrita: el rediseño espera la baja, la firma, el HTML y la confirmación de pago. No es una lista de ideas para algún día; está comprometida.

| Ticket | Tamaño | En quién se inspira | Con qué | Cómo se siente |
| --- | --- | --- | --- | --- |
| [Rediseño visual](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md) | L | Twenty, Attio, Linear, sobre la marca actual | Tailwind y shadcn, que ya están en el repo | Jerarquía, densidad, tipografía y superficies en toda la app. No es retocar una página. |
| [Movimiento](wayfinder/issues/31-sistema-de-movimiento.md) | M | Linear, Raycast, Apple, Emil | CSS. Motion solo si alguna interacción no se puede hacer con CSS | Paneles a 200 ms con ease-out, menos movimiento cuando el sistema lo pide, el botón acusa el clic. Sin entradas de página ni tickers. |
| [Tabla densa](wayfinder/issues/25-tabla-densa-de-registros.md) | L | Twenty, Attio | TanStack Table (MIT) | Orden, filtro, vistas guardadas y acciones por lote. |
| [Panel y línea de tiempo](wayfinder/issues/32-panel-y-linea-de-tiempo.md) | M | Twenty, Attio, Upflow | Sheet de shadcn (MIT) | El consorcio al lado de la lista: mails, respuestas, comprobantes, pausas. |
| [Menú de comandos](wayfinder/issues/33-menu-de-comandos.md) | M | Linear, Attio | `cmdk` (MIT) | Ctrl+K para saltar y actuar. Aparece al instante. |
| [Hoy](wayfinder/issues/34-hoy-al-lado-del-dashboard.md) | M | Linear (cola de excepciones) | Las mismas cifras, en otra ruta | Comprobante, sin email, rebote, pausa vencida. El dashboard sigue. |
| [Vista previa del mail](wayfinder/issues/22-plantilla-logo-y-previa.md) | S | El editor medido en la evaluación de UI; Upflow y Chaser muestran el mensaje | El HTML que ya genera el backend, en un iframe | Ves el mail mientras editás la plantilla. |

En peso de trabajo hay dos tramos largos (el sistema visual y la tabla con vistas) y cinco piezas concretas. Es más que una pasada de estilos, y es menos que reescribir el producto.

## Qué tomamos de los CRM

- **Twenty y Attio:** el diff antes de importar, el reporte de filas con error, la tabla densa, las vistas guardadas, las acciones por lote y el panel al lado de la lista.
- **Upflow:** guardar la deuda y mandar la campaña son dos actos. La historia del consorcio junta mail, respuesta y comprobante. La pausa no toca el saldo.
- **Chaser:** en la fila se ve el estado y el motivo (sin email, baja, mínimo). La pausa es un apagado con motivo, no un expediente.
- **Linear:** la paleta para saltar y actuar, sin animarla. Hoy como cola de excepciones, no como reemplazo de las cifras.

## Lo que dejamos afuera

Lo miramos y no entra:

- DSO y forecast,
- un kanban de toda la gestión,
- el pixel de apertura,
- un portal de pago,
- informes o clasificación por IA,
- notas y tareas como módulo aparte,
- el modo oscuro como proyecto (si al tener los tokens sale gratis, bien, pero no se le dedica una fase).

Tampoco el fork de Twenty, ni `empresa_id`, ni Framer Motion para animar páginas. La lista completa está en [No construir esto](wayfinder/issues/28-no-construir-esto.md).

## Los tres choques, ya resueltos

1. **Hoy.** Se suma. El dashboard de cifras no se borra ni se parte en «Tendencia».
2. **Búsqueda.** El campo de la tabla filtra lo que está abierto, y además hay paleta `cmdk`. Esto da vuelta el default anterior de «sin paleta».
3. **Marcar como pago.** Pide confirmación con el nombre y el efecto. No hay toast de deshacer, porque el servidor no vuelve a «contestado».

## Después de la reunión

Se construye la capa 1 a partir de los tickets, en el orden del mapa. La capa 2 empieza cuando esa integridad ya está escrita.

El PR de documentación al fork (`Documentos/`, ADRs, `CONTEXT.md`, `PENDIENTES.md`) se abre solo cuando ustedes digan que sí. Hasta entonces no se pushea ni se commitea nada en el repo.

**Lo que falta votar en la reunión:**

- repos y cuál es el canónico,
- el titular del código,
- si la clave de producción sigue en pausa,
- USD 10 o hasta 15,
- el horario de soporte,
- la forma del Excel real,
- quién lee el panel de Neon.

**Lo que puede esperar:** la AAIP, `cssutils` y la segunda empresa.
