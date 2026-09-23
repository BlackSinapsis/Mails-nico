# Grilling: entrega inicial y evolución de la herramienta

Estado: conversación abierta. Rondas 1 y 2 respondidas; fecha flexible aclarada. Se registra aprobación de señalar y corregir errores de archivo; la aplicación total del bloqueo se explicita en la siguiente ronda. Capacidad horaria de soporte pendiente. Las recomendaciones no se consideran aceptadas antes de su respuesta.

## Intención confirmada

Separar una primera entrega utilizable por el cliente de un plan posterior de mejora continua. Fecha tentativa actual: 25/09/2026, todavía a definir; reemplaza la referencia inicial a “la semana próxima”. Conservar el objetivo de cortes de deuda, historial y mails; evaluar Twenty y mejoras de UI sin sobredimensionar la herramienta. Primero discutir a fondo las decisiones, luego organizarlas con Wayfinder.

## Método

Se usan grilling y domain-modeling para precisar decisiones y vocabulario, y Wayfinder para organizar el mapa después de acordar su destino. Se pregunta por rondas: una respuesta abre las decisiones dependientes. Las recomendaciones no sustituyen respuestas humanas.

Wayfinder organizará decisiones, investigaciones y prototipos; no confundirá ese mapa con tickets de implementación. Por ahora se conserva el registro en Markdown en el proyecto. No se publicaron issues ni se decidió una migración.

## Hechos disponibles antes de preguntar

- Los documentos históricos plantean un operador y aproximadamente 600 consorcios cada 15 días. El dataset de 50 clientes es ficticio, no el volumen contratado confirmado para este piloto.
- `docs/PENDIENTES.md` registra pruebas históricas hasta 60 correos; no demuestra una campaña de 600 en el entorno de entrega.
- El mismo documento dice que las columnas fueron confirmadas con archivos reales y que la clave tiene ocho dígitos. Otros textos siguen diciendo “a confirmar”. No hay un export real reciente disponible entre los Excel examinados.
- Hay despliegue previsto Vercel/Render/Neon, pero divergencia documental entre Render Free y Starter; no se inspeccionó la configuración viva del hosting.
- Existe un backup SQLite manual local. No hay evidencia de restauración del entorno de entrega en la revisión.
- La auditoría previa reprodujo riesgos de importación, duplicación y estado de pago; la existencia de pantallas usables no resuelve esos riesgos.

Estas son evidencias y límites. No se le pedirá al usuario que investigue hechos que podamos consultar nosotros.

## Árbol de decisiones provisional

- Destino: acordar una entrega inicial viable y una ruta de evolución.
  - Resultado esperado del primer uso → capacidades mínimas y aceptación.
  - Grado de acompañamiento → alcance de prueba, recuperación y excepciones manuales.
  - Fecha y rigidez del compromiso → recortes y decisión de salida.
  - Capacidad de soporte → operación, responsables y sostenibilidad.
  - Regla ante fallos importantes → bloqueantes y funciones postergables.
  - Beneficio prioritario → métricas y orden de mejoras.
  - Horizonte del producto → valor de adoptar Twenty y costo de mantenimiento.
- Después: contrato vigente del export, datos reales, capacidad de correo, restauración, UX de excepciones y definición de funcionalidades del piloto.
- Más adelante: prueba comparativa de plataforma, mejoras de CRM, mapa de dependencias y tickets ejecutables.

Este árbol está abierto; no declara resueltas las ramas posteriores.

## Ronda 1 — Definir qué estamos entregando

### Q1 — Resultado de la primera entrega

¿Qué tiene que poder completar el cliente en su primer uso para que consideres cumplida la entrega?

Recomendación: cargar su Excel real, revisar cambios y destinatarios, enviar una campaña y consultar su resultado e historial. Dashboard limitado a indicadores fiables; tareas avanzadas y rediseño amplio quedan fuera del compromiso inicial.

Respuesta: “ok”. Se acepta el flujo propuesto: Excel real, revisión, campaña, resultado e historial; indicadores fiables y mejoras amplias posteriores.

### Q2 — Autonomía inicial

¿Querés un piloto acompañado en las primeras dos cargas o una entrega que el cliente opere solo desde el primer día?

Recomendación: piloto acompañado durante dos cortes, con responsable explícito y revisión de la primera campaña. El acompañamiento no sustituye los controles que evitan corrupción de datos o destinatarios equivocados.

Respuesta: “sí”. Se registra como aceptación de la recomendación de piloto acompañado durante las primeras dos cargas.

