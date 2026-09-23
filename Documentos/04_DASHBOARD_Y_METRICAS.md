# Dashboard: definiciones que resisten el uso quincenal

Fecha: 13/09/2026. Objetivo: cada cifra debe poder explicarse con una lista de clientes y dos cortes identificados.

## Jerarquía propuesta

Encabezado: **Cartera al 16/09/2026 · cargada el 17/09 · corte completo**. Mostrar última revisión de correo aparte. Aviso si faltó la actualización esperada.

Primera fila: saldo informado, clientes con deuda, regularizados desde el corte anterior y clientes que aparecen/reaparecen. Segunda sección: explicación del cambio de saldo. Debajo: evolución por cortes y listas para actuar. Evitar quince tarjetas de igual peso; las métricas adicionales van al detalle.

Un selector permite explorar cortes anteriores de manera explícita. Las cifras financieras se calculan “al corte”; la gestión actual se muestra identificada como actual. No mezclar ambos tiempos silenciosamente.

## Definiciones

Sea A el corte anterior comparable y B el elegido. D_A y D_B son conjuntos de clientes con saldo positivo; s_A y s_B sus saldos. Para clientes ausentes, usar cero solo si la cobertura del corte es válida. En el primer corte no existe comparación.

| ID | Indicador | Cálculo y alcance | Nombre o advertencia |
|---|---|---|---|
| KPI01 | Saldo informado | Suma de s_B, incluidos sin mail/filtrados/inactivos | “Saldo según corte del…” |
| KPI02 | Clientes con deuda | Cantidad de claves únicas en D_B | No cantidad de filas de factura ni de mails |
| KPI03 | Regularizados | D_A menos D_B | Cierre por ausencia en corte completo; no se borran del maestro |
| KPI04 | Nuevas apariciones | D_B menos D_A | Separar primera aparición conocida y reaparición |
| KPI05 | Continúan debiendo | Intersección D_A y D_B | Desglosar saldo igual, menor y mayor |
| KPI06 | Variación neta | Suma s_B menos suma s_A | Mostrar importe con signo; % solo con base A > 0 |
| KPI07 | Saldo que sale de cartera | Suma s_A de regularizados | Saldo informado previo de quienes regularizaron |
| KPI08 | Reducciones entre quienes continúan | Suma de max(s_A − s_B, 0) en la intersección | Reducciones netas observadas; no cobros brutos |
| KPI09 | Aumentos entre quienes continúan | Suma de max(s_B − s_A, 0) en la intersección | Aumentos netos observados; no facturación bruta |
| KPI10 | Saldo de apariciones | Suma s_B de D_B menos D_A | Separar primera aparición y recurrentes |
| KPI11 | Continuidad prolongada | Saldo actual de clientes observados con continuidad >90 días al corte | No afirmar que todo ese saldo tiene 90 días de vencido |
| KPI12 | Cobertura de contacto | Deudores elegibles con contacto válido / deudores elegibles | Definir elegibilidad; dar numerador y denominador |
| KPI13 | Recordatorios enviados | Mensajes con confirmación de aceptación por proveedor, por campaña/período | No equivale a entrega ni a ciclos |
| KPI14 | Respuestas humanas | Mensajes/hilos entrantes humanos vinculados / destinatarios enviados según definición | Rebotes y autorrespuestas no son conversación útil |
| KPI15 | Trabajo pendiente | Promesas vencidas, comprobantes por revisar, correos por corregir y tareas vencidas | Son listas de gestión, no variaciones del saldo |

No mostrar “cobrado por los mails” a partir de estos datos. La atribución causal al recordatorio no se deduce de la desaparición posterior. Si se desea un indicador de regularización entre contactados, llamarlo así, fijar la cohorte y conservar el denominador.

## Identidad de reconciliación

Para cortes completos comparables:

**Saldo B = saldo A − saldo que sale − reducciones + aumentos + saldo de apariciones.**

**Deudores B = deudores A − regularizados + apariciones.**

Ambas identidades deben cumplirse con los mismos filtros y moneda, sin diferencias de redondeo. Cada componente abre su lista; exportar el detalle debe reproducir el total. No sumar saldos de cortes sucesivos como si fueran montos adeudados distintos.

