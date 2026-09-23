> Antecedente preservado el 13/09/2026. Para el objetivo actualizado de cortes quincenales, las reglas y decisiones vigentes de análisis están en [00_INDICE.md](00_INDICE.md) y documentos 01–09. Este archivo conserva la revisión previa; no implica decisiones de implementación aprobadas.

# De recordatorios por mail a CRM de cobranza

Revisión de producto, experiencia de uso y arquitectura de solución · 13 de septiembre de 2026.

## Dictamen

La aplicación tiene una base útil para una empresa de mantenimiento de ascensores: transforma un Excel en recordatorios y permite revisar resultados por ciclo. Cumple una parte importante del objetivo original. Sin embargo, todavía no cierra el proceso de cobranza: no permite demostrar cuánto se cobró, registrar una promesa de pago ni organizar quién debe hacer qué y cuándo.

Recomiendo evolucionarla hacia un **CRM de cobranza especializado en consorcios**. Mantendría el flujo de Excel y el historial existentes, corregiría primero la interpretación de los datos y agregaría una ficha de cliente y una bandeja de trabajo. No recomiendo una migración completa a otro CRM solo para conseguir una interfaz más moderna.

## Qué se evaluó y qué no puede afirmarse

- Lectura de los recorridos de las ocho páginas, modelos de información y operaciones que soportan las pantallas. El código se usó como evidencia del comportamiento, no como objeto de una revisión de estilo.
- Dataset local de 50 clientes, 9 ciclos y 323 registros. En el ciclo activo hay 30 registros: 8 NO_CONTESTADO —6 enviados y 2 fallidos—, 5 CONTESTADO, 4 PAGO, 3 REBOTADO, 4 SIN_EMAIL y 6 FILTRADO. El maestro muestra 46 activos y 4 inactivos.
- En esta sesión se habían ejecutado 190 tests backend: 189 pasaron inicialmente y el caso fallido pasó al corregir el entorno de test; se repitieron los 19 casos de configuración. Esto es evidencia funcional parcial, no una certificación integral ni una prueba de producción.
- En esta revisión se comprobaron por HTTP el acceso y las consultas de resumen, evolución, morosos y envíos: todas respondieron 200. Se reprodujeron casos límite del parser y del clasificador con entradas sintéticas, sin tocar la base.
- Dos evaluaciones independientes de UX y evidencia visual, autorizadas por el usuario. Sus resultados y límites se detallan en el anexo de UI.
- Se consultaron las páginas oficiales actuales de Twenty, SuiteCRM, Frappe CRM y EspoCRM. No se desplegaron ni se hizo una prueba funcional de esos productos.
- No se enviaron mensajes ni se accedió a la bandeja de Gmail en esta auditoría. No se verificaron concurrencia entre servidores, recuperación de un despliegue, carga masiva, restauración de producción ni conciliación bancaria.

## ¿Cumple el objetivo?

| Trabajo del usuario | Situación actual | Evaluación |
|---|---|---|
| Importar clientes y deudores | Maestro, cruce, preview, deduplicación y filtros | Resuelto en el recorrido normal; falta diagnóstico detallado de errores |
| Enviar recordatorios personalizados | Plantilla, proveedor, progreso y reintentos de fallidos | Implementado; falta validar entrega real y recuperación operativa |
| Entender quién contestó | Clasificación y fragmento de respuesta, historial por ciclo | Parcial: la conversación completa y los adjuntos quedan fuera |
| Saber qué hacer hoy | Listas por estado y rankings de deuda | Insuficiente: faltan tareas, vencimientos, responsables y compromisos |
| Confirmar un cobro | PAGO inferido o manual; saldado por desaparición del Excel | Insuficiente para afirmar acreditación o conciliar pagos |
| Gestionar la relación con el cliente | Datos básicos e historial de rondas | Base inicial; faltan administradoras, contactos múltiples, notas y actividad |
| Operar en equipo | Usuarios autenticados | No hay asignación ni permisos por función en el modelo revisado |

## Lo que conservaría