### Q3 — Fecha y compromiso

¿Qué día exacto querés entregar y es una fecha comprometida con el cliente o una meta interna?

Recomendación: fijar una fecha de primera sesión operativa y condicionar el envío real a criterios de salida acordados. No prometer una plataforma nueva para cumplir esta fecha.

Respuesta: “a definir, probablemente el 25/9”. Fecha tentativa, no compromiso firme. No está resuelta todavía la regla de salida ante un problema importante.

### Q4 — Capacidad de operación y soporte

¿Quién podrá acompañar al cliente y atender problemas durante el primer mes, y cuántas horas semanales reales puede dedicar?

Recomendación: un responsable identificado, acompañamiento de las primeras dos cargas y un canal de incidencias con tiempo de respuesta acordado. No presupuestar disponibilidad permanente implícita.

Respuesta: Juan y el usuario se harán cargo. Confirma Neon para datos, Vercel para frontend y Render para backend. Solicita estudiar optimización de costos y alternativas como Cloudflare. Horas de soporte disponibles y tiempo de respuesta todavía no especificados; no asumir disponibilidad ilimitada.

### Q5 — Límite de salida

Si llega la fecha y sigue existiendo un caso que puede marcar mal una deuda o duplicar un recordatorio, ¿preferís postergar el envío real o entregar un piloto más limitado donde ese recorrido esté deshabilitado?

Recomendación: recortar funciones solo si el recorrido riesgoso queda efectivamente bloqueado; si el problema afecta al flujo central que se va a usar, postergar su activación. Un aviso “usalo con cuidado” no corrige una importación que descarta deudas.

Respuesta: “no importa”. Ambigua: no se considera autorización para liberar errores conocidos ni confirmación de que la fecha sea flexible. Se aclara en Q8.

### Q6 — Beneficio que manda

Para el primer mes, ¿cómo ordenarías ahorrar tiempo preparando/envíando mails, evitar deudores sin seguimiento y entender la evolución de la cartera?

Recomendación: preparar/envíar correctamente con menos trabajo, conservar historial fiable y después profundizar las herramientas de seguimiento. El orden es una propuesta a contrastar con el dolor principal del cliente.

Respuesta: 1) ahorrar tiempo; 2) evitar falta de seguimiento; 3) saber cómo evoluciona la cartera. Este orden prevalece sobre la recomendación inicial del asistente.

### Q7 — Horizonte del producto

¿Estamos construyendo una herramienta para este cliente o hay intención concreta de ofrecerla a otras empresas en los próximos meses?

Recomendación: optimizar primero para este cliente y documentar qué sería reutilizable. Incorporar necesidades de varias empresas solo si existe un compromiso o plan comercial concreto que lo justifique.

Respuesta: “por ahora este cliente”. Multiempresa y producto comercial para terceros no forman parte del alcance actual.

## Decisiones consolidadas de la ronda 1

- Entrega inicial del recorrido actual, con indicadores fiables; profesionalización posterior.
- Piloto acompañado durante dos cortes; soporte de Juan y el usuario.
- Fecha tentativa 25/09/2026, a definir.
- Prioridades: ahorro de tiempo → seguimiento → evolución de cartera.
- Por ahora un solo cliente; sin requisitos de multiempresa.
- Infraestructura actual confirmada por el usuario: Neon, Vercel y Render. Investigación de costos autorizada; ningún cambio de proveedor decidido.

## Ronda 2 — Límites prácticos del piloto

### Q8 — Aclarar el límite de salida

Cuando dijiste “no importa”, ¿te referías a que podemos mover la fecha o recortar el alcance si queda un problema importante?

Recomendación: mantener esa flexibilidad sin liberar un recorrido que pueda perder deudas o duplicar reclamos.

Respuesta recibida: hay flexibilidad con la fecha, sin inconveniente en moverla. Aclara el “no importa” de Q5; no expresa aceptación de defectos de integridad.

### Q9 — Primera campaña real

¿La primera campaña acompañada debe cubrir todos los destinatarios elegibles o empezar con un lote chico y continuar después de verificarlo?

Recomendación: importar siempre la cartera completa; empezar el envío con un lote acotado y continuar tras revisar el resultado. Seleccionar destinatarios no debe convertir el corte en parcial.

Respuesta recibida: sí, prueba inicial con pocos mails, acordada y acompañada con el cliente. Existe confianza para hacer ensayos con él. Cantidad y casillas se elegirán para esa sesión; esto no autoriza enviar correos reales ahora.

### Q10 — Archivo con errores