## Ejemplo numérico de aceptación

| Cliente | 01/09 | 16/09 | Interpretación |
|---|---:|---:|---|
| Acacias | $200.000 | Ausente | Regularizado; salen $200.000 |
| Laureles | $300.000 | $250.000 | Reducción neta de $50.000 |
| Rosales | $80.000 | $120.000 | Aumento neto de $40.000 |
| Tilos | Ausente | $150.000 | Primera aparición; entran $150.000 |
| Cedros | $50.000 | $50.000 | Continúa; debajo del mínimo, pero suma deuda |
| Olivos | Ausente | $90.000 | Reaparición si existe episodio previo cerrado |
| Pinos | $120.000 | Ausente | Regularizado; salen $120.000 |
| Sauces | $150.000 | $150.000 | Continúa sin email; suma deuda |

- Saldo A: $900.000; saldo B: $810.000; variación: −$90.000 (−10%).
- Deudores: 6 → 6; regularizados: 2; apariciones: 2, de las cuales 1 recurrente.
- Sale de cartera: $320.000; reducciones: $50.000; aumentos: $40.000; apariciones: $240.000.
- Verificación: 900.000 − 320.000 − 50.000 + 40.000 + 240.000 = 810.000.
- Las reducciones y salidas suman $370.000. El saldo neto bajó $90.000. Ninguna cifra es una medición de cobro bruto sin información de movimientos.

## Estados sin dato y base cero

| Situación | Qué mostrar |
|---|---|
| Antes del primer corte | “Todavía no hay un corte aceptado” |
| Primer corte | Saldo y deudores; comparación “Sin base anterior” |
| Corte anterior $0, actual $100.000 | Variación +$100.000; porcentaje “No aplica: base cero” |
| Ambos cortes $0 | Variación $0; sin aumento rojo ni “sin corte anterior” |
| Corte rechazado o carga fallida | Último corte válido y error; no reemplazarlo por cero |
| Mes sin corte | “Sin observación”; mantener el hueco o arrastre explícitamente señalado |
| Cliente ausente en corte completo | $0 según ese corte |
| Cliente fuera de cobertura o anterior al historial conocido | “Sin dato”, no “Al día” |

## Gráficos e historial

- Vista inicial por cortes reales: etiquetas `01/09`, `16/09`, `01/10`; tooltip con año, fecha del corte, carga y versión. Los puntos deben reflejar la distancia temporal real.
- Un gráfico escalonado puede representar “último saldo informado conocido”, siempre rotulado así. No implica que el saldo bancario permaneció constante entre observaciones.
- Vista mensual opcional: último corte disponible del mes, indicando su fecha; no llamarlo cierre de mes cuando fue el día 16. Nunca sumar ambos saldos quincenales.
- Los meses omitidos deben verse; una curva suavizada entre enero y abril no prueba una evolución observada en febrero y marzo.
- La ficha de cliente puede mostrar regularizaciones y reapariciones en una misma línea. Las versiones sustituidas no generan puntos adicionales.
- Los mails, promesas y comprobantes se dibujan como actividad con fechas propias. No cambian el valor de la serie de facturación.

## Qué cambiar en “Saldado histórico”

En $100.000 → $60.000 → ausente, la fórmula actual muestra $60.000 y la suma de reducciones/salida es $100.000. Ambas cantidades describen hechos diferentes. Propuesta: “Reducciones y salidas observadas” con detalle por intervalo; opcional “Saldo al cierre de episodios”. No etiquetar ninguna como “Total pagado” si solo se tiene el Excel de saldos.

## Pruebas de coherencia de pantalla

Toda respuesta debe incluir el identificador/revisión del corte usado. La tarjeta, tabla y gráfico no pueden combinar revisiones. Los filtros de campaña no se aplican a cartera; si se filtra cartera por administradora o responsable, todos sus indicadores deben usar esa misma selección y mostrarlo. El ranking por importe y el de continuidad parten del mismo conjunto de deudores; el segundo puede priorizar o filtrar, pero debe explicar el subconjunto.