1. **Excel como puerta de entrada.** Es compatible con el trabajo que ya hace la empresa. Una API puede sumarse más adelante sin obligar a cambiar el sistema de facturación.
2. **Preview antes de enviar.** Permite revisar destinatarios y exclusiones. El aviso cuando desaparece más de la mitad de los deudores ya es una buena prevención, aunque no cubre todas las importaciones parciales.
3. **Historial por ciclos y por cliente.** Aporta memoria y permite reconstruir tendencias. Es una base valiosa que no conviene perder en una migración.
4. **Revalidar un reintento contra el maestro actualizado.** Evita reutilizar a ciegas un correo corregido o una baja.
5. **Separación visual de estados y diseño sobrio.** El color acompaña etiquetas, los montos son legibles y la aplicación no está sobrecargada de funciones comerciales ajenas al negocio.

## Los problemas más importantes

### P1 · El estado del correo se confunde con el estado de la deuda

Hoy PAGO pertenece a un registro de envío. Un adjunto puede activarlo, pero eso no prueba la acreditación; además el dashboard puede seguir sumando el saldo del Excel mientras el perfil muestra «Pagó» o «Al día». Hay aclaraciones útiles en Seguimiento y en el panel lateral, pero la terminología no es consistente en todo el producto.

**Cambio:** separar tres cosas: comunicación, gestión de cobranza y saldo. Usar «Comprobante recibido» para la señal automática. «Pago confirmado» debe exigir monto, fecha, origen de validación y usuario responsable. La deuda debe seguir mostrando la fecha de su fuente.

**Criterio de aceptación:** recibir un PDF nunca pone a cero el saldo; confirmar un pago parcial reduce solo el importe conciliado; revertir una clasificación conserva quién la cambió y por qué.

Evidencia: `reply_classifier.py`, `dashboard_service.py`, `ClientePerfilPage.tsx`, `EnvioDrawer.tsx`, `lib/estado.ts`.

### P1 · Se pide revisar un comprobante que la aplicación no permite abrir

El seguimiento conserva un fragmento de hasta 200 caracteres y un indicador de adjunto. La ficha no contiene el archivo ni la conversación completa. El usuario debe buscar el mail por su cuenta para comprobar algo que la pantalla le pide verificar.

**Cambio:** conversación completa vinculada al cliente, adjuntos consultables con acceso controlado y enlace al mensaje original cuando el proveedor lo permita. El primer paso puede ser un identificador visible y una búsqueda directa, antes de construir una bandeja completa.

**Criterio de aceptación:** desde «Comprobante recibido» se llega al documento correcto y se distingue claramente si no pudo descargarse.

### P1 · La cobranza no tiene próxima acción

Un cliente responde «pago el viernes», pero solo queda CONTESTADO. No hay lugar estructurado para registrar fecha, monto prometido, responsable, recordatorio o incumplimiento. Tampoco hay una lista de casos que necesitan atención hoy.

**Cambio:** agregar tarea y compromiso de pago vinculados al cliente y al caso. La pantalla inicial debe priorizar promesas vencidas, comprobantes pendientes y contactos con problemas.

**Criterio de aceptación:** una promesa vencida aparece en la bandeja del responsable; una promesa vigente evita otro recordatorio automático; el cumplimiento requiere evidencia, no solo mover una tarjeta.

### P1 · Un Excel imperfecto puede cambiar la interpretación de toda la cartera

Reproducción: una clave numérica 1 formateada en Excel como 00000001 se lee como «1». No coincide con un maestro que conserva «00000001». Una deuda textual «150.000,50» se omite en vez de generar un error por fila. Dos filas de un cliente conservan la última, no la suma.

La ausencia de un cliente en el nuevo archivo se interpreta como saldado. Si se subió solo una sucursal, una hoja equivocada o un archivo viejo, esa inferencia puede ser falsa. Existe una advertencia de desaparición superior al 50%, pero un archivo parcial más pequeño también puede causar problemas.

