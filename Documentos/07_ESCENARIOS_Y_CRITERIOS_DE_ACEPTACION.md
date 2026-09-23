# Escenarios y criterios de aceptación

Fecha: 13/09/2026. Esta es la especificación de validación para las próximas entregas. Solo los casos señalados como reproducción R tienen evidencia de ejecución actual; los demás son pruebas pendientes.

## Importación y continuidad

| ID | Dado / cuando | Resultado requerido | Hallazgo/regla |
|---|---|---|---|
| AC01 | Primera carga válida de 30 deudores | 30 clientes con deuda, total conciliado, sin “cobro” ni delta anterior | RN05, KPI01–02 |
| AC02 | Se confirma dos veces el mismo borrador | Un solo corte y una sola autorización de campaña | H02, R01, RN02 |
| AC03 | Mismo contenido para nueva fecha real | Se puede aceptar como otra observación después de confirmar fecha/procedencia; no se trata como retry | RN03 |
| AC04 | Cliente desaparece del siguiente corte completo | Saldo cero según ese corte; cierre del episodio; maestro e historial conservados | RN04 |
| AC05 | Cliente reaparece tras una ausencia válida | Mismo cliente, episodio nuevo, racha 1, etiqueta recurrente | R06, RN08 |
| AC06 | Cliente sigue debiendo el mismo importe | Continúa episodio; no inventar pago ni nuevo cargo | RN06 |
| AC07 | Saldo baja de $100.000 a $60.000 | Reducción observable $40.000, mantiene episodio | R05, KPI08 |
| AC08 | Saldo aumenta | Aumento neto separado; no compensar y ocultar regularizaciones de otros clientes | KPI09 |
| AC09 | Se omite una quincena | No se crea un corte ni deuda cero; alerta de datos atrasados | RN15 |
| AC10 | Se intenta subir archivo anterior al corte vigente | Rechazo explicado o carga histórica separada; no reemplaza saldo vigente | R08, H01 |
| AC11 | Se corrige una versión de la misma fecha | Reemplazo trazable, un punto en la serie, recálculo coherente de intervalos posteriores | H09, RN01/16 |
| AC12 | Archivo parcial o de otra cartera | No cierra clientes fuera de cobertura; primera versión puede rechazarlo | RN04 |
| AC13 | Export legítimo sin deudores | Recorrido explícito “cartera sin deuda”, impacto revisado y corte cero válido | R02, RN09 |
| AC14 | Todas las filas fueron rechazadas | No puede convertirse en corte cero válido | R03, H03 |
| AC15 | Monto textual `150.000,50`, fórmula sin valor, negativo, NaN o vacío | Regla explícita por formato; errores visibles; aceptación bloqueada si comprometen completitud | H04 |
| AC16 | Clave con ceros, número 0, espacios o tipo distinto | Identificación estable según contrato; no cerrar y crear otro cliente accidentalmente | H04/RN13 |
| AC17 | Clave repetida en dos filas | Mostrar conflicto; resolver según contrato cliente/factura; total conciliado | R07 |
| AC18 | Archivo .xls auténtico o archivo corrupto | Soporte real o rechazo comprensible antes de confirmar; nunca error genérico seguido de saldo cero | H04 |
| AC19 | Otro usuario acepta un corte durante el preview | Detectar versión cambiada y recalcular antes de aceptar | H08 |
| AC20 | Se corta la conexión durante aceptación | Estado consultable por ID; retry sin duplicar; dashboard solo ve versión completa | RN02 |

## Clientes y correo

