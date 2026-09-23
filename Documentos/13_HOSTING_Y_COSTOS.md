# Hosting y costos: piloto y evolución

> Actualización del grilling: el usuario fijó un presupuesto objetivo de infraestructura de **USD 10/mes**. Los escenarios superiores se conservan como comparación; no cumplen ese objetivo ni fueron aprobados. Falta verificar una configuración completa dentro del presupuesto con consumo real, archivos y recuperación.

Fecha de consulta: 13/09/2026. Estado: investigación y propuestas; ninguna migración ni contratación realizada.

## Decisión que hay que tomar

Para el piloto tentativo del 25/09, recomiendo conservar el backend Python y Neon, verificar los planes efectivos y corregir las condiciones que impiden operar el correo o conservar archivos. El frontend estático sí es candidato a Cloudflare con poco cambio funcional. Migrar todo el backend a Workers antes de la entrega agregaría trabajo que todavía no demuestra un beneficio para este cliente.

Esta recomendación distingue compatibilidad técnica de conveniencia económica. No conocemos las facturas, consumos, descuentos ni servicios compartidos de Juan y Julián. No hay un ahorro confirmado.

## Qué necesita esta aplicación

Inspección de configuración y código públicos del repositorio; no se leyeron archivos de secretos ni se accedió a cuentas de proveedores.

| Necesidad observada | Evidencia del repo | Consecuencia para hosting |
|---|---|---|
| Frontend React/Vite compilado a archivos estáticos | `frontend/package.json`, `frontend/vercel.json` | Se puede alojar separado del backend; requiere rutas SPA y URL pública de la API |
| FastAPI Python en contenedor, Gunicorn y migraciones al arrancar | `backend/Dockerfile`, `backend/entrypoint.sh` | Encaja en un servicio de contenedores o VPS; no es una función aislada lista para Workers |
| Gmail/Yahoo por SMTP 587 y respuestas por IMAP 993 | `backend/app/core/email_providers.py` | El host debe admitir esas conexiones salientes; no alcanza con que responda la página |
| Consulta automática del correo cada diez minutos | `backend/app/services/imap_watcher.py`, `backend/app/main.py` | Requiere proceso vivo o un mecanismo programado equivalente |
| Campañas con tareas en memoria y progreso al navegador | `backend/app/routers/ciclos.py` | Un reinicio puede interrumpir trabajo; pagar un host no vuelve duraderas esas tareas |
| Logo escrito en carpeta `uploads` y servido desde backend | `backend/app/routers/plantilla.py` | Necesita disco persistente, almacenamiento de objetos o un activo fijo; guardar su URL en Neon no conserva el archivo |
| PostgreSQL mediante SQLAlchemy/psycopg2 y bloqueo de sesión del watcher | `backend/app/core/database.py`, `backend/app/services/imap_watcher.py` | Revisar conexión directa/pool y coordinación antes de cambiar conectividad o número de procesos |

`render.yaml` declara `plan: free`. Esto prueba la configuración versionada, **no el plan que está activo en Render**: pudo haberse cambiado en el panel.

## Condiciones decisivas de los proveedores

### Render: verificar primero el servicio efectivo