Si una fila trae clave o monto inválido, ¿preferís bloquear la aceptación del archivo hasta corregirlo, aunque retrase los mails?

Recomendación: conservar el último corte válido, explicar las filas problemáticas y no aplicar regularizaciones desde un archivo incompleto.

Respuesta recibida: sí a identificar y señalar cuáles filas fallaron o no cumplen y corregirlas. El usuario enfatiza visibilidad y corrección. Se explicitará que el corte completo queda sin aplicar hasta resolver errores de clave/monto; no se interpreta “flaguear” como permiso para descartar silenciosamente deudores. Dónde se corrige se decide en Q15.

### Q11 — Actualizar sin enviar

¿Debe poder guardar un corte y actualizar historial/dashboard aunque decida no enviar mails ese día?

Recomendación: sí; una continuación rápida puede llevarlo a preparar mails, pero actualizar saldos no debería obligar a enviarlos.

Respuesta recibida: sí. Debe permitir importar, actualizar historial y consultar dashboard sin enviar. El usuario quiere gestión de clientes con sentido de CRM, manteniendo el correo como función central. Esta separación está acordada para el producto; no está implementada por esta conversación.

### Q12 — Comprobante o promesa antes del siguiente corte

Si el cliente manda un comprobante o promete pagar y sigue figurando en el siguiente Excel, ¿el operador debe poder pausar su recordatorio hasta revisar el caso?

Recomendación: pausa manual con motivo y fecha de revisión; conservar el saldo del Excel. No considerar un adjunto prueba automática de pago ni pausar indefinidamente.

Respuesta recibida: sí a una pausa manual u “on hold”, distinta de dar de baja. Debe gestionarse por cliente junto con filtros de monto u otros criterios de envío. La lista es estable, con aproximadamente uno o dos clientes nuevos por mes. No se dieron por aprobadas reactivación automática, fecha obligatoria ni todas las opciones de filtrado: se precisan en la ronda 3.

### Q13 — Corregir un corte equivocado

Para el piloto, ¿la corrección de un corte ya aceptado debe estar disponible para el operador o puede quedar a cargo de ustedes?

Recomendación: empezar con recuperación asistida por Juan y el usuario, con copia previa y procedimiento verificado; no exigir un editor completo de historia para esta entrega. La corrección debe conservar trazabilidad y no repetir mails.

Respuesta recibida: sí, corregir una importación ya aceptada puede quedar a cargo de Juan y el usuario para el piloto. La herramienta de autoservicio se evaluará después.

### Q14 — Presupuesto de infraestructura

¿Qué tope mensual de alojamiento consideran razonable para este cliente, sin contar desarrollo y soporte?

Recomendación: comparar costo total y mantenimiento, no perseguir costo cero. El importe y la conveniencia de cambiar se decidirán con los escenarios de hosting; no hay techo asumido.

Respuesta recibida: USD 10 por mes para infraestructura. Espera login adecuado, dashboard, backend sólido, rapidez e integridad. Se registra como presupuesto objetivo, no como capacidad o calidad demostradas por ese importe. Los escenarios de USD 13,30 y superiores no satisfacen el presupuesto nominal y quedan como comparadores, no recomendaciones aprobadas. Aún no se eligió proveedor ni se verificó costo total con copias y consumo de Neon.

## Decisiones consolidadas de la ronda 2

- Fecha flexible; el 25/09 sigue siendo tentativa.
- Primera campaña con un lote pequeño acompañado por el cliente; cartera importada completa.
- Filas inválidas visibles y corregibles; pendiente precisar el mecanismo de corrección antes de aceptar.
- Importación, historial y dashboard independientes del envío de mails.
- Pausa manual por cliente, separada de baja y saldo; alcance y levantamiento pendientes.
- Filtros de envío útiles, sin constructor genérico aprobado.
- Recuperación de cortes erróneos asistida por Juan y el usuario en el piloto.
- Presupuesto objetivo de infraestructura: USD 10/mes.
- Maestro estable con aproximadamente uno o dos clientes nuevos mensuales.

## Ronda 3 — Reglas operativas del primer uso

### Q15 — Corregir filas inválidas

¿Te sirve que una clave o monto inválido impida aplicar el corte y que el operador corrija el archivo en Excel y lo vuelva a subir?

Recomendación: listado de errores por fila y columna, descargable; conservar el corte anterior hasta validar todo. Posponer edición de celdas dentro de la aplicación. Respuesta: pendiente.

### Q16 — Levantar una pausa