| ID | Dado / cuando | Resultado requerido | Hallazgo/regla |
|---|---|---|---|
| AC21 | Deudor sin maestro/email o por debajo, exactamente en y por encima del mínimo | Todos siguen en saldo y deuda; elegibilidad de envío aplica el umbral acordado, sin redondeo que cambie de grupo | RN10–11 |
| AC22 | Cliente inactivo o dado de baja sigue en Excel | Sigue debiendo; no recibe campaña automática | RN10 |
| AC23 | Se corrige email inválido | Próxima acción recuperable, con saldo vigente y destinatario revalidado | H17 |
| AC24 | Se importa un corte sin enviar mails | Historial y dashboard actualizados; cero recordatorios nuevos | H07/H11 |
| AC25 | Respuesta trae imagen de firma o PDF no comprobante | Se registra mensaje/evidencia; no cambia saldo, racha ni ranking | R04, H05 |
| AC26 | Respuesta a un ciclo viejo llega después del nuevo | Figura en actividad del cliente y campaña original; no reinicia antigüedad | R04, H06 |
| AC27 | Primero responde texto y luego manda comprobante | Ambos mensajes y adjunto accesibles; seguimiento no termina en la primera respuesta | Antecedente UI/correo |
| AC28 | Dos consorcios comparten dirección/dominio | Historial correcto por clave y mensaje; no fusionar deudas ni adjuntos | RN12, T18 |
| AC29 | Reintento de campaña de un corte sustituido/saldado | Bloqueo o nueva preparación según saldo vigente; nunca reclamar monto obsoleto silenciosamente | H17–18 |
| AC30 | Baja o nuevo corte mientras hay mensajes en cola | Pendientes revalidados/cancelados; enviados preservados con su contexto | RN18 |
| AC31 | Reinicio o caída del proveedor durante campaña | Pendientes recuperables; intentos auditados; ningún duplicado por retry ciego | Arquitectura |
| AC32 | Promesa para el viernes, llega nuevo corte sin deuda | Cierre según facturación; tarea resuelta con motivo y vínculo al corte | T04/T21 |
| AC33 | Comprobante posterior al corte pero cliente aún figura deudor | Estado “Comprobante por revisar” y saldo del corte visibles juntos; no mensaje contradictorio “Al día” | RN14 |

## Dashboard e interacción

| ID | Dado / cuando | Resultado requerido | Hallazgo/regla |
|---|---|---|---|
| AC34 | Dataset de ocho clientes del documento 04 | Totales $900.000 → $810.000; puente exacto; 6 → 6 clientes | KPI01–10 |
| AC35 | Saldo anterior cero | Delta absoluto correcto; porcentaje no aplicable, sin falsa ausencia de corte | H15 |
| AC36 | 01/09, 16/09 y 01/10, con un mes sin cargas | Fechas distintas, puntos reales y huecos identificables | H13 |
| AC37 | Cliente $100k → $60k → ausencia | Ficha $0 al corte; reducción/salida $100k con nombres correctos; no confundir cierre $60k | R05, H10/H14 |
| AC38 | Cliente 5 cortes sin email | “5 cortes con deuda” y “0 recordatorios”; ambos correctos | R01, H11 |
| AC39 | Saldo vigente con larga continuidad y nuevos cargos | Etiqueta de continuidad del cliente, sin atribuir 90 días de vencimiento a todo el monto | H12 |
| AC40 | Cambia de corte mientras cargan tablas/KPI | Una revisión coherente por vista; reintento de datos incompletos | H19 |
| AC41 | Uso con teclado y teléfono | Buscar, revisar corte, abrir cliente y gestionar sin controles inaccesibles ni menú que tape contenido | Auditoría UI |
| AC42 | Corte rechazado o error de consulta | Mantener/identificar último dato válido; error recuperable, nunca mostrar vacío como éxito | H03/H19 |

## Validación de Twenty antes de migrar

La opción elegida debe superar los mismos AC aplicables que la aplicación propia. Agregar: operador sin permisos de administración; UI en español y moneda/fechas locales; carga del historial antiguo; vínculo de correo a consorcios con administradora compartida; exportación y restauración; actualización de la extensión sin modificar el núcleo; costo de cualquier función premium requerida.

Un mock visual no satisface AC24–33. Una respuesta HTTP 200 no satisface AC34–42. Registrar siempre entorno, versión, datos de entrada, resultado esperado, obtenido y evidencia.

## Matriz mínima antes de un piloto real

Prioridad bloqueante: AC01–05, AC09–17, AC19–25, AC28–31 y AC34–35. Completar los restantes que formen parte del alcance liberado antes de declarar terminado el upgrade. Si una capacidad se pospone, la UI debe evitar sugerir que existe.