Render Free bloquea salida SMTP en puertos 25, 465 y 587. El cambio ya estaba vigente en septiembre de 2025. Gmail y Yahoo usan 587 en este proyecto: si el backend efectivo sigue en Free, su envío actual no es compatible con esa condición. Un servicio de cómputo pago elimina esa limitación. [Cambio oficial de SMTP](https://render.com/changelog/free-web-services-will-no-longer-allow-outbound-traffic-to-smtp-ports).

Además, Free duerme después de quince minutos sin tráfico entrante, tarda aproximadamente un minuto en volver, no permite disco persistente y puede reiniciarse. Tiene 750 horas gratuitas por workspace; el exceso puede suspender servicios. Su filesystem es efímero, también en reinicios y despliegues. Render desaconseja Free para producción. Consecuencia: el watcher no seguirá consultando mientras el proceso esté dormido y el logo puede perderse. Las consultas salientes no sustituyen tráfico entrante. [Límites oficiales](https://render.com/docs/free).

Referencia publicada: cómputo web de 512 MB desde USD 7/mes; disco USD 0,25/GB-mes. El workspace tiene una tarifa separada: Hobby USD 0 más cómputo; Pro USD 25 más cómputo. No confundir pagar workspace con cambiar un servicio Free. Render también permite frontend estático sin tarifa de instancia, sujeto a consumos del workspace. No se validó aquí si 512 MB soporta el Excel real y los procesos configurados. [Precios de Render](https://render.com/pricing).

### Vercel: el uso comercial afecta la elección

Vercel Hobby está reservado a uso personal no comercial. Su definición comercial incluye trabajo realizado con fin económico, incluso por un consultor contratado. Esta aplicación entregada a un cliente requiere evaluar Pro o alojarla en otro proveedor. No debemos asumir que bajo tráfico hace apropiado Hobby. [Fair Use](https://vercel.com/docs/limits/fair-use-guidelines).

Pro publica una base de USD 20/mes y crédito de consumo incluido; asientos de desarrollador y excedentes pueden modificar el total. Si Juan y Julián ya pagan una cuenta compartida por otros proyectos, trasladar este frontend quizá no reduzca la factura: importa el costo incremental y qué asientos necesitan. [Precios](https://vercel.com/pricing), [control de consumo](https://vercel.com/docs/pricing/manage-and-optimize-usage).

### Neon: conservarlo, medir actividad y recuperación

La oferta publicada muestra Free con 100 CU-horas/mes por proyecto, 0,5 GB por proyecto y recuperación de hasta seis horas o el límite de cambios indicado. Launch publica USD 0,106/CU-hora, USD 0,35/GB-mes y ventana de hasta siete días; no interpretar el gasto típico de su web como presupuesto de este proyecto. Revisar también restauración, transferencia, ramas y plan heredado de la cuenta. [Precios vigentes publicados](https://neon.com/pricing).

Neon puede suspender cómputo tras cinco minutos de inactividad. En este repo el watcher consulta PostgreSQL incluso para decidir si hay correos pendientes; `/health` también hace una consulta. **Inferencia a medir:** polling y monitores frecuentes pueden despertar la base repetidamente y reducir el ahorro por suspensión. [Scale to Zero](https://neon.com/docs/introduction/scale-to-zero).

Ejemplo aritmético, no medición: 0,25 CU durante 720 horas son 180 CU-horas; durante la mitad de esas horas, 90. Que el operador entre dos veces al mes no significa que la base esté activa solamente esas dos veces. No cambiar la frecuencia sin acordar cuánto puede tardar en aparecer una respuesta.

La ventana corta de recuperación gratuita no cubre por sí sola un error descubierto quince días después. Propuesta: conservar los archivos fuente y comprobantes de importación; definir copia periódica fuera del servicio y probar restauración. Una copia que nunca se restauró no acredita recuperación operativa.

### Cloudflare: separar frontend de backend

**Frontend:** Pages sirve activos estáticos gratis y sin límite de solicitudes cuando no invocan funciones. Free admite 500 builds mensuales, 20.000 archivos y 25 MiB por archivo; permite varios administradores. Son límites holgados como hipótesis para esta SPA, que hay que contrastar con el build. [Precios Pages](https://developers.cloudflare.com/pages/functions/pricing/), [límites](https://developers.cloudflare.com/pages/platform/limits/).

El alcance de ese traslado sería build de Vite, rutas de acceso directo, configuración de API, dominio, CORS y verificación de login/importación/progreso. No cambia el motor de correo ni elimina el costo del backend. Workers Static Assets es otra opción para ese mismo frontend estático. No hace falta reescribirlo ni comprar un plan de CDN por este motivo.

En las páginas de producto y condiciones consultadas no se identificó una prohibición general equivalente a Vercel Hobby para una aplicación comercial estática. No constituye una autorización contractual universal: confirmar los términos efectivos al elegir cuenta/producto. [Condiciones de Cloudflare](https://www.cloudflare.com/service-specific-terms-application-services/).

**Backend:** Cloudflare sí admite Python y FastAPI; afirmar que no ejecuta Python sería incorrecto. Pero lo ejecuta mediante Pyodide/WebAssembly. Las dependencias admitidas deben ser Python puro, ruedas compatibles o paquetes incluidos en Pyodide. No se verificó que nuestras versiones de psycopg2-binary, bcrypt, Pillow, cryptography y demás sean trasladables. [Python Workers](https://developers.cloudflare.com/workers/languages/python/), [paquetes](https://developers.cloudflare.com/workers/languages/python/packages/).

Hay diferencias concretas que obligan a adaptar y probar:

- `threading` y `multiprocessing` no son funcionales en ese entorno; el filesystem es temporal. El uso actual de executor para IMAP y archivos locales requiere alternativa. [Biblioteca estándar](https://developers.cloudflare.com/workers/languages/python/stdlib/).
- Workers tiene TCP saliente y bloquea específicamente el puerto 25. Esto **no prueba** que SMTP 587 e IMAP 993 con `smtplib`/`imaplib` funcionen sin cambios: sus conexiones deben adaptarse al runtime y verificarse. No confundir Email Workers con sincronizar automáticamente el Gmail/Yahoo existente. [TCP sockets](https://developers.cloudflare.com/workers/runtime-apis/tcp-sockets/).
- Un bucle permanente iniciado al arrancar FastAPI no se conserva como servicio permanente. `waitUntil` permite hasta treinta segundos adicionales tras responder o desconectarse el cliente; no es sustituto de una cola durable. Haría falta programar consultas y ejecutar envíos mediante trabajos recuperables. [Contexto y duración](https://developers.cloudflare.com/workers/runtime-apis/context/).

Workers Paid parte de USD 5/mes más consumo; Free tiene 100.000 solicitudes/día y límites de CPU. Que esa base sea menor no determina el costo del sistema: faltan base de datos, almacenamiento, trabajos y adaptación. [Precios Workers](https://developers.cloudflare.com/workers/platform/pricing/), [límites](https://developers.cloudflare.com/workers/platform/limits/).

Cloudflare Containers es otro producto: acepta una estrategia de contenedor, pero factura recursos activos y no equivale a ejecutar nuestro servicio permanentemente por USD 5. Sería una evaluación aparte, incluyendo reposo, persistencia y correo. No es una propuesta cerrada para este piloto. [Tarifas de contenedores](https://developers.cloudflare.com/containers/pricing/).

### VPS compacto: posible, con operación a cargo de ustedes

Un VPS Linux permite conservar Python, Docker y las conexiones del proceso. Como referencia, Hetzner publicó CX23 a EUR 5,49/mes en Alemania/Finlandia, sin IVA ni IPv4, tras el ajuste del 15/06/2026. Ese valor no incluye copias externas ni su trabajo. [Ajuste de precios](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/).

Hetzner bloquea por defecto 25 y 465, y documenta 587 como alternativa para servicios de correo externos. Eso favorece el mecanismo actual, sujeto a prueba desde el servidor. No propongo operar un servidor de correo propio. [FAQ de servidores](https://docs.hetzner.com/cloud/servers/faq/).

El costo oculto sería mantener sistema operativo, actualizaciones, TLS, despliegues, monitoreo, copias y recuperación. Si además alojamos PostgreSQL allí, una sola máquina concentra aplicación y datos. Para un único cliente y entrega próxima no lo recomiendo por una diferencia pequeña de tarifa; considerarlo si Juan y Julián ya operan infraestructura semejante y pueden restaurarla.

## Ampliación: otras alternativas económicas compatibles con el producto

Consulta adicional: 13/09/2026. Esta sección compara alternativas concretas; la síntesis de experiencias de foros y el modelo de carga se desarrollan en el documento 14. Un precio pequeño no acredita capacidad suficiente para el Excel real.

### Railway: cómodo, pero SMTP cambia el precio mínimo

Railway encaja con un backend en contenedor. Su restricción decisiva está documentada: **SMTP sólo está disponible en Pro o superior**; Free, Trial y Hobby requieren un proveedor con API HTTPS. Hay que redesplegar después de subir a Pro para aplicar la habilitación. Por lo tanto, Railway Hobby no conserva el correo actual por USD 5/mes. [Red saliente de Railway](https://docs.railway.com/networking/outbound-networking).

Pro parte de USD 20/mes, acreditados al consumo. No se suman automáticamente otros USD 20 de recursos: se paga el mínimo o el consumo superior. La referencia de recursos es USD 10/GB-mes de RAM, USD 20/vCPU-mes, USD 0,15/GB-mes de volumen y USD 0,05/GB de salida. La memoria retenida consume aun sin visitantes; importa el uso efectivo. [Precios y forma de facturación](https://docs.railway.com/pricing).

**Para este proyecto:** candidato si ustedes ya usan Railway Pro y les mejora la operación conjunta. No aparece como ganador sólo por ahorrar en un único backend de poco tráfico que necesita SMTP. Cambiar de Gmail/Yahoo SMTP a una API requiere decidir remitente, dominio, respuestas y trazabilidad; no es un ajuste de hosting transparente. El watcher también exige evitar que el servicio duerma o reemplazar su ejecución por un trabajo programado.

### Fly.io: candidato de bajo costo que merece una prueba acotada

Fly Machines permite ejecutar el contenedor Python. La tabla oficial tiene precios por región: en las tablas consultadas, una máquina `shared-cpu-1x` de 512 MB aparece aproximadamente entre USD 3,19 y 5,16/mes; con 1 GB, entre USD 5,70 y 9,20/mes. Son referencias de cómputo continuo, no presupuesto total; volumen, snapshots, transferencia y posibles IP dedicadas se calculan aparte. No elegir 256 MB sólo porque sea la fila más barata. [Precios regionales](https://fly.io/docs/about/pricing/).

Hay una respuesta del foro oficial de Fly del 19/02/2026 que indica que el puerto 587 no está bloqueado. Es evidencia publicada, no una prueba con nuestra cuenta ni con Gmail/Yahoo; la documentación de diagnóstico recomienda proveedores transaccionales si hay problemas de correo. Mantener como criterio de aceptación una conexión SMTP 587 y una IMAP 993 desde la máquina de prueba, más un envío/recepción de prueba expresamente autorizado. [Respuesta sobre 587](https://community.fly.io/t/request-to-unblock-outbound-smtp-port-587-for-app-rialma-api/27164/2), [diagnóstico oficial](https://fly.io/docs/getting-started/troubleshooting/).

Fly puede apagar máquinas sin tráfico. Para el watcher actual hay que mantener al menos una activa en la región primaria o desactivar ese apagado; de lo contrario, reaparece el mismo problema de seguimiento interrumpido. `min_machines_running` no garantiza mínimos en todas las regiones. [Autostop y autostart](https://fly.io/docs/launch/autostop-autostart/).

**Para este proyecto:** alternativa razonable para probar después de estabilizar el flujo. Conservar Neon y cambiar únicamente el backend limita el alcance. No hacer esa migración sólo para ganar unos dólares sin medir RAM, conexión y recuperación; tampoco considerar una máquina única como alta disponibilidad.

### Coolify sobre Hetzner: más recursos por tarifa, más responsabilidad

Coolify self-hosted no cobra licencia; organiza despliegues en infraestructura propia. Coolify Cloud cobra una base publicada de USD 5/mes para conectar dos servidores, pero **los servidores se pagan aparte**. No reemplaza a Hetzner ni convierte en administrados todos los componentes de la aplicación. [Precios Coolify](https://www.coolify.io/pricing).

Su guía marca como mínimo 2 CPU, 2 GB de RAM y 10 GB libres para Coolify. Hay que sumar aplicación, base si se aloja allí, imágenes Docker y copias. También advierte que compilar en el mismo servidor puede volverlo poco responsivo si consume sus recursos. Un build fuera del VPS reduce esa competencia, pero agrega configuración que deben mantener. [Instalación y dimensionamiento](https://coolify.io/docs/start-with-self-hosted).

La tarifa **EUR 5,49/mes** del CX23 está confirmada en la tabla oficial del ajuste del 15/06/2026 para Alemania/Finlandia, sin IVA ni IPv4. La página de producto describe 2 vCPU, 4 GB RAM y 40 GB, pero al consultar mostró **“not available”** para CX23. Es una referencia tarifaria, no una oferta disponible garantizada hoy; no basar el compromiso del 25/09 en conseguirlo. [Tarifa publicada](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/), [producto y disponibilidad](https://www.hetzner.com/cloud/cost-optimized/).

**Para este proyecto:** sería mi segunda línea de evaluación si ustedes quieren una base propia para varios proyectos y ya dominan Linux/Docker. Para una sola aplicación, Docker Compose sin panel también es válido si les resulta más simple. Coolify facilita tareas, pero no elimina actualizaciones del servidor, backups, restauración, monitoreo ni el impacto de que una máquina se caiga. El SMTP 587 permitido por el VPS no elimina límites o rechazos del proveedor de correo.

### Consolidar frontend, backend y PostgreSQL en Render

También es una opción concreta: frontend estático, el backend Python ya compatible y una base PostgreSQL paga en el mismo proveedor. El nivel inicial de base dispone de **0,1 CPU, 256 MB de RAM y hasta 100 conexiones**. Son recursos modestos: el máximo de conexiones no significa que cien operaciones pesadas simultáneas rindan bien. [Especificaciones de cómputo](https://render.com/docs/compute-plans).

La referencia de base es USD 6/mes más almacenamiento a USD 0,30/GB-mes; puede comenzar con 1 GB. Con backend desde USD 7, el piso aritmético de esas dos instancias y 1 GB de base sería **USD 13,30/mes**, antes de workspace pago, disco de uploads, copias externas, transferencia y otros cargos. No usar las tarifas antiguas que incluían almacenamiento en el cómputo. [Precios](https://render.com/pricing), [modelo de almacenamiento](https://render.com/articles/how-much-does-cloud-application-hosting-cost-for-small-businesses), [creación de base](https://render.com/docs/postgresql-creating-connecting).

La conexión interna entre servicios de la misma cuenta y región evita el recorrido público. Frente a Neon, esto simplifica proveedores y hace más predecible el costo de cómputo, pero se pierde su ventaja de pagar menos cuando duerme. Sigue siendo PostgreSQL; requiere exportar/restaurar y verificar versión, migraciones, secuencias e integridad, aunque no exige reescribir el producto. [Conexión interna](https://render.com/docs/postgresql-creating-connecting).

En bases pagas, Render ofrece recuperación a un punto del tiempo: tres días en workspace Hobby y siete en Pro o superior. Los backups lógicos exportados se conservan siete días en el servicio. Estas ventanas tampoco cubren por sí solas un problema descubierto al corte siguiente; hace falta retención propia acordada. [Recuperación y backups](https://render.com/docs/postgresql-backups).

**Para este proyecto:** candidato fuerte a comparar con Render + Neon si la factura de Neon crece por actividad de fondo o si reducir proveedores les ahorra mantenimiento. Si Neon funciona dentro de su plan y está bien respaldado, cambiarlo antes del piloto agrega riesgo de migración sin un beneficio confirmado. La base de 256 MB se debe probar con el histórico objetivo; no atribuirle la misma capacidad que el cómputo de Neon por ser ambos PostgreSQL.

### Orden propuesto para evaluar

1. Revisar costo efectivo y estabilidad de **Render pago + Neon**; resolver primero el frontend comercial y la persistencia.
2. Comparar **Render completo** por simplicidad y costo predecible, y **Fly + Neon** por tarifa de cómputo, con una prueba pequeña cada uno sólo si cambian la decisión.
3. Evaluar **Hetzner + Coolify o Compose** si quieren asumir operación o repartir un servidor entre proyectos; confirmar disponibilidad y copias externas.
4. Considerar **Railway** si ya existe Pro compartido o se valora especialmente su operación. Su Hobby no cumple el transporte de correo actual.

Para todos: el mismo ensayo debe cargar el Excel real máximo esperado, consultar historial, ejecutar una campaña de prueba controlada, recibir su respuesta, reiniciar durante trabajo y recuperar sin duplicar. Medir memoria máxima, duración, errores y gasto estimado. Ninguna de estas comparaciones ejecutó ese ensayo ni demuestra un límite de clientes soportados.

## Escenarios para decidir

Referencias antes de impuestos, dominio, casilla de correo, excedentes y trabajo de soporte. No son cotizaciones ni factura actual.

| Escenario | Referencia mensual parcial | Trabajo y decisión |
|---|---|---|
| Mantener Vercel + Render pago + Neon | Base Vercel desde USD 20 + cómputo Render desde USD 7 + Neon/almacenamiento/otros | Menos traslado; calcular costo incremental si los planes se comparten |
| Cloudflare estático + Render pago + Neon | Front estático potencialmente USD 0 + cómputo Render desde USD 7 + Neon/otros | Candidato principal para reducir costo del front si realmente genera un cargo evitable |
| Render estático + Render pago + Neon | Sin tarifa de instancia estática + cómputo Render + Neon/otros | Comparar también: menor cantidad de proveedores que introducir Cloudflare |
| Render estático + backend + PostgreSQL pago con 1 GB | Piso calculado USD 13,30 + extras | Simplifica proveedores; probar recursos y restaurar una copia antes de migrar |
| Front estático + Fly.io + Neon | VM 512 MB de referencia USD 3,19–5,16 según región + Neon/extras | Medir RAM, continuidad de IMAP y correo antes de atribuir ahorro |
| Front estático + Railway Pro + Neon | Mínimo Pro USD 20 acreditado a consumo + Neon/extras | SMTP requiere Pro; no presupuestar el Hobby de USD 5 |
| Cloudflare Workers + almacenamiento + Neon | Workers Paid desde USD 5 + servicios/consumos | Requiere adaptación funcional; no elegir por esa cifra aislada |
| VPS + Neon, o VPS con PostgreSQL | VM de referencia EUR 5,49 + extras + base/copia | Más responsabilidad de operación; validar costo total y recuperación |

El criterio económico debe ser: **factura que realmente se elimina − nuevos consumos − mantenimiento adicional − costo de migración distribuido en el tiempo**. Si una migración ahorra poco pero consume varios días o vuelve más frágil la entrega, no mejora la viabilidad.

## Para el piloto tentativo del 25/09

1. Confirmar planes efectivos, dueño de cuentas y gasto del último mes; no inferirlos desde archivos del repo.
2. Asegurar un backend que pueda conectar SMTP y continuar consultando respuestas cuando nadie esté usando la pantalla.
3. Resolver persistencia del logo si se usa; conservar también fuentes de importación para recuperación y trazabilidad acordadas.
4. Probar con tamaño real de Excel memoria, tiempo de carga, reinicio durante campaña y recuperación. No hacer envíos a terceros sin el ensayo autorizado correspondiente.
5. Definir qué pasa ante fallo parcial y cómo Juan/Julián comprueban lo enviado antes de reintentar. Hosting pago no corrige duplicación o pérdida de tareas en memoria.
6. Probar restauración en una base separada y dejar quién la ejecuta. No cambiar a la vez plataforma, modelo de datos y experiencia de uso justo antes del primer corte.
7. Cambiar sólo el frontend de proveedor si el ahorro efectivo se confirma y hay tiempo para verificar y volver atrás. En caso contrario, programarlo tras el primer uso acompañado.

## Información pendiente del grilling

- Plan y cargo real de Neon, Vercel y Render; servicios compartidos y créditos temporales.
- Presupuesto mensual aceptable para este cliente y quién paga cada cuenta.
- Cuántos clientes/deudores/mails y tamaño máximo del Excel real; crecimiento esperado.
- Demora aceptable para detectar respuestas: inmediata, diez minutos, una hora o actualización manual.
- Horas semanales de Juan y Julián y experiencia operando VPS.
- Uso del logo, archivos que deben conservarse y cuánto historial no se puede perder.
- Tiempo máximo de recuperación aceptable y responsabilidad durante sus ausencias.
- Región efectiva de backend/Neon, memoria usada, salud de conexiones y reinicios observados.

## Alcance de validación

Investigación con fuentes oficiales y revisión de configuración no secreta. Los precios son referencias públicas consultadas en la fecha indicada; algunas fuentes se obtuvieron mediante el índice de búsqueda cuando su contenido Markdown no pudo abrirse directamente. No se verificaron planes contratados, facturas, servidores remotos, credenciales, SMTP/IMAP real, restauraciones ni compatibilidad ejecutada con Workers. Las conclusiones de arquitectura son inferencias explícitas a partir del código y de los límites publicados.