**Cambio:** importación con fecha de corte, alcance completo/parcial, normalización explícita de claves, informe de filas rechazadas y reconciliación de totales. Para duplicados, acordar si la fila representa un cliente o una factura antes de elegir sumar o reemplazar. Guardar el archivo, huella y resultado de cada importación.

**Criterio de aceptación:** ninguna fila relevante desaparece sin explicación; el usuario ve filas leídas, válidas, rechazadas y duplicadas; una importación parcial nunca salda por ausencia; reintentar la misma confirmación no crea otra campaña.

### P1 · Un fallo de envío necesita un proceso recuperable

La aplicación distingue enviados y fallidos y mantiene tareas vivas ante un F5. Esa protección no equivale a una cola durable frente al reinicio del servidor. El control en memoria de envíos y velocidad tampoco coordina dos procesos. Además «Sin email» no tiene una recuperación directa dentro del ciclo después de corregir el maestro: el reintento actual acepta NO_CONTESTADO sin message_id.

**Cambio:** una campaña guardada, con intentos persistentes y estados explícitos: pendiente, en proceso, aceptado por el proveedor, fallo temporal y fallo definitivo. Revalidar los casos sin email, permitir pausar y mostrar el motivo del fallo. Evitar confundir «aceptado por SMTP» con «entregado».

**Criterio de aceptación:** reiniciar el servicio no pierde pendientes ni duplica mensajes ya confirmados; dos operadores no envían el mismo caso a la vez; corregir un correo habilita una recuperación concreta.

## Auditoría de los recorridos de producto

| Pantalla | Mejora propuesta | Resultado esperado |
|---|---|---|
| Ingreso y primera configuración | Checklist de maestro, plantilla, proveedor y prueba de conexión; modo demo explícito | El nuevo usuario sabe qué falta antes de enviar |
| Dashboard | Fecha de corte visible, actualización de datos, listas accionables y detalle de cada indicador | Pasar de mirar montos a decidir el trabajo de hoy |
| Nuevo envío | Separar importación, revisión y campaña; mostrar remitente, exclusiones, estimación y alcance | Confirmación informada y menos envíos accidentales |
| Seguimiento | Buscar, ordenar, filtrar, guardar vistas; tabla compacta con panel lateral | Encontrar y procesar 500 casos sin recorrer cientos de tarjetas |
| Maestro | Convertirlo en Clientes; búsquedas, contacto principal/secundario, administradora y responsable | Un centro de relación, no solo una agenda de mails |
| Perfil | Actividad cronológica, comunicaciones, documentos, tareas, promesas y movimientos de saldo | Resolver el caso sin saltar entre pantallas y Gmail |
| Plantilla | Vista previa con datos reales del caso, versión y prueba a destinatario controlado | Saber exactamente qué se enviará |
| Configuración | Estado por cuenta, última sincronización exitosa, fallos y remitente activo | Diferenciar credenciales guardadas de integración saludable |

La prioridad visual debe estar en búsqueda, densidad útil, consistencia, estados de carga/error y móvil. Animaciones más vistosas, colores nuevos o un tablero Kanban no resuelven por sí mismos la gestión pendiente. Las tarjetas actuales pueden mantenerse como vista alternativa; para trabajo repetitivo conviene una tabla con filtros y selección.

## Casos límite que debe cubrir el upgrade