¿Los correos de un cliente en pausa deben reactivarse sólo cuando el operador lo indique, aunque ya haya pasado una fecha de revisión?

Recomendación: levantar manualmente; recordar las revisiones vencidas y conservar la pausa al importar archivos posteriores. Respuesta: pendiente.

### Q17 — Filtros de la primera entrega

¿Alcanza para el piloto con un monto mínimo general, pausas individuales y selección de destinatarios para la campaña?

Recomendación: ese conjunto inicial, mostrando el motivo de cada exclusión; dejar umbrales particulares y filtros combinados avanzados para después. Nunca modificar el saldo o historial por excluir de un envío. Respuesta: pendiente.

### Q18 — Nuevo corte con envíos pendientes

Si se acepta un nuevo Excel antes de terminar la campaña anterior, ¿deben quedar bloqueados los recordatorios pendientes basados en los saldos viejos?

Recomendación: sí; conservar su registro y preparar los próximos mails con la cartera vigente. El lote de prueba y su continuación utilizan el mismo corte mientras no haya otro aceptado. Respuesta: pendiente.

### Q19 — Envío con resultado incierto

Si se interrumpe la conexión después de intentar un correo y no se sabe si salió, ¿aceptás que quede para revisión manual en vez de repetirse automáticamente?

Recomendación: separar fallos seguros de resultado desconocido; revisar los desconocidos antes de reintentar. Respuesta: pendiente.

### Q20 — Cambios manuales y maestro posterior

Si se corrige un email en la ficha y después se importa un maestro que todavía trae el email viejo, ¿debe pedirse resolver la diferencia antes de reemplazarlo?

Recomendación: conservar el contacto actual y mostrar el conflicto. Las pausas y bajas no deben perderse al actualizar el maestro. Respuesta: pendiente.

### Q21 — Demora del seguimiento automático

¿Qué demora máxima es aceptable para que aparezca una respuesta recibida por correo?

Recomendación: diez minutos, como referencia actual, con actualización manual cuando se necesite; evaluar treinta o sesenta minutos sólo si esa demora es aceptable y el ahorro se demuestra. Respuesta: pendiente.

### Q22 — Disponibilidad para soporte

¿Qué horario y tiempo de respuesta pueden comprometer Juan y vos si una importación o campaña queda bloqueada?

Recomendación: acompañar las campañas del piloto en horario acordado y responder dentro de un día hábil fuera de esas sesiones, si su disponibilidad lo permite. No se promete ese servicio al cliente sin respuesta. Respuesta: pendiente.

### Q23 — Fecha de los datos

Si se carga hoy un archivo exportado hace varios días, ¿la evolución de cartera debe usar la fecha de esos datos y conservar aparte la fecha de carga?

Recomendación: sí; confirmar fecha del corte al importar y tratar archivos de fecha anterior como correcciones asistidas, no como nueva cartera vigente. Respuesta: pendiente.

## Ramas siguientes todavía abiertas

Capacidad y horario de soporte, volumen del piloto, export vigente, fallos y recuperación de campañas, pruebas de restauración, pendientes de respuesta y alcance concreto de UI. Las preguntas que dependan de la evaluación de hosting o de respuestas de la ronda 2 esperan esa evidencia. La elección Twenty/aplicación actual sigue abierta.

## Investigación adicional solicitada: infraestructura económica

El usuario pidió consultar Twitter o foros para comparar opciones económicas de frontend, backend y base de datos compatibles con la carga. Se amplió la investigación en [13 — Hosting y costos](13_HOSTING_Y_COSTOS.md) y [14 — Alternativas y experiencias](14_ALTERNATIVAS_BARATAS_Y_EXPERIENCIAS.md). Se consultaron foros públicos y fuentes oficiales; no se cambiaron servicios. Esta solicitud no responde las preguntas de la ronda 2 ni aprueba una migración. Quedan por confirmar gasto actual, presupuesto, consumo real y disposición a operar un servidor propio.

## Continuidad y handoff

El resumen [HANDOFF_PRODUCTO_Y_RUTA.md](HANDOFF_PRODUCTO_Y_RUTA.md) reúne la intención, acuerdos, evidencia, preguntas Q15–Q23 y próximos pasos al 23/09/2026. El inventario completo de documentos está en [00_INDICE.md](00_INDICE.md).

Fork solicitado en GitHub personal `BlackSinapsis`: pendiente de completar inicio de sesión. `gh auth status` informa que el token local venció; Brave muestra el formulario de login de GitHub. Los archivos siguen guardados en este proyecto. Aún no se ha creado el fork ni enviado la documentación allí.
