# Handoff del análisis y la ruta del CRM

Actualizado: 23/09/2026. Proyecto: Mails Nico. A cargo: Juan y Julián.

## Para qué es este handoff

Este documento reúne lo acordado para la entrega inicial y la evolución de la herramienta. El cliente actual necesita cargar una exportación completa de deudores cada quince días, conservar un historial por cliente y enviar recordatorios cuando corresponda. La fecha tentativa del 25/09/2026 puede moverse. El plan es probar el primer envío con pocos destinatarios junto al cliente.

La secuencia que guía el producto es: ahorrar tiempo, evitar deudores sin seguimiento y entender cómo evoluciona la cartera. Se trabaja por ahora para un cliente. No se decidió migrar a Twenty ni cambiar el hosting.

## Acuerdos confirmados

- Durante el piloto, Juan y Julián acompañan los primeros dos cortes.
- Cada Excel debe representar la cartera completa. Una importación actualiza el historial y el dashboard aunque no se manden correos ese día.
- La lista de destinatarios del correo puede ser menor que la cartera importada. La primera campaña será pequeña y se revisará con el cliente antes de ampliarla.
- Si una clave o un monto son ilegibles, el sistema debe señalar las filas para corregirlas. Sigue pendiente decidir si la corrección se hace en Excel y se vuelve a subir.
- Se necesita poner a un cliente en pausa de recordatorios, u “on hold”, sin darlo de baja ni borrar su saldo o historial.
- Si Juan o Julián aceptan un corte equivocado, ellos pueden coordinar la recuperación durante el piloto.
- USD 10 por mes es el presupuesto objetivo de infraestructura. Todavía no se ha demostrado que una configuración con respaldo y seguimiento confiable quepa en ese monto.
- La lista de clientes es bastante estable; se estima que se incorporen uno o dos por mes.
- Según lo acordado previamente, un cliente que desaparece de un nuevo corte completo se considera regularizado conforme a la información del sistema de facturación. Esta regla depende de comprobar que la importación sea completa y válida.

## Lectura del producto actual

La aplicación ya permite administrar el maestro, cargar deudores, preparar recordatorios y revisar respuestas. La base del flujo sirve para el piloto, pero hay riesgos alrededor de cómo se actualiza la cartera:

- Un archivo vacío o una fila de monto descartada puede hacer que el sistema interprete una deuda como saldada.
- La señal de correo “PAGO” puede confundirse con un saldo confirmado por facturación. Recibir un adjunto no prueba por sí solo que el dinero se acreditó.
- Subir dos veces el mismo Excel puede crear ciclos duplicados y cambiar indicadores.
- Un reintento puede usar una dirección o un saldo anterior. Si no sabemos si un correo salió, reenviarlo automáticamente puede duplicar el reclamo.
- La ficha del cliente, la búsqueda y la conversión de respuestas en próximas acciones necesitan mejorar para formar un CRM de seguimiento.

La auditoría ejecutó 44 pruebas existentes del parser, los cortes y el dashboard; todas pasaron con SQLite de prueba. Esas pruebas describen reglas actuales, algunas de las cuales habrá que cambiar para cumplir el producto acordado. Además se reprodujeron ocho casos de aplicación en memoria y un contraejemplo matemático. La evaluación visual independiente encontró oportunidades en búsqueda, ficha del cliente, accesibilidad, claridad de los envíos y gestión de comprobantes.

No se verificaron la conexión real de correo, las facturas de los proveedores, una restauración de producción ni el rendimiento con el Excel máximo del cliente. Los informes distinguen hechos medidos, riesgos inferidos y propuestas.

## Dirección de producto y Twenty

Twenty aporta referencias para fichas, vistas, relaciones, actividad y navegación. La decisión actual es conservar el flujo de cobranza y definir bien los cortes antes de decidir si conviene migrar. Si se evalúa Twenty, la prueba debe preservar el recorrido Excel → revisión → envío → seguimiento y medir el esfuerzo para adaptarlo al negocio.