| Caso | Cobertura actual / riesgo | Comportamiento objetivo |
|---|---|---|
| Firma con una imagen, sin comprobante | Reproducido: se clasifica como PAGO | Tratar como respuesta; adjunto candidato con revisión |
| Responde texto y varios días después manda comprobante | El watcher selecciona solo NO_CONTESTADO al iniciar el barrido | Incorporar todos los mensajes nuevos del hilo y conservar su secuencia |
| Responde a un recordatorio de hace 45 días | La ventana actual de envíos elegibles es de 30 días | Política visible y sincronización por mensaje pendiente, no solo antigüedad |
| Respuesta sin In-Reply-To o References | No hay coincidencia directa | Cola de mensajes sin vincular y asociación manual, sin asignación arriesgada |
| Pago equivocado o parcial | No hay reversión ni importe conciliado en el flujo actual | Movimiento financiero trazable y corrección con motivo |
| Varios consorcios comparten una administradora | Un solo correo por cliente, sin entidad de administradora | Contactos relacionados y comunicación por consorcio o agrupada según política |
| Dos facturas del mismo cliente | Dedupe conserva la última fila | Regla según el significado de la fila; nunca perder importes accidentalmente |
| Se importa un archivo parcial o viejo | Ausencias pueden quedar saldadas | Fecha de corte y alcance; sin saldado automático en carga parcial |
| Nuevo ciclo mientras el anterior sigue enviando | Falta una coordinación durable de campañas | Bloqueo o regla explícita de transición; finalizar o pausar lo anterior |
| Doble clic, timeout y reintento de confirmación | Riesgo de campaña duplicada; no reproducido con concurrencia | Identificador único de operación y confirmación recuperable |
| El cliente se da de baja después de entrar en la cola | El lote preparado puede quedar desactualizado | Revalidación de la baja justo antes del envío |
| Cambio de cuenta dentro del mismo proveedor | Envio conserva proveedor, no identidad inmutable del buzón | Asociar cada mensaje a la cuenta concreta y mantener su seguimiento |
| Nuevas respuestas tardías con el mismo conteo | El aviso descartado se identifica por cantidad | Marcar lectura por evento/usuario, no por número total |
| API lenta o caída | Algunas pantallas confunden fallo de carga con lista vacía | Carga, vacío y error diferentes; reintento y datos previos identificados |
| Acceso desde teléfono o solo teclado | Ver anexo de inspección visual | Navegación adaptable, foco y acciones completamente alcanzables |

## Qué tomar de los CRM open source

La comparación es de patrones aplicables. No implica que una instalación estándar de esos productos ya haga cobranza por Excel ni conciliación para este negocio.

| Referente | Capacidad documentada | Qué incorporaría aquí | Límite de la comparación |
|---|---|---|---|
| Twenty | Empresas, personas, tareas, notas, filtros y vistas de registros; extensibilidad | Ficha unificada, navegación por objetos, búsquedas y vistas guardadas | Adaptar el modelo de cobranza exige trabajo; no sustituye el motor específico por defecto |
| SuiteCRM | Workflows con condiciones, acciones y restricciones de ejecución repetida | Reglas transparentes: si una promesa vence, crear tarea; no repetir sin control | Su amplitud requiere configuración y simplificación para un operario |
| Frappe CRM | Comunicaciones, asignaciones, seguimiento, vistas guardadas y uso móvil | Cronología de actividad y trabajo asignado, con buena continuidad entre dispositivos | Su orientación comercial no define por sí sola la conciliación de deuda |
| EspoCRM | Correos relacionados, calendario, casos, roles, entidades personalizadas y exportación | Caso de cobranza, permisos por rol, registro de cambios y exportabilidad | Reportes y automatización aparecen bajo Advanced Pack; no asumir todo incluido en el núcleo |

