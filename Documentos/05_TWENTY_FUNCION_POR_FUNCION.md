# Twenty: qué aporta a este producto y qué sería excesivo

Fecha de consulta: 13/09/2026. Evaluación funcional de las familias documentadas, no certificación de todos los módulos de una instalación. “Ahora” significa dentro del upgrade prioritario, no que ya esté implementado. Las recomendaciones son nuestra evaluación de ajuste al negocio.

## Criterio de selección

Una función entra si reduce errores de los cortes, facilita encontrar y entender una deuda, permite gestionarla o preserva comunicaciones. No entra únicamente porque Twenty la incluya. El recorrido cotidiano debe seguir siendo cargar Excel, revisar cambios, preparar mails y resolver excepciones.

## Datos y trabajo del operador

| ID | Capacidad documentada | Uso concreto propuesto | Decisión y condición |
|---|---|---|---|
| T01 | Organizaciones y contactos [F1] | Consorcios, administradoras y personas responsables | Ahora; identidad del consorcio por clave de facturación |
| T02 | Objetos/campos personalizados [F1] | Corte, saldo por cliente, episodio, campaña y compromiso | Necesario si se adopta Twenty; reglas específicas por desarrollar |
| T03 | Relaciones entre registros [F1] | Una administradora atiende varios consorcios; varios contactos por consorcio | Ahora, con una asociación simple; vigencias históricas si hay cambios reales |
| T04 | Tareas y notas [F1] | “Llamar el viernes”, aclaración de deuda, responsable | Ahora; fecha y estado, sin gestión compleja de proyectos |
| T05 | Campos de archivo [F1] | Excel fuente y comprobante | Ahora para trazabilidad, con permisos y conservación definidos |
| T06 | Campos libres/extensibilidad [F1] | Campos adicionales específicos del negocio | Solo los necesarios; evitar que el operador deba diseñar su base |
| T07 | Oportunidades comerciales [F1] | Captación/venta de servicios | Fuera del alcance inicial de cobranza |

## Interfaz y productividad

| ID | Capacidad documentada | Uso concreto propuesto | Decisión y condición |
|---|---|---|---|
| T08 | Búsqueda transversal [F2] | Encontrar clave, consorcio, administradora o contacto | Ahora; alto valor incluso con 50 clientes |
| T09 | Vistas guardadas y favoritos [F2] | “Reaparecieron”, “Sin email”, “Promesas vencidas” | Ahora; entregar vistas predefinidas antes de pedir configurarlas |
| T10 | Tablas con columnas, orden y filtros [F2] | Ver importe, cambio, fecha de corte y próxima acción | Ahora; mostrar pocas columnas útiles por defecto |
| T11 | Panel lateral y ficha completa [F2] | Abrir cliente sin perder filtro ni posición | Ahora; saldo, contexto y una acción relevante |
| T12 | Menú reordenable/ocultable [F3] | Hoy, Clientes, Cortes, Campañas; Informes como vista o sección secundaria | Ahora si se usa Twenty; ocultar módulos no utilizados |
| T13 | Tema claro/oscuro y atajos [F3] | Comodidad y uso intensivo | Conveniente; después de corregir accesibilidad y estados de error |
| T14 | Kanban [F2] | Seguimiento de gestiones | Opcional posterior; una tabla cubre el trabajo inicial; mover a “Pagado” no cambia saldo |
| T15 | Calendario [F2] | Fechas de promesa y tareas | Después de incorporar compromisos; no exige sincronizar toda la agenda personal |
| T16 | Editor de páginas con widgets [F2] | Ficha diseñada para cobranza | Usarlo como herramienta de configuración, no exponérselo al operador en cada tarea |

## Importación, comunicación, métricas y automatización

