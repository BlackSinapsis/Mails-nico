# Hoja de ruta y decisiones previas a los tickets

Fecha: 13/09/2026. No son tickets creados ni un cronograma comprometido. Orden por dependencias y reducción de errores de negocio.

## Qué quedó confirmado por el usuario

- Maestro persistente separado del listado periódico de deudores.
- Excel completo desde facturación aproximadamente cada 15 días.
- Ausencia en un corte posterior válido se interpreta como deuda regularizada.
- Historial por cliente y dashboard que siga siendo correcto con el paso del tiempo.
- Conservar envío de mails y facilidad de uso.
- Considerar capacidades y estética de Twenty, evitando un alcance excesivo.
- Documentar antes de crear tickets y comenzar una migración.

## Entregas recomendadas

| Entrega | Problema que resuelve | Incluye | Entrada necesaria | Condición de salida |
|---|---|---|---|---|
| E0. Contrato del export | Ambigüedad de filas, claves y montos | Muestra real anonimizada o descripción fiel, fecha y ámbito, totales | Confirmar saldo por cliente vs factura | Documento 01 validado con ejemplos representativos |
| E1. Cortes confiables | Historia falsa por repetición, archivo viejo o inválido | Borrador, errores por fila, fecha/versión, aceptación atómica e idempotente | E0 | AC de importación y continuidad prioritarios aprobados |
| E2. Dashboard e historial | Indicadores contradictorios y datos sin fecha | Fórmulas de 04, episodios observados, conteos correctos y vista por corte | E1 | Totales conciliados y casos AC34–40 aprobados |
| E3. Correo fiable | Envíos obsoletos, estados mezclados y excepciones sin salida | Campañas separadas, intentos persistentes, comprobantes, recuperación y bajas | E1 y política de envío | AC24–33 aprobados para funciones liberadas |
| E4. CRM mínimo e interacción | Falta de búsqueda y próxima acción | Contactos, ficha, notas, tareas, promesas, vistas guardadas y accesibilidad | E2 y necesidad operativa validada | Un operador resuelve los casos sin reconstruir contexto entre pantallas |
| E5. Decisión de plataforma | Riesgo de migrar por estética | Prueba comparativa A/B del documento 06 | E0–E2 definidos; versión Twenty fijada | Registro de decisión con evidencia, costo y plan de vuelta atrás |
| E6. Migración gradual, si corresponde | Pérdida de historia y doble operación | Transformación verificada, comparación, piloto y único emisor | Decisión E5 | Conciliación de datos y criterios AC; operación y restauración probadas |

E5 puede investigarse en paralelo con especificar E1–E4; no debe sustituir el acuerdo de reglas. No es necesario implementar todo dos veces: antes de construir contactos/tareas en A, usar la prueba de ajuste para decidir si conviene hacerlo sobre Twenty.

## Alcance mínimo propuesto

Una cartera, una moneda, cortes completos, un canal email, asistente de importación, historial y dashboard fiables, búsqueda y ficha, pendientes de contacto/comprobante, notas y tareas sencillas. Asignación de responsable cuando haya más de una persona. Promesas con fecha e importe cuando se incorpore gestión estructurada.

Fuera del primer alcance: ventas y oportunidades, marketing masivo, IA autónoma, facturación propia, conciliación bancaria automática, multiempresa, WhatsApp, mantenimiento técnico integral, edición libre de dashboards por el operador y builder genérico de automatizaciones.

## Decisiones abiertas, con propuesta provisional

| ID | Decisión | Propuesta inicial | Qué cambia si se responde distinto |
|---|---|---|---|
| D01 | Una fila por cliente o factura | Saldo agregado por cliente | Si son facturas, cambia importación/modelo y se habilita antigüedad real por vencimiento |
| D02 | Fecha y total de control disponibles | Pedir fecha al cargar y comparar total del export | Si existe metadata confiable, leerla y evitar carga manual |
| D03 | Moneda y ámbito | Una cartera en ARS | Si hay varios, separar comparaciones y evitar sumas mezcladas |
| D04 | Corrección del corte aceptado | Versionar sin borrar historia; sin mails retroactivos | Define permisos y recálculo de transiciones |
| D05 | Subir historia fuera de orden | Rechazar en flujo normal; herramienta separada si hace falta | Agrega recálculo y pruebas de cobertura |
| D06 | Regla de no reenviar cuando hay promesa/comprobante | Pausa explícita con motivo, vencimiento y revisión | Afecta elegibilidad; no modifica saldo |
| D07 | Cambios del maestro | Mostrar conflictos con correcciones manuales; conservar bajas | Define prevalencia de datos y auditoría |
| D08 | Usuarios y administradoras | Un operador inicial; relaciones simples | Más equipo aumenta valor de Twenty, roles y asignación |
| D09 | Momento de envío tras aceptar corte | Preparar y confirmar campaña aparte con continuación rápida | Puede simplificarse la UI sin acoplar las operaciones |
| D10 | Objetivo CRM más allá de cobranza | Solo contactos, tareas y atención relacionada | Ventas/servicio técnico justificarían reevaluar plataforma y alcance |

No se vuelve a preguntar si la ausencia significa regularización: ya está confirmado para cortes completos. Las decisiones restantes son detalles del contrato y de operación.

## Cómo convertir este análisis en tickets después

Cada ticket deberá indicar: problema del operador, hallazgos H relacionados, reglas RN afectadas, criterio AC, comportamiento visible antes/después, migración de datos si existe y riesgo de compatibilidad. Evitar títulos vagos como “mejorar CRM” o “integrar Twenty”.

Ejemplos de futuros paquetes: “Evitar dos cortes por confirmar dos veces”, “No cerrar deuda por filas rechazadas”, “Mostrar variación desde cartera cero”, “Separar comprobante de saldo” y “Conservar contexto al abrir cliente”. Son descripciones preparatorias; no se crearon issues ni se autorizó un cambio de plataforma.

## Métrica de éxito del upgrade

El operario puede aceptar un corte y explicar qué cambió sin cálculos manuales; no se pierde historial por errores de carga; se mantienen los mails y sus resultados; cada excepción tiene una próxima acción. El total de la cartera y sus cambios son reproducibles desde los cortes. Una plataforma más grande solo se justifica si ayuda a lograr esto con menos costo de uso y mantenimiento.