Fuentes: [Twenty](https://twenty.com/), [SuiteCRM Workflows](https://docs.suitecrm.com/admin/administration-panel/workflow/), [Frappe CRM](https://frappe.io/crm), [EspoCRM Features](https://www.espocrm.com/features/). Consultadas el 13/09/2026. La conveniencia para este proyecto es una evaluación propia.

## Comparación de diseño y completitud con Twenty

Twenty sirve como referencia por la continuidad de sus interacciones: buscar, filtrar, abrir un registro sin perder la lista y acceder a su información relacionada. La comparación visual usa la demostración pública de su web; no es una prueba de una instalación autenticada ni una certificación de su accesibilidad. Las capacidades se contrastaron con su [guía oficial de layout](https://docs.twenty.com/getting-started/core-concepts/layout).

| Dimensión | Esta aplicación hoy | Patrón documentado en Twenty | Adaptación propuesta para cobranza |
|---|---|---|---|
| Navegación | Estados de correo en el menú y nuevamente en solapas | Objetos y favoritos | Hoy, Clientes, Cobranza, Campañas, Informes; estados como vistas |
| Encontrar un registro | Lectura de listas; falta buscador en Maestro | Búsqueda transversal | Buscar consorcio, clave, administradora o email desde cualquier pantalla |
| Tablas | Columnas fijas y pocas operaciones | Agrupación, edición y columnas configurables | Vista por responsable, saldo, antigüedad y próxima acción |
| Filtros | Principalmente estado y ciclo | Vistas con filtros y orden guardados | «Promesas vencidas», «Sin contacto válido», «Comprobantes pendientes» |
| Detalle rápido | Panel con datos y fragmento de respuesta | Panel lateral conectado a ficha completa | Resolver o abrir cliente sin perder posición ni filtros |
| Ficha completa | Historial de ciclos y gráfico | Pestañas y widgets relacionados | Contactos, deuda, actividad, documentos y tareas reunidos |
| Trabajo diario | No hay agenda del cobrador | Tareas y notas vinculadas a registros | Próxima acción obligatoria en un caso abierto |
| Atajos | Interacción centrada en clics | Menú de comandos Cmd/Ctrl+K | Buscar y abrir casos por teclado; mantener acciones explícitas |
| Representación | Tarjetas por estado y tablas separadas | Tabla, Kanban y calendario | Tabla como vista principal; calendario de compromisos; Kanban solo si ayuda |

La brecha de diseño más importante es funcional: Twenty organiza una misma entidad a través de varias vistas coherentes; esta aplicación obliga a reconstruir el contexto entre envío, seguimiento y maestro. Su sobriedad visual ya es compatible con una evolución de ese tipo. Conservaría la paleta azul puerto y adoptaría mayor consistencia de cabeceras, barras de herramientas y paneles.

No copiaría todos los objetos comerciales ni construiría inmediatamente un editor de layouts. Tampoco usaría arrastrar una tarjeta a «Pagado» como confirmación financiera. El diseño objetivo puede tener la continuidad de Twenty y seguir siendo mucho más sencillo en opciones.

## Anexo de UI: revisión independiente y evidencia visual

Evaluación A: diseño y recorrido. Evaluación B: evidencia DOM, accesibilidad y viewport. Ambas se realizaron por separado con pestañas propias y sin modificar datos. Convergen en la necesidad de búsqueda, simplificación del flujo de envío y editor de correo con vista previa.

- **P1, móvil confirmado:** a 390 × 844, la barra lateral ocupa 240 px y el área principal queda en unos 135 px, antes del padding. Dashboard y Maestro resultan recortados. La navegación debe colapsar y los controles adaptarse al espacio.
- **P1, teclado confirmado:** las filas que abren perfiles desde Dashboard no ofrecen enlace/botón accesible por teclado. Las tarjetas de Seguimiento sí implementan activación con Enter/Espacio; conservar ese acierto.
- **P1, nombres accesibles:** seis controles visibles de Plantilla no tienen etiqueta asociada en el DOM. Asociar etiquetas y campos; validar lectura y errores con teclado y lector de pantalla.
- **P1, contexto de campaña:** «Nuevo Envío» puede mostrar simultáneamente un texto previo a confirmar, mails enviados y la acción «Reenviar todos». Separar nueva campaña de recuperación del ciclo existente.
- **P2, editor:** Plantilla expone HTML y variables sin vista previa. El operador necesita ver el mail, editar texto y comprender el filtro de monto como criterio de campaña.
- **P2, recuperación:** el dashboard falló en algunas visitas del navegador y cargó en otras; las consultas HTTP directas dieron 200. Es una incidencia observada de causa no aislada, no un fallo persistente demostrado. El producto necesita reintento contextual y carga parcial aunque el origen sea transitorio.

Evaluación heurística cualitativa A, escala 0 deficiente a 4 excelente: visibilidad 2; lenguaje del usuario 2; control y libertad 2; consistencia 3; prevención 2; reconocimiento 3; eficiencia 2; estética/minimalismo 3; recuperación 2; ayuda 2. Total orientativo 23/40. No es una medición objetiva de satisfacción ni se asignó una puntuación comparable a Twenty, que no se probó en las mismas condiciones.

El operario experto encuentra fricción al buscar y actuar por lotes; el nuevo usuario debe deducir qué Excel cargar y qué significa «Pago»; quien usa teclado pierde acceso a filas navegables; en móvil la estructura limita la lectura. El recorrido empieza ordenado, pero pierde continuidad al resolver excepciones y cerrar casos.

Capturas reales de la aplicación acompañan el informe visual. No se hicieron pruebas con usuarios, medición formal de contraste ni auditoría completa con lector de pantalla. El detector automático de Impeccable no pudo arrancar porque su motor no estaba instalado y su caché no era escribible; se usaron capturas, DOM, árbol accesible y fuente. No interpretar esa limitación como un resultado limpio.

## Construir, integrar o migrar

**Evolución de esta aplicación — recomendada ahora.** Conserva el trabajo probado y el flujo del operario. La empresa asume desarrollar tareas, contactos, permisos y trazabilidad; el beneficio es mantener una herramienta acotada al problema real.

**CRM externo más motor de cobranza especializado — candidato si crece el equipo.** Permite aprovechar contactos, tareas y actividad de un CRM. Requiere definir una única fuente de verdad por entidad y resolver sincronización, permisos y fallos entre dos sistemas. No dejar que ambos editen el mismo saldo.

**Migración total — posponer hasta una prueba de ajuste.** Antes de elegir plataforma, reproducir con los mismos 50 clientes: importación y bajas, promesa de pago, adjunto falso, respuesta tardía y conciliación parcial. Evaluar exportación, actualizaciones, extensiones, operación y licencia vigente. Sin esa prueba no hay fundamento para prometer menor costo o plazo.

## Qué aporta revisar el repositorio de Twenty

El [repositorio público](https://github.com/twentyhq/twenty) presenta una plataforma extensible, no solo una pantalla de CRM. Su README declara React y TypeScript en la interfaz, NestJS, PostgreSQL, Redis y BullMQ en el servidor, además de herramientas para definir aplicaciones y objetos. La [guía de aplicaciones](https://docs.twenty.com/developers/extend/apps/getting-started/quick-start) ofrece una ruta de extensión que merece una prueba antes de optar por un fork.

Tres niveles de aprovechamiento:

1. **Patrones de interacción:** adoptarlos en el producto actual —vistas, búsqueda, detalles contextuales— requiere menos acoplamiento y es mi primera recomendación.
2. **Componentes:** `twenty-ui` es un candidato a evaluar, no un reemplazo automático de los componentes actuales. Primero probar una tabla, un panel y el tema en una rama aislada; comparar dependencias, accesibilidad y costo de mantener dos sistemas visuales. Puede ser más simple implementar esos patrones con los componentes ya existentes.
3. **Plataforma:** realizar una prueba de una aplicación de cobranza sobre Twenty con consorcios, compromisos y tareas, dejando al motor actual la importación especializada. Elegir esa vía solo si elimina suficiente trabajo de CRM sin volver frágil la sincronización.

El archivo [LICENSE vigente en main](https://github.com/twentyhq/twenty/blob/main/LICENSE) distingue un núcleo mayormente AGPLv3, archivos Enterprise bajo licencia comercial y paquetes MIT —incluidos `twenty-ui` y el toolkit indicado allí—. También describe una excepción para aplicaciones que usan sus interfaces. Esto hace necesario revisar el paquete y versión concretos antes de reutilizar código; «el repo es open source» no describe una licencia uniforme. Es una lectura del repositorio, no una conclusión sobre la licencia de un producto derivado todavía inexistente.

No se clonó ni se desplegó Twenty ni se evaluaron todos sus módulos. Se revisaron README, licencia, manifiestos y documentación de interacción/extensión; el análisis de reutilización es una propuesta de validación, no una compatibilidad demostrada.

## Adaptar Twenty conservando la esencia de esta aplicación

**Sí, es técnicamente viable.** Dado el interés explícito en tener el CRM completo y su estética, la siguiente validación recomendada es una aplicación de cobranza sobre Twenty que reutilice el motor actual de Excel y correo. Esta recomendación de prueba complementa la evolución gradual: todavía no justifica reemplazar la aplicación operativa.

Twenty permite definir objetos, relaciones, vistas, navegación, páginas de detalle, componentes React y lógica propia mediante su [sistema de aplicaciones](https://docs.twenty.com/developers/extend/apps/getting-started/quick-start). La [navegación configurable](https://docs.twenty.com/getting-started/core-concepts/layout) permite ocultar opciones que no se usan. Es adecuado para presentar un CRM acotado a cobranza, aunque esa simplicidad requiere diseñar y probar los recorridos del operador.

| Parte del producto | Adaptación propuesta |
|---|---|
| Clientes, administradoras y contactos | Registros relacionados en Twenty, con una fuente de edición definida |
| Tareas, notas y actividad | Aprovechar las capacidades del CRM y vincularlas al caso |
| Excel de maestro y deudores | Conservar el asistente especializado, cruce, reglas y revisión previa |
| Campañas, plantillas, mínimo de deuda y exclusiones | Módulo propio de cobranza visible dentro del CRM |
| Envío y reintentos | Un único motor de envío, inicialmente el actual con las correcciones del informe |
| Respuestas, rebotes y comprobantes | Eventos vinculados al cliente y a la campaña; comprobante separado de pago confirmado |
| Saldo y pagos parciales | Fuente contable identificada y conciliación propia, sin dos sistemas editando el mismo saldo |

El operador podría seguir el recorrido **Subir Excel → revisar destinatarios → enviar → gestionar respuestas**, dentro de una navegación sencilla: Hoy, Clientes, Cobranza, Campañas e Informes. Los detalles avanzados quedarían en configuración. La integración debe aspirar a una sola experiencia y resolver autenticación, permisos y errores; conectar dos servidores no lo garantiza por sí solo.

La documentación describe [envíos automáticos desde cuentas conectadas](https://docs.twenty.com/user-guide/workflows/capabilities/send-emails-from-workflows), pero eso no demuestra que reproduzcan nuestras campañas, bajas, clasificación y reintentos. Su [página de composición](https://docs.twenty.com/user-guide/calendar-emails/how-tos/can-i-send-emails-from-twenty) contiene afirmaciones inconsistentes sobre composición nativa y funciones futuras; hay que verificar la versión instalada antes de depender de ellas. La importación [admite Excel y CSV según la documentación](https://docs.twenty.com/user-guide/data-migration/capabilities/file-formats), pero no incorpora automáticamente el cruce maestro/deudores ni la interpretación de ciclos de esta aplicación.

**La maleabilidad es alta para el modelo y las vistas; la integración especializada requiere desarrollo; modificar profundamente el núcleo aumenta el costo de actualizaciones.** Por eso probaría una extensión antes que un fork. Tampoco presentaría un cambio de colores como adopción de un CRM completo.

Prueba de ajuste propuesta: instancia local aislada, versión fijada, los mismos 50 clientes, una importación completa y otra parcial, campaña simulada, respuesta seguida de comprobante, rebote, corrección de correo, promesa y pago parcial. Primero correo simulado; cualquier prueba con destinatarios reales requiere autorización de envío. La salida debe demostrar equivalencia del flujo actual, ausencia de duplicados, evidencia de pago separada y un recorrido comprensible para el operador. La compatibilidad sigue pendiente hasta completar esa prueba.

## Modelo funcional objetivo: entidades y operación

- **Consorcio y administradora:** organizaciones relacionadas. La relación puede cambiar con vigencia y conservar historia.
- **Contacto:** persona con uno o varios canales y su función. Preferencias por contacto/canal separadas de la existencia del cliente.
- **Caso de cobranza:** deuda gestionada, prioridad, responsable, próxima acción y estado de gestión.
- **Snapshot de saldo / documento de deuda:** evidencia importada con fecha y origen. Si no se dispone de facturas y vencimientos, llamar a la antigüedad «observada desde»; no presentarla como vencimiento contractual.
- **Comunicación:** mensaje entrante/saliente, cuenta, hilo, destinatarios, intentos y adjuntos. No representa un pago.
- **Pago y aplicación:** importe, fecha, estado de revisión y vínculo con la deuda. Un comprobante es evidencia candidata.
- **Tarea / compromiso:** responsable, fecha, estado y resultado. Motor de la bandeja «Hoy».
- **Evento de auditoría:** actor, fecha, antes/después y motivo. Incluye automatismos y correcciones.

Mantendría una aplicación modular con una base relacional y un trabajador de cola persistente. Para este tamaño no hay una razón demostrada para distribuir todo en microservicios. Archivos fuera del disco efímero del servidor, con permisos; integración de correo vinculada por cuenta; métricas de última sincronización, cola y errores. OAuth puede reducir la fricción de contraseñas de aplicación, pero requiere evaluar permisos y operación del proveedor antes de adoptarlo.

## Secuencia recomendada y cómo aceptar cada entrega

| Entrega | Alcance | Comprobación de salida | Esfuerzo relativo |
|---|---|---|---|
| 1. Confianza del dato | Separar comprobante/pago, reporte de importación, alcance completo/parcial, fecha de corte | Ninguna fila omitida silenciosamente; PDF no cancela deuda; carga parcial no salda | Medio–alto |
| 2. Operación fiable | Campañas e intentos persistentes, recuperación, evitar duplicados, cuenta e historial de mensajes | Reinicio y reintento sin pérdida; baja respetada; correo corregido recuperable | Alto |
| 3. CRM mínimo de cobranza | Clientes/contactos, responsable, tareas, notas, compromisos y bandeja Hoy | Un caso puede pasar de contacto a promesa, revisión y cierre con trazabilidad | Alto |
| 4. Productividad | Búsqueda, filtros guardados, acciones por lote, móvil y accesibilidad | Casos representativos resueltos con teclado y teléfono; lotes con resumen de resultado | Medio |
| 5. Escala e integración | Conciliación con fuente contable, cuentas adicionales, reglas y reporting | Saldo reconciliado con fuente; fallos visibles; permisos y restauración probados | Alto, depende de integraciones |

El esfuerzo es una comparación cualitativa, no una cotización. Antes de poner fechas hay que definir responsable de conciliación, fuentes disponibles, volumen, usuarios y alcance de correo. No construiría todavía un editor genérico de automatizaciones, un módulo comercial de oportunidades ni IA que decida si se pagó. Primero reglas explícitas y acciones revisables.

## Métricas del producto y pruebas de aceptación

Medir tiempo por caso gestionado, promesas vencidas sin seguimiento, comprobantes pendientes de revisión, porcentaje de contactos utilizables y tiempo de recuperación de fallos. Medir cobros confirmados solo cuando exista una fuente de confirmación. La reducción entre dos Excel puede incluir ajustes y no demuestra el efecto causal de los mails.

Antes de usar automatizaciones sin supervisión: probar duplicados y filas inválidas, archivo parcial, doble confirmación, reinicio durante un lote, baja con mensaje en cola, cambio de cuenta, texto seguido de adjunto, respuesta tardía, pago parcial, reversión y dos operadores simultáneos. Probar el ciclo completo con destinatarios controlados y comprobar acceso a evidencias. Registrar fecha, entorno y resultado; mantener el dataset demo separado de datos reales.

## Decisiones de negocio que condicionan el CRM

¿La administradora es el contacto comercial o solo el canal de cobro? ¿Quién confirma la acreditación? ¿El Excel informa saldo por cliente o facturas con vencimiento? ¿Cuántas personas gestionarán la cartera? ¿Qué promesa suspende el siguiente recordatorio? ¿Se necesita gestionar mantenimiento, contratos o reclamos además de deuda?

La recomendación actual supone que el primer objetivo sigue siendo la cobranza y que el sistema de facturación permanece como fuente del saldo. Si el alcance incluye toda la relación comercial y el servicio técnico, la evaluación de integración con un CRM existente gana peso.