| ID | Capacidad documentada | Uso concreto propuesto | Decisión y condición |
|---|---|---|---|
| T17 | Importar archivos, mapear campos y validar [F4] | Ayudar con formatos y errores | Mantener asistente propio de corte; importar filas genéricas no resuelve ausencia, fecha ni rectificación |
| T18 | Historial de correo [F5] | Leer conversación y comprobantes en contexto | Alto valor; probar asociación correcta cuando una administradora representa varios consorcios |
| T19 | Envíos desde workflows [F6] | Recordatorios personalizados | Capacidad candidata; conservar inicialmente un único motor especializado y probar equivalencia |
| T20 | Campañas nativas [F7] | Reemplazar la campaña actual | No basar la migración en esto: la página de planes las presenta como premium y próximas |
| T21 | Triggers manuales/programados y condiciones [F8] | Avisar que falta Excel, tarea por rebote o promesa vencida | Incorporar pocas reglas explícitas; sin enviar automáticamente porque se creó una fila |
| T22 | Paneles, filtros y agregaciones [F9] | Mostrar cortes y cambios de cartera | Útiles como presentación; los cálculos entre cortes necesitan lógica/proyecciones específicas |
| T23 | API y webhooks [F10] | Conectar motor de cobranza e importación con el CRM | Necesarios para integración; idempotencia, permisos, errores y recuperación propios |
| T24 | Apps, componentes y lógica propia [F11] | Asistente Excel y acciones de campaña dentro de Twenty | Ruta preferida de evaluación antes de modificar el núcleo |
| T25 | Sincronización de calendario [F5/F12] | Reuniones con administradoras | Posponer salvo necesidad demostrada; no necesaria para importar o cobrar |

## Administración y funciones que no justifican sobrecargar el MVP

| ID | Capacidad documentada | Uso concreto propuesto | Decisión y condición |
|---|---|---|---|
| T26 | Roles y permisos [F13] | Separar configuración, lectura y operación de cobranza | Básico ahora si hay varios usuarios; probar que el operador pueda actuar sin ser administrador |
| T27 | Permisos por registro, SSO y auditoría premium [F7/F13] | Carteras restringidas/equipo grande | No exigirlos para un operador; evaluar costo si aparecen esos requisitos |
| T28 | Autoalojamiento [F14] | Control de datos e instalación local | Viable, con costo de operación, backups, archivos, correo y actualizaciones |
| T29 | IA, agentes y enriquecimiento [F12] | Resumir respuestas o proponer siguiente acción | Posterior y asistido; no decidir pagos ni enviar sin reglas y revisión definidas |
| T30 | Varios espacios de trabajo [F7] | Ofrecer el producto a varias empresas | Fuera del alcance inicial; no confundir con varios consorcios de una misma cartera |

## Tres límites relevantes encontrados

**Correo y consorcios.** La guía de Twenty describe asociación de emails a People/Companies/Opportunities, y advierte limitaciones para objetos personalizados; en Companies utiliza dominio. Una administradora puede compartir dirección o dominio entre varios consorcios. Nuestra inferencia: hay que probar vinculación por destinatario, cliente y mensaje; no asumir que el CRM conoce a qué deuda corresponde cada conversación. Un Caso de Cobranza personalizado puede necesitar un componente propio o una relación con contactos. [F5]

**Permisos frente a simplicidad.** La documentación señala que disparar workflows manuales requiere actualmente permiso de gestión de workflows. Esto puede chocar con un operador que solo debe “Enviar recordatorios”. Debe probarse una acción específica de la app con permisos limitados; no resolverlo dando administración total. Los permisos por registro son premium según la guía. [F13]

**Versión y edición.** La documentación de composición de mail contiene secciones inconsistentes sobre funciones actuales y futuras. Además, la página de planes distingue funcionalidades gratuitas de premium y enumera campañas como próximas. Fijar una versión y comprobar su comportamiento; no prometer una migración completa apoyándose en una captura comercial. [F7/F15]

## Problemas relacionados que sí podrían aportar valor

- **Cambios de administradora:** conservar contactos anteriores, vigencia y nuevo destinatario para no mandar el reclamo a quien dejó de gestionar el consorcio.
- **Deuda discutida:** nota/caso con motivo, responsable y próxima revisión; suspender recordatorios por un plazo definido, manteniendo el saldo del Excel.
- **Promesa incumplida:** tarea al vencimiento y evidencia de seguimiento. Un nuevo corte sin deuda cierra la gestión de forma explicable.
- **Correo rebotado o ausente:** bandeja de corrección con acción para actualizar contacto y preparar intento válido; no perpetuar una lista sin salida.
- **Un contacto gestiona muchos consorcios:** vista por administradora. Un mail consolidado sería una fase posterior porque exige reglas de confidencialidad, selección y conciliación; no es necesario para el primer upgrade.
- **Reclamo por servicio que afecta el cobro:** relación simple con un caso de atención y pausa temporal. No construir un sistema de mantenimiento, inventario o rutas técnicas sin una demanda concreta.

## Recomendación de UI aplicada

