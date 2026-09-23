# Análisis del producto: cortes de deuda y evolución hacia CRM

Actualizado: 23/09/2026. Estado: análisis y propuesta; no hay migración iniciada ni tickets creados.

## Decisión central

El producto es una herramienta de cobranza alimentada por un **Excel completo de deudores aproximadamente cada 15 días**, con un maestro de clientes independiente. El historial de deuda debe existir aunque no se envíe ningún correo. Twenty es una posible base de CRM y una referencia de interacción; no sustituye las reglas de interpretación de esos cortes.

Recomendación: definir y corregir primero el contrato del corte, sus comparaciones y el dashboard. Adoptar búsqueda, fichas y vistas coherentes. Decidir una migración a Twenty después de una prueba de ajuste que conserve el recorrido Excel → revisión → mails → seguimiento. Evitar por ahora un fork profundo y un CRM comercial de alcance general.

## Documentos

| Archivo | Para qué sirve |
|---|---|
| [01_OBJETIVO_Y_CONTRATO_DE_DATOS.md](01_OBJETIVO_Y_CONTRATO_DE_DATOS.md) | Alcance confirmado, fuentes, fechas, identidad y reglas de importación |
| [02_AUDITORIA_DEL_COMPORTAMIENTO_ACTUAL.md](02_AUDITORIA_DEL_COMPORTAMIENTO_ACTUAL.md) | Hallazgos concretos, impactos y referencias al producto actual |
| [03_REGLAS_DE_CORTES_E_HISTORIAL.md](03_REGLAS_DE_CORTES_E_HISTORIAL.md) | Altas, desapariciones, reapariciones, correcciones y continuidad |
| [04_DASHBOARD_Y_METRICAS.md](04_DASHBOARD_Y_METRICAS.md) | Definición de cada indicador, cálculos y ejemplos verificables |
| [05_TWENTY_FUNCION_POR_FUNCION.md](05_TWENTY_FUNCION_POR_FUNCION.md) | Qué aporta Twenty, qué adaptar, qué posponer y qué descartar |
| [06_ARQUITECTURA_Y_DECISION_DE_MIGRACION.md](06_ARQUITECTURA_Y_DECISION_DE_MIGRACION.md) | Opciones de solución, responsabilidades y condiciones para migrar |
| [07_ESCENARIOS_Y_CRITERIOS_DE_ACEPTACION.md](07_ESCENARIOS_Y_CRITERIOS_DE_ACEPTACION.md) | Casos concretos para validar el sistema actual y cualquier reemplazo |
| [08_HOJA_DE_RUTA_Y_DECISIONES.md](08_HOJA_DE_RUTA_Y_DECISIONES.md) | Entregas ordenadas y decisiones necesarias antes de crear tickets |
| [09_EVIDENCIAS_Y_LIMITES.md](09_EVIDENCIAS_Y_LIMITES.md) | Pruebas ejecutadas, resultados y lo que todavía no se comprobó |
| [10_ANALISIS_GENERAL_Y_UI_PREVIO.md](10_ANALISIS_GENERAL_Y_UI_PREVIO.md) | Revisión previa de pantallas, accesibilidad y otros CRM, conservada como antecedente |
| [11_MAPA_DEL_REPOSITORIO_PREVIO.md](11_MAPA_DEL_REPOSITORIO_PREVIO.md) | Mapa elaborado durante la exploración inicial |
| [12_GRILLING_ENTREGA_Y_EVOLUCION.md](12_GRILLING_ENTREGA_Y_EVOLUCION.md) | Conversación abierta para separar piloto próximo, profesionalización y decisión de plataforma |
| [13_HOSTING_Y_COSTOS.md](13_HOSTING_Y_COSTOS.md) | Precios, compatibilidad de correo y alternativas de infraestructura para el piloto |
| [14_ALTERNATIVAS_BARATAS_Y_EXPERIENCIAS.md](14_ALTERNATIVAS_BARATAS_Y_EXPERIENCIAS.md) | Experiencias de foros, dimensionamiento y presupuestos ilustrativos de una infraestructura económica |
| [HANDOFF_PRODUCTO_Y_RUTA.md](HANDOFF_PRODUCTO_Y_RUTA.md) | Resumen para continuar: acuerdos, evidencia, decisiones abiertas y estado del fork |

Los documentos 01–09 incorporan la aclaración más reciente del objetivo y prevalecen sobre recomendaciones incompatibles del antecedente 10. Los identificadores H, RN, KPI, T y AC permiten vincular futuros tickets con una necesidad y su prueba de aceptación.

## Qué está demostrado

- Se revisaron los recorridos, las reglas de importación, la persistencia, los cálculos y las pantallas correspondientes.
- Se ejecutaron 44 tests existentes del área de cortes/dashboard/parser: todos pasaron. Que pasen demuestra el comportamiento actual; algunas expectativas existentes deberán cambiar para cumplir las reglas propuestas.
- Se hicieron ocho reproducciones de comportamiento en bases SQLite en memoria y un ejemplo matemático de ambigüedad entre cortes. Los resultados están documentados en 09 y en `evidencias/RESULTADOS_CORTES.json`.
- Twenty se evaluó mediante documentación oficial, repositorio público y demostración visual pública. No se instaló ni se certificó la compatibilidad de una versión concreta.

## Lectura rápida

1. Leer 01 y 04 para acordar qué debe significar cada dato.
2. Usar 02 y 07 para comprobar los huecos y aceptar las correcciones.
3. Leer 05 y 06 para decidir cuánto CRM aporta valor.
4. Convertir las entregas de 08 en tickets solo cuando estén resueltas sus decisiones de entrada.

La auditoría no modificó la aplicación ni la base de demostración y no envió correos.
