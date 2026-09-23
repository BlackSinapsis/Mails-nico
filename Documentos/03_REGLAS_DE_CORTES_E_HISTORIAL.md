# Reglas propuestas para los cortes y el historial

Fecha: 13/09/2026. Especificación funcional propuesta; todavía no implementada.

## Modelo mínimo suficiente

| Registro | Qué conserva | Qué evita |
|---|---|---|
| Cliente | Identificador interno, clave externa, nombre y estado comercial | Crear un cliente nuevo cada quincena |
| Contacto | Email, función y relación con cliente/administradora | Usar el email como identidad de deuda |
| Importación | Archivo, huella, hoja, errores, responsable y fecha de carga | No poder explicar de dónde salió un dato |
| Corte | Fecha de negocio, ámbito, versión aceptada y totales | Confundir subir un archivo con avanzar el tiempo |
| Saldo por cliente y corte | Clave, monto, moneda y procedencia de fila | Sobrescribir el historial con el último saldo |
| Episodio observado | Primera presencia continua, última presencia, cierre/reaparición | Mezclar una deuda anterior regularizada con una posterior |
| Campaña e intento | Corte de origen, destinatarios, mensaje y resultado | Contar una carga como si fuera un mail |
| Gestión | Nota, tarea, promesa, comprobante y resultado de revisión | Convertir una respuesta de correo en saldo contable |

No es necesario duplicar un cliente por cada episodio. El episodio puede comenzar como una proyección calculada a partir de los cortes válidos; persistir un caso de gestión solo cuando se necesite responsable, tareas o promesas. No introducir infraestructura de eventos compleja para resolver estas relaciones.

## Tabla de transiciones

Comparar el corte actual B con el anterior A aceptado, de igual ámbito y moneda. “No observado antes” se refiere al historial conocido, no a la vida completa del cliente.

| En A | En B | Historia anterior | Resultado |
|---|---|---|---|
| Ausente | Presente | Nunca observado con deuda | Primera aparición observada; abrir episodio |
| Ausente | Presente | Episodio cerrado anteriormente | Reaparición; nuevo episodio y misma ficha de cliente |
| Presente | Presente, igual monto | Cualquiera | Continuidad con saldo estable |
| Presente | Presente, menor monto | Cualquiera | Continuidad con reducción neta observada |
| Presente | Presente, mayor monto | Cualquiera | Continuidad con aumento neto observado |
| Presente | Ausente | B completo y válido | Regularizado según B; cerrar episodio |
| Ausente | Ausente | Cobertura conocida | Continúa sin deuda informada |
| Presente | Sin observación | B faltante/parcial/rechazado | Estado desconocido en B; no cerrar ni incrementar observaciones |

Un corte puede producir primera aparición, reaparición y disminución de saldo en clientes diferentes al mismo tiempo. Las categorías por presencia y por variación se calculan separadamente, con conteos consistentes.

## Reglas identificadas