La mejora posterior debe darle al operador una ficha transversal, búsqueda, motivos de exclusión y una cola clara de próximos pasos. Multiempresa y funciones comerciales genéricas quedan fuera del alcance actual.

## Hosting y costos

El usuario confirmó que hoy utilizan Neon para datos, Vercel para el frontend y Render para el backend. Los planes activos y las facturas no se verificaron. La investigación revisó Cloudflare Pages, Render completo, Fly.io, Railway y VPS con Coolify; no se cambió ningún servicio.

El backend debe permanecer disponible para revisar el correo y usa SMTP. Servir archivos estáticos en Cloudflare puede reducir el costo del frontend, pero no reemplaza el backend que envía y busca respuestas. Railway exige su plan Pro para SMTP. El VPS puede reducir la tarifa de cómputo, pero traslada la operación y la recuperación a Juan y Julián.

Antes de elegir, hay que comprobar costos reales, polling de correo, memoria, tamaño del Excel, archivos adjuntos y restauración. USD 10 queda como límite de referencia, no como costo garantizado. El detalle está en [13_HOSTING_Y_COSTOS.md](13_HOSTING_Y_COSTOS.md) y [14_ALTERNATIVAS_BARATAS_Y_EXPERIENCIAS.md](14_ALTERNATIVAS_BARATAS_Y_EXPERIENCIAS.md).

## Grilling y decisiones abiertas

El registro completo de preguntas y respuestas está en [12_GRILLING_ENTREGA_Y_EVOLUCION.md](12_GRILLING_ENTREGA_Y_EVOLUCION.md). Las preguntas 1–14 están contestadas y documentadas. Falta conversar la ronda 3, preguntas 15–23, sobre:

1. Corregir filas inválidas fuera de la aplicación y volver a subir el archivo.
2. Reactivar manualmente a los clientes que están en pausa.
3. Alcance inicial de monto mínimo, pausas y selección de destinatarios.
4. Qué pasa con los correos pendientes cuando se carga otro corte.
5. Cómo tratar un envío cuyo resultado es incierto.
6. Resolver conflictos entre un correo corregido manualmente y el maestro.
7. Demora aceptable para detectar respuestas entrantes.
8. Horario y tiempo de soporte de Juan y Julián.
9. Cómo registrar la fecha del corte y la fecha de carga.

Las preguntas están pendientes; las respuestas recomendadas en el registro son propuestas y no se consideran decisiones del usuario.

## Ruta de continuidad

1. Completar las respuestas Q15–Q23 en el grilling.
2. Confirmar una exportación real representativa, responsables y horario de soporte, costos y procedimiento de restauración.
3. Acordar criterios del piloto y límites seguros para detener o corregir un envío.
4. Una vez fijado el destino, crear con Wayfinder un mapa de decisiones y separar trabajo del piloto y mejoras futuras.
5. Crear tickets de implementación cuando los criterios de aceptación estén claros.

## Archivos de referencia

- [00_INDICE.md](00_INDICE.md): catálogo de los análisis, reglas, criterios, evidencias y comparación de infraestructura.
- [12_GRILLING_ENTREGA_Y_EVOLUCION.md](12_GRILLING_ENTREGA_Y_EVOLUCION.md): entrevista, respuestas y preguntas pendientes.
- [ANALISIS_PRODUCTO_CRM.md](../docs/ANALISIS_PRODUCTO_CRM.md): auditoría de producto y UI.
- [MAPA_REPOSITORIO.md](../docs/MAPA_REPOSITORIO.md): mapa del repositorio.
- [CONTEXT.md](../CONTEXT.md): glosario del dominio.
- `.lavish/`: auditoría visual y prototipos anteriores.
- `evidencias/`: reproducciones aisladas de los cortes.

## GitHub y estado de la copia

El repositorio de origen es `Juanrocod/Mails-nico`. Se creó el fork personal [BlackSinapsis/Mails-nico](https://github.com/BlackSinapsis/Mails-nico) y se publicó la rama `codex/handoff-analysis` mediante la CLI. La rama remota coincide con la local al momento de esta actualización. Incluye el análisis, el registro del grilling, las evidencias, la auditoría visual y este handoff en Markdown.
