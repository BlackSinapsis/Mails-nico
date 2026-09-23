# Alternativas económicas: experiencias, carga y recomendación

> Actualización del grilling: el usuario fijó un presupuesto objetivo de infraestructura de **USD 10/mes**. Los escenarios superiores se conservan como comparación; no cumplen ese objetivo ni fueron aprobados. Falta verificar una configuración completa dentro del presupuesto con consumo real, archivos y recuperación.

Consulta: 13/09/2026. Complementa [13_HOSTING_Y_COSTOS.md](13_HOSTING_Y_COSTOS.md). Investigación, sin contratación, migración ni cambios en producción. La decisión sigue abierta dentro del [grilling](12_GRILLING_ENTREGA_Y_EVOLUCION.md).

## Resultado para este proyecto

La primera opción a presupuestar es **frontend estático gratuito en Cloudflare o Render, backend Python en Render pago y PostgreSQL en Neon**. Conserva el funcionamiento del correo y permite investigar el gasto sin convertir el piloto en una reescritura. La segunda es concentrar frontend, backend y PostgreSQL en Render. La tercera es un VPS con Coolify si Juan y Julián quieren asumir su operación y aprovecharlo también para otros proyectos.

Son recomendaciones de ajuste al producto, no resultados de una prueba de rendimiento. No sabemos aún planes efectivos, facturas, memoria máxima, región ni tamaño de archivos reales. El objetivo de unos 600 consorcios procede de `docs/adr/0002-envio-automatico-smtp.md`; debe confirmarse para este piloto.

“Hosting” comprende dónde vive cada parte: pantalla, servidor de aplicación, base de datos y, si conservamos originales y comprobantes, almacenamiento de archivos. El correo utiliza además la casilla del cliente. Un precio anunciado para una parte no es el precio de todo el sistema.

## Qué aparece en los foros

Se consultaron discusiones públicas e índice de búsqueda; no se publicaron preguntas ni se contactó a nadie. Las búsquedas dirigidas a X no aportaron publicaciones suficientemente útiles y verificables para esta comparación; la evidencia comunitaria utilizada es de Reddit. No se inspeccionó una sesión de Twitter en Brave. Es una muestra cualitativa, no una medición de popularidad o cuota de mercado. Los detalles técnicos y tarifas se contrastan en el documento 13 con fuentes del proveedor.