- **RN01 — Historial inmutable:** preservar filas aceptadas y archivo fuente. Una rectificación crea una nueva versión; la original sigue auditable.
- **RN02 — Publicación única:** una confirmación repetida de un mismo borrador produce el mismo corte. No crea un ciclo, episodio o campaña adicional.
- **RN03 — Igual contenido no siempre es duplicado:** mismo archivo para la misma fecha/ámbito es repetición; mismos saldos en una fecha posterior pueden ser un nuevo corte legítimo. Advertir reutilización del archivo, sin decidir solo por su huella.
- **RN04 — Cierre por ausencia:** requiere nuevo corte completo, válido, aceptado, posterior y comparable. La fecha de cierre observada es la del corte, no la fecha bancaria del pago.
- **RN05 — Primera carga:** establece una línea de base. No calcula cobros, variaciones ni vencimientos anteriores al sistema.
- **RN06 — Racha:** cantidad de cortes comparables consecutivos con saldo positivo. Un mail, una plantilla o un reintento no la aumenta ni la reinicia.
- **RN07 — Antigüedad:** diferencia de fechas de observación; no racha multiplicada por 15. La primera observación es un límite del conocimiento, no el vencimiento original.
- **RN08 — Reaparición:** si hubo una ausencia válida intermedia, abrir nuevo episodio. Mostrar recurrencia histórica sin afirmar automáticamente que se trata de la misma deuda.
- **RN09 — Corte vacío:** distinguir declaración de cero deuda de archivo sin datos utilizables. Mostrar impacto sobre clientes y total antes de aceptar.
- **RN10 — Contactabilidad:** mínimo de monto, falta de email, baja de comunicaciones e inactividad comercial solo afectan los envíos. La deuda continúa en indicadores e historial.
- **RN11 — Cliente sin maestro:** conservar su saldo con clave externa y nombre del archivo; abrir pendiente de identificación/contacto. No excluir su deuda ni crear silenciosamente un contacto incorrecto.
- **RN12 — Email compartido:** varios consorcios pueden tener la misma administradora/email. Asociar por clave, campaña y mensaje; no fusionar clientes por dirección o dominio.
- **RN13 — Corrección de identidad:** mantener alias/equivalencia explícita y auditada. Evitar registrar un cierre y una primera aparición falsos por renumeración del mismo cliente.
- **RN14 — Correo frente a corte:** un comprobante cambia el estado de gestión. El saldo informado del corte permanece, con una indicación de evidencia posterior si corresponde.
- **RN15 — Sin actualización:** alertar por demora de carga; conservar el último corte con su fecha. No asegurar que ese saldo siga siendo el saldo real al día de consulta.
- **RN16 — No reenviar por recalcular:** corregir o insertar un corte histórico actualiza proyecciones, no dispara correos ni repite tareas ya ejecutadas.
- **RN17 — Unidades monetarias:** calcular con decimales y precisión acordada; no mezclar monedas ni redondear cada fila antes de sumar sin una regla del origen.
- **RN18 — Seguridad operativa del envío:** antes de cada intento, verificar que la campaña no quedó obsoleta, la baja siga respetada y exista saldo elegible según la política vigente.

## Correcciones y cargas fuera de orden

### Error detectado en el último corte

Guardar nueva versión del mismo corte, mostrar diferencia contra la versión vigente y activar la corrección de forma atómica. Recalcular regularizaciones, reapariciones, rachas y KPI afectados. Conservar mensajes ya enviados y marcar cuáles se basaron en datos corregidos. Cancelar pendientes afectados. Una rectificación no desenvía un mail ni borra actividad de la persona.

### Archivo atrasado o histórico

Propuesta inicial: no permitir que reemplace automáticamente el corte vigente. Ofrecer un recorrido separado para incorporar historia, solo si se necesita. Ordenar por fecha de corte y recalcular las transiciones posteriores. Si esa función no se implementa en la primera entrega, rechazar claramente la carga atrasada; no aceptarla como nueva.

### Dos versiones para la misma fecha

Tratar la segunda como rectificación, nunca como otra quincena. Para una cartera inicialmente única, una versión vigente por fecha es suficiente. Si se requieren varios cierres intradía, ampliar el contrato con hora o identificador del reporte.

### Una carga mientras otra persona revisa

El borrador guarda la revisión de base utilizada para comparar. Si cambió el corte aceptado, recalcular y pedir una nueva aceptación informada dentro del producto. La campaña conserva los destinatarios y texto aprobados, y revalida exclusiones antes de enviarse.

## Ejemplo de historial de un cliente

| Corte | Saldo informado | Hecho observado | Gestión independiente |
|---|---:|---|---|
| 01/08 | $200.000 | Primera aparición conocida | Recordatorio enviado |
| 16/08 | $150.000 | Disminuye $50.000; sigue debiendo | Promete pagar el 22/08 |
| 01/09 | Ausente → $0 | Regularizado según facturación; cierre observado | Puede conservarse comprobante recibido el 25/08 |
| 16/09 | $90.000 | Reaparece; nuevo episodio | Debajo del mínimo, sin mail automático |
| 01/10 | Sin corte | Sin nueva observación | Alerta de actualización pendiente |

La ficha conserva los dos episodios, muestra 3 cortes con deuda, los mails realmente enviados y las fechas exactas de cada observación. No debe decir que los $90.000 son deuda vencida desde agosto.

## Límite deliberado del producto

Con saldos quincenales no se reconstruyen todos los movimientos. $100.000 → $80.000 puede ser un pago de $20.000, o un pago de $70.000 más nuevos cargos de $50.000. Asimismo, un cliente puede pagar y volver a deber el mismo monto entre cortes sin que el sistema lo vea. El historial debe describir lo observado y reservar “cobros confirmados” para una fuente que los identifique.