El aspecto de Twenty aporta sobriedad, tablas consistentes y contexto persistente. El objetivo es que se vea y se use como un CRM cuidado, conservando un vocabulario de cobranza. Una ficha debe responder: cuánto figuraba al corte, qué cambió, qué se habló y qué hacer ahora. La estructura propuesta usa un solo buscador, tabla principal, panel lateral y estados claros de carga, vacío, error y éxito. En móvil el menú se contrae; las acciones y etiquetas deben funcionar por teclado.

No se necesita replicar un catálogo de objetos, un editor libre de automatizaciones, ventas, marketing, IA y múltiples espacios para lograrlo. Tampoco alcanza con copiar colores: la consistencia de datos y recorridos es parte del diseño.

## Recorrido propuesto, llevado a pantallas

1. **Hoy:** último corte y su fecha; aviso de próxima carga; tres listas prioritarias: contacto por corregir, comprobantes por revisar y tareas/promesas vencidas. Acción principal “Importar corte”.
2. **Importar corte:** seleccionar archivo y confirmar fecha. El sistema propone la hoja/columnas conocidas; muestra el mapeo solo si detecta un cambio o error. Progreso, mensaje de error específico y posibilidad de volver sin perder el borrador.
3. **Revisar cambios:** total de cartera y conciliación; pestañas “Aparecen”, “Continúan”, “Regularizados” y “Errores”. Distinguir primeras apariciones de reapariciones. Ver el cliente desde un panel sin abandonar la revisión. Acción principal “Guardar corte”.
4. **Preparar recordatorios:** destinatarios elegibles, excluidos con motivo, remitente y vista previa de un mail. Dos salidas claras: “Enviar recordatorios” o “Terminar sin enviar”. La configuración avanzada queda fuera del camino habitual.
5. **Campaña:** estado persistente de pendientes, enviados y fallidos, con reintento permitido solo sobre datos vigentes. Recargar la página recupera el estado de la operación.
6. **Cliente:** arriba saldo y fecha del corte; debajo cambio observado y continuidad. Actividad ordenada con mails, notas y promesas. Acción contextual: corregir contacto, revisar documento o registrar próxima tarea. Volver conserva búsqueda, filtros y posición.

Los pasos 2–4 pueden vivir en un mismo asistente. La separación de responsabilidades no exige multiplicar páginas ni pedir al usuario que entienda la arquitectura. El diseño visual definitivo debe validarse con un prototipo y el operador antes de implementar una migración.

## Fuentes oficiales consultadas

- [F1 — Modelo de datos](https://docs.twenty.com/getting-started/core-concepts/data-model).
- [F2 — Layout, vistas, búsqueda y fichas](https://docs.twenty.com/getting-started/core-concepts/layout).
- [F3 — Navegación y preferencias](https://docs.twenty.com/user-guide/layout/capabilities/navigation).
- [F4 — Formatos de importación](https://docs.twenty.com/user-guide/data-migration/capabilities/file-formats).
- [F5 — Asociación del correo a objetos](https://docs.twenty.com/user-guide/calendar-emails/how-tos/can-i-track-email-activity-on-all-objects).
- [F6 — Envíos mediante workflows](https://docs.twenty.com/user-guide/workflows/capabilities/send-emails-from-workflows).
- [F7 — Ediciones y funciones premium](https://docs.twenty.com/user-guide/billing/capabilities/pricing-plans).
- [F8 — Automatizaciones](https://docs.twenty.com/getting-started/core-concepts/workflows).
- [F9 — Dashboards](https://docs.twenty.com/getting-started/core-concepts/dashboards).
- [F10 — API](https://docs.twenty.com/developers/extend/api).
- [F11 — Aplicaciones y extensiones](https://docs.twenty.com/developers/extend/apps/getting-started/quick-start).
- [F12 — Catálogo de capacidades](https://docs.twenty.com/getting-started/key-features).
- [F13 — Permisos y limitaciones](https://docs.twenty.com/user-guide/permissions-access/capabilities/permissions).
- [F14 — Autoalojamiento](https://docs.twenty.com/developers/self-host/capabilities/docker-compose).
- [F15 — Composición de correo](https://docs.twenty.com/user-guide/calendar-emails/how-tos/can-i-send-emails-from-twenty).

Los nombres de funciones remiten a documentación consultada; disponibilidad exacta, licencia, traducción, accesibilidad y desempeño deben verificarse en la versión elegida. La evaluación no equivale a haber probado esos 30 ítems de extremo a extremo.
