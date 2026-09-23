# Auditoría de cortes, historial y dashboard actuales

Fecha: 13/09/2026. P1 = puede alterar una decisión de cobranza o el historial; P2 = claridad y productividad. “Reproducido” significa ejecución aislada, no incidente ocurrido con datos reales.

## Base que ya resuelve parte del objetivo

El maestro persiste separado de los ciclos; confirmar un archivo archiva el ciclo anterior y conserva sus registros. Los deudores sin email, inactivos o debajo del mínimo también quedan registrados y suman deuda. La desaparición del corte siguiente marca el registro anterior como saldado. Una reaparición posterior inicia una nueva racha cuando el episodio previo quedó saldado. Hay preview con conteos de nuevos, repetidos y saldados, advertencia de desaparición superior al 50%, historial por cliente y consulta de ciclos anteriores. Son capacidades que deben conservarse.

## Hallazgos priorizados

| ID | Prioridad y evidencia | Comportamiento e impacto | Cambio necesario |
|---|---|---|---|
| H01 | P1, modelo y ruta | El ciclo solo guarda fecha de carga y número. Un archivo viejo se acepta como nuevo y puede elevar el saldo vigente | Fecha de corte y ámbito; orden de negocio; tratamiento explícito de cargas atrasadas |
| H02 | P1, R01 | Confirmar dos veces el mismo archivo crea dos ciclos y aumenta la racha | Reconocer corte repetido y confirmación repetida; mantener igual resultado sin efectos duplicados |
| H03 | P1, R02–R03 | Un archivo con encabezados solos, o filas cuyo monto textual se descarta, puede cerrar toda la cartera | Reporte de errores y confirmación específica de corte sin deudores |
| H04 | P1, parser/R07 | Duplicados conservan última fila; clave numérica pierde formato de ceros; montos argentinos en texto se omiten | Contrato de filas, identidad y formatos explícitos antes de publicar |
| H05 | P1, R04 | PAGO en un mail corta la racha de deuda y excluye del ranking por antigüedad, pero el saldo sigue en el total | Separar estado del corte y del mensaje |
| H06 | P1, R04 | Una respuesta PAGO en un ciclo viejo cambia hoy el inicio de la racha aunque los Excel intermedios mantengan deuda | Las respuestas tardías agregan actividad; no reescriben continuidad contable |
| H07 | P1, ruta/modelo | Guardar corte y disparar mails están unidos; no existe un modo explícito de “actualizar sin enviar” | Independencia de corte, campaña e intento, preservando un recorrido corto |
| H08 | P1, fuente | Preview y confirmación vuelven a interpretar el archivo y maestro; no hay versión aceptada ni confirmación ligada a una base de comparación | Borrador identificado, versión y detección de cambios antes de confirmar |
| H09 | P1, fuente | No hay rectificación de corte, versionado ni exclusión de revisiones del gráfico | Corrección trazable que sustituye una versión y recalcula comparaciones, sin mails retroactivos |
| H10 | P1/P2, R05 + UI | “Saldado histórico” suma solo el saldo al desaparecer; omite reducciones previas. $100k → $60k → ausente muestra $60k | Distinguir saldo al cierre, reducciones observadas y cobros confirmados |
| H11 | P2, UI/R01 | La columna “Recordatorios” usa cantidad de ciclos, incluyendo cortes sin mail | Contar mensajes aceptados por proveedor; mostrar cortes por separado |
| H12 | P1/P2, servicio/UI | “Deuda +90 días” usa primera carga y reloj actual, no vencimiento. Incluye todo el saldo actual del cliente | “Saldo de clientes con continuidad observada >90 días al corte”; advertencia de datos atrasados |
| H13 | P2, UI | Gráfico principal conserva solo último ciclo de cada mes y suaviza entre puntos; oculta cambios quincenales y saltos de cobertura | Vista predeterminada por fecha de corte, con detalle; mensual como alternativa explicada |
| H14 | P2, R05 + UI | Cliente ausente en el corte actual tiene “Deuda actual —” aunque el gráfico dibuja cero | Cero cuando la cobertura completa lo demuestra; desconocido cuando no la demuestra |
| H15 | P2, UI | Si el corte anterior tiene deuda cero se muestra “Sin ciclo anterior” y se pierde una comparación válida | Delta absoluto; porcentaje no calculable por base cero |
| H16 | P2, modelo/fuente | Maestro puede sobreescribir datos manuales; no registra identidad histórica ni cambios de administradora. Ausencia del maestro no elimina clientes | Precedencia explícita, auditoría y conservación de identidad/contactos |
| H17 | P1, fuente | Reintento individual no comprueba que el envío pertenezca al corte vigente ni que no esté saldado | Bloquear o reconstruir el recordatorio contra el último saldo aceptado |
| H18 | P1, fuente | Campañas activas no reevalúan todo el estado de deuda al aceptar otro corte | Cancelar pendientes obsoletos; revalidar vigencia, baja y destinatario antes de despachar |
| H19 | P2, UI | Dashboard hace cuatro consultas independientes sin versión compartida; al aceptar un corte concurrente puede mezclar respuestas | Una revisión común y refresco coherente; no se reprodujo la carrera |

## Aclaraciones para no confundir defecto con regla de negocio

- **Desaparecer = regularizado** es una regla válida confirmada para este producto. El hueco está en no certificar integridad, fecha y ámbito del archivo antes de aplicarla.
- Mantener en la deuda a quien está filtrado por monto o no tiene mail es correcto. Los filtros de comunicación no deben alterar el total de cartera.
- “Cobrado” existe en el servicio/API de resumen y evolución, pero el dashboard principal actual no lo muestra como tarjeta. La auditoría de ese cálculo no debe presentarse como una tarjeta visible inexistente.
- Racha actual mide observaciones consecutivas con saldo; no prueba que sea la misma factura impaga. Si un cliente paga y vuelve a deber entre dos cortes, esa discontinuidad no es observable con saldos solos.
- La falta de una carga no es una desaparición. No se debe cerrar a nadie por pasar 15 días.

## Referencias de evidencia

| Componente | Ubicación en el repositorio |
|---|---|
| Confirmación, preview y reintentos | `backend/app/routers/ciclos.py` |
| Ausencia y saldado | `backend/app/services/ciclo_service.py` |
| KPI, reducciones y antigüedad | `backend/app/services/dashboard_service.py` |
| Claves, formatos y duplicados | `backend/app/services/excel_parser.py` |
| Unión, rachas y filtros | `backend/app/services/excel_joiner.py` |
| Historial y maestro | `backend/app/routers/maestro.py`, `backend/app/services/maestro_service.py` |
| Mensajes y respuesta tardía | `backend/app/services/imap_watcher.py`, `reply_classifier.py`, `routers/seguimiento.py` |
| Tarjetas y series | `frontend/src/pages/DashboardPage.tsx`, `ClientePerfilPage.tsx`, `components/dashboard/EvolucionChart.tsx` |

Las reproducciones R01–R08 y los límites de la prueba están en el documento 09. Los 44 tests actuales pasan: varios protegen justamente las reglas anteriores que aquí proponemos cambiar. No alcanza con conservarlos verdes; hacen falta los criterios del documento 07.