| Conversación | Experiencia o recomendación observada | Cómo influye aquí |
|---|---|---|
| [FastAPI: alternativas de hosting, agosto de 2025](https://www.reddit.com/r/FastAPI/comments/1mfacje) | Participantes cuentan despliegues con Railway mediante Docker y con Hetzner/Coolify; también mencionan Render y Koyeb | Los contenedores administrados y el VPS son candidatos razonables para investigar; no se adopta la afirmación del autor sobre incompatibilidad general con Vercel |
| [React + FastAPI + PostgreSQL, junio de 2025](https://www.reddit.com/r/webdev/comments/1ligsc4/what_would_be_the_best_hosting_for_me/) | Se proponen Cloud Run, VPS y separar frontend estático de base administrada; un participante describe uso de Neon | Separar componentes puede ahorrar sin cambiar la aplicación. Un servicio que duerme requiere revisar nuestras tareas de correo |
| [PostgreSQL con Hetzner/Coolify, marzo de 2026](https://www.reddit.com/r/coolify/comments/1rxb5gd/selfhosting_postgres_on_hetzner_coolify_for_a_pos/) | La conversación se concentra en copias, recuperación y la responsabilidad de alojar base y aplicación juntas | El costo de un VPS debe incluir quién recupera los datos, no sólo el alquiler |
| [La misma consulta en Hetzner, marzo–junio de 2026](https://www.reddit.com/r/hetzner/comments/1rxb4zc/selfhosting_postgres_on_hetzner_coolify_for_a_pos/) | Algunos usuarios proponen separar la base o guardar copias fuera del servidor | Es la misma pregunta publicada en otra comunidad; no se cuenta como evidencia independiente de adopción |
| [Experiencia de cuatro meses con Supabase autogestionado, abril de 2026](https://www.reddit.com/r/Supabase/comments/1sv3vrw/selfhosting_supabase_on_a_12mo_hetzner_box_4/) | El autor declara ahorro, pero describe almacenamiento, copias y componentes adicionales; otros preguntan por recuperación | Un relato de ahorro puede esconder trabajo operativo. No reutilizar su factura ni sus precios antiguos como presupuesto nuestro |

La señal útil es la elección entre pagar por operación administrada o encargarse del servidor. Ningún comentario demuestra que nuestra campaña real funcione con 512 MB, que el proveedor permita SMTP en un plan concreto o que se pueda recuperar el historial después de un error.

## Qué carga hay que dimensionar

Estimaciones aritméticas para orientar la prueba, no mediciones:

| Dimensión | Ejemplo | Implicación |
|---|---|---|
| Historial | 600 clientes × 24 cortes/año = 14.400 observaciones/año; cada 15 días exactos serían aproximadamente 24–25 cortes | El número de filas por sí solo no justifica una arquitectura compleja; faltan tamaño de fila, índices, mensajes y crecimiento |
| Envíos | 600 destinatarios a 5 cada 30 segundos ≈ una hora, más latencia y fallos | El trabajo debe sobrevivir al cierre de pantalla y poder recuperarse de un reinicio |
| Seguimiento | Un chequeo cada 10 minutos = 144 oportunidades diarias; 4.320 en 30 días por bucle activo | Aunque nadie entre, sigue habiendo actividad. Varios procesos también consultan la base para coordinarse |
| Archivos originales | Supuesto de 2 Excel/mes de 5 MB cada uno = 120 MB/año | Conservar originales puede ser barato; este tamaño no es el del archivo real |
| Adjuntos | Depende de cuántos mensajes llegan y del peso de los archivos | Deben dimensionarse aparte de las filas de deuda; no asumir que ocupan poco |

El watcher actual busca mensajes de una ventana y descarga su contenido completo mediante `RFC822` antes de comprobar si corresponde a un envío (`backend/app/services/imap_watcher.py`). Por tanto, puede volver a transferir mensajes y adjuntos entre consultas. Propuesta posterior a validar: seguimiento incremental por identificador de mensaje, lectura de encabezados antes del cuerpo y una política clara de revisiones tardías. No reducir controles de seguimiento sólo para evitar consumo.

El backend también consulta PostgreSQL desde `/health` (`backend/app/main.py`). **Inferencia a medir:** un monitor frecuente y los chequeos de correo pueden impedir que Neon aproveche su suspensión automática. Optimizar esas consultas puede ser más rentable que cambiar de proveedor. Hay que conservar una comprobación real de salud de la base, aunque se separe de la comprobación de que el proceso está vivo.

## Base de datos y archivos: alternativas concretas

**Neon:** ya utiliza PostgreSQL y evita una migración de datos. La tarifa publicada incluye Free con 0,5 GB y 100 CU-horas mensuales por proyecto. En Launch, el cómputo publicado es USD 0,106/CU-hora y almacenamiento USD 0,35/GB-mes. La referencia consultada mediante índice puede diferir de planes heredados; debe contrastarse con la cuenta. [Precios de Neon](https://neon.com/pricing).

**Supabase:** agrega autenticación, almacenamiento y otras herramientas. Su Free publica 500 MB de base y pausa tras una semana inactiva; Pro parte de USD 25/mes con un primer proyecto y copias diarias retenidas siete días, sujeto a recursos y excedentes. Mi evaluación: migrar sólo PostgreSQL desde Neon no demuestra ahorro; adquiere interés si elegimos utilizar también esas funciones. [Precios oficiales](https://supabase.com/pricing).

**Cloudflare D1:** usa semántica SQL de SQLite y acceso por API/Workers. No es cambiar la dirección de conexión de Neon: habría que adaptar acceso a datos, migraciones y la coordinación que hoy usa PostgreSQL. Que el proyecto funcione con SQLite local tampoco demuestra compatibilidad con D1. No lo elegiría como recorte de costos para el piloto. [Descripción oficial](https://developers.cloudflare.com/d1/).

**Cloudflare R2:** candidato para originales, logo y eventuales comprobantes; puede usarse desde el backend Python existente. Standard incluye 10 GB-mes, un millón de operaciones de escritura/listado y diez millones de lectura mensuales; excedentes de almacenamiento a USD 0,015/GB-mes y operaciones aparte. No cobra salida directa a internet. Los archivos de deuda deben permanecer privados, con acceso desde la aplicación. R2 guarda objetos; no reemplaza la base de clientes ni crea copias automáticamente. [Tarifas](https://developers.cloudflare.com/r2/pricing/), [ejemplo oficial con Python](https://developers.cloudflare.com/r2/examples/aws/boto3/).

**PostgreSQL en el VPS:** concentra la factura, pero también la recuperación. Coolify facilita despliegues; su propia copia de configuración no incluye automáticamente datos de aplicaciones, bases y volúmenes. Necesitamos copias de la aplicación y restauración por separado. [Alcance oficial de las copias de Coolify](https://coolify.io/docs/core/backup-and-recovery/instance-backup).

## Presupuesto ilustrativo de la opción con Neon

Cloudflare puede servir este frontend estático sin cargo por solicitudes estáticas; las funciones se facturan aparte. Render publica una instancia web de 512 MB a USD 7/mes. Falta probar si ese tamaño alcanza. [Cloudflare](https://developers.cloudflare.com/pages/functions/pricing/), [Render](https://render.com/pricing).

| Supuesto | Base mensual de referencia |
|---|---:|
| Front estático sin cargo + Render de USD 7 + Neon dentro de Free | USD 7 antes de extras |
| Mismo front/backend + Neon Launch con 90 CU-horas y 0,5 GB | USD 16,72 antes de extras |
| Mismo front/backend + Neon Launch con 180 CU-horas y 0,5 GB | USD 26,26 antes de extras |

Las dos filas pagas calculan 7 + CU-horas × 0,106 + 0,5 × 0,35; no restan el cupo Free de un plan diferente. 180 CU-horas equivalen a 0,25 CU continuamente durante 720 horas; 90, a la mitad del tiempo. Son escenarios hipotéticos. No incluyen tarifa de workspace si aplica, recuperación adicional, ramas, disco del logo, transferencia excedente, impuestos, dominio, casilla ni trabajo de soporte. R2 podría mantenerse dentro del cupo incluido en el ejemplo de archivos, pero requiere integración y control de consumo. No llamar “USD 7 todo incluido” a este presupuesto.

## Qué llevar a Wayfinder

La decisión de hosting es una rama separada de la decisión de CRM. Se puede mejorar UI sin migrar hosting y abaratar el frontend sin adoptar Twenty.

Antes de cerrar esta rama, obtener el gasto incremental real de los tres proveedores, el presupuesto mensual y la disposición de Juan/Julián a administrar un VPS. Comparar dos o tres configuraciones completas con igual capacidad de recuperación y seguimiento. Luego hacer una prueba aislada con el Excel representativo, varios cortes acumulados, envío a casillas de prueba autorizado, respuesta, adjunto y reinicio durante campaña. Medir memoria, tiempos, consumo de base y transferencia. El resultado debe incluir vuelta atrás y costo de mantenimiento.

Para el piloto tentativo del 25/09: conservar Python y el flujo de correo; evaluar el frontend como cambio acotado. Mover también la base o adoptar Workers exige una ventaja demostrada y una prueba de restauración. El ahorro objetivo es en factura **y tiempo de ustedes**, coherente con la prioridad expresada por el usuario.
