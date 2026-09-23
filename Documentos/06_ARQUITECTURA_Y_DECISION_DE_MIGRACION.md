# Arquitectura y decisión de migración

Fecha: 13/09/2026. Decisión provisional: no reemplazar todavía la aplicación; cerrar reglas y comparar una extensión de Twenty contra mejorar la aplicación actual. No es una aprobación de migración.

## Opciones reales

| Opción | Qué se aprovecha | Trabajo que sigue siendo propio | Costo/riesgo dominante | Ajuste actual |
|---|---|---|---|---|
| A. Evolucionar aplicación y adoptar patrones de Twenty | Flujo actual, historial y operación conocidos | Cortes fiables, dashboard, búsqueda, contactos/tareas simples y UI | Mantener capacidades propias de CRM | Primera opción para alcance acotado y pocos operadores |
| B. Twenty como CRM + módulo de cobranza integrado | Entidades, relaciones, tareas, vistas y estética nativa | Importación quincenal, comparaciones, campañas, métricas y enlace de mensajes | Integración, permisos, consistencia, versiones y operación | Candidato si ahorra trabajo real de CRM y la prueba mantiene simplicidad |
| C. Reconstruir todo dentro de Twenty | Una plataforma para CRM y lógica propia | Reescribir reglas/migración y garantizar equivalencia del correo | Mayor cambio inicial y dependencia de capacidades/versiones | No elegir sin demostrar ventajas sobre B |
| D. Fork profundo de Twenty | Libertad de modificar interfaz y núcleo | Resolver divergencias, actualizaciones y mantenimiento | Costo recurrente y acoplamiento | Descartado como punto de partida |

La opción B es técnicamente plausible gracias al [sistema de apps](https://docs.twenty.com/developers/extend/apps/getting-started/quick-start) y sus [API](https://docs.twenty.com/developers/extend/api). La compatibilidad del flujo completo todavía no fue probada. El repositorio es maleable, pero no convierte automáticamente la lógica de cobranza en funcionalidades estándar.

## Arquitectura mínima común a las opciones A y B

Facturación → archivo de corte → validación/borrador → aceptación → saldos históricos y comparación → dashboard/ficha → preparación de campaña → envío y seguimiento → gestión.

La aceptación del corte y la autorización de campaña son límites distintos. El correo trabaja en una cola persistente con intentos trazables. El historial sigue disponible aunque el proveedor de correo falle. Una sola aplicación modular y una base relacional bastan para A; no hay motivo demostrado para microservicios.

Si se elige B, el backend actual puede evolucionar a un servicio de cobranza detrás de la UI de Twenty. Esto agrega un límite de integración que debe justificarse por el ahorro en CRM. Una app con componentes dentro del CRM suele dar más continuidad que un enlace que abre otra aplicación; hay que comprobar qué superficies de extensión admite la versión fijada. Un iframe o dos logins separados no cuentan como integración terminada.

## Propiedad de los datos en B

| Dato | Dueño propuesto | Qué ve el otro sistema |
|---|---|---|
| Identidad externa | Clave de facturación con equivalencia a ID del CRM | Mapeo estable; no emparejar por nombre |
| Contactos y administradoras | Twenty, si se adopta como maestro operativo | Motor recibe versión/identificador y destinatario aprobado |
| Archivo, corte y saldos | Módulo de cobranza | Proyección de lectura para fichas y vistas del CRM |
| Campaña, intento, message_id y resultado | Un solo motor de correo | Actividad vinculada a cliente/campaña |
| Tarea, nota y compromiso | CRM, con relaciones al episodio | Reglas de suspensión y próxima acción consultables |
| Preferencia de no contacto | Un registro canónico compartido por integración | Revalidación inmediata antes del envío |

No permitir que ambos sistemas editen libremente el saldo, el destinatario y la baja. Definir transacciones locales, publicación durable de cambios, identificadores de eventos y reintentos sin duplicación. Si no hace falta sincronización inmediata, puede empezar con una integración pequeña y comprobable; no diseñar un bus de eventos genérico.

## Condiciones que deciden si migrar

**Elegir A** si tareas, notas, búsqueda y ficha resuelven el trabajo, hay pocos operadores y Twenty obliga a sostener dos experiencias o demasiada integración.

**Elegir B** si contactos relacionados, trabajo en equipo y vistas reutilizables tienen demanda real; la app de cobranza encaja sin modificar el núcleo; y se demuestra que mantener esa integración cuesta menos que construir y mantener las capacidades necesarias en A.

**Posponer la decisión** si todavía no sabemos qué columnas trae el export real o las pruebas no reproducen los cierres/reapariciones. Cambiar de plataforma antes de acordar las reglas solo trasladaría las inconsistencias.

No se asignan puntuaciones numéricas ficticias ni ahorro porcentual. El costo debe incluir implementación, migración, infraestructura, soporte, actualizaciones, licencia de funciones necesarias y recuperación de incidentes.

## Prueba de ajuste acotada de Twenty

1. Instancia local aislada con versión fijada y datos ficticios; aplicación actual disponible como referencia.
2. Modelar cliente/contacto, corte y gestión; mostrar una ficha con saldo del corte y actividad separada.
3. Integrar un asistente de importación con preview de cambios y errores. Reutilizar el motor donde tenga sentido.
4. Ejecutar los escenarios AC del documento 07 con envío simulado. Evaluar después un intercambio real controlado solo cuando se autorice.
5. Probar Gmail, un email compartido por varios consorcios, respuesta tardía y comprobante posterior a una respuesta de texto.
6. Probar al operador con permisos mínimos: cargar, revisar, preparar campaña y registrar una gestión sin configurar objetos ni workflows.
7. Comprobar reinicio, reintento, exportación/restauración de datos y una actualización de la plataforma compatible con la extensión.
8. Comparar esfuerzo y fricción con una versión equivalente del flujo en A. Documentar diferencias reales, no solo cantidad de pantallas.

Salida: tabla de capacidades demostradas, faltantes, dependencias premium y costo de mantenimiento. Si un requisito central falla o exige modificar el núcleo, volver a A o reducir alcance antes de migrar.

## Licencia y operación

La [licencia del repositorio](https://github.com/twentyhq/twenty/blob/main/LICENSE) distingue núcleo AGPL, zonas Enterprise y paquetes MIT; revisar la versión/paquete que se reutilice. El [plan de funciones](https://docs.twenty.com/user-guide/billing/capabilities/pricing-plans) sitúa SSO, permisos por registro y auditoría entre las capacidades premium, y campañas como próximas. No asumir que todo lo visible en el repositorio está disponible gratis para cualquier distribución.

El [autoalojamiento](https://docs.twenty.com/developers/self-host/capabilities/docker-compose) exige operar aplicación, datos persistentes y backups. La prueba debe incluir almacenamiento de Excel/adjuntos, configuración de correo, claves de cifrado, actualizaciones y restauración, además de la interfaz. No se hizo una conclusión jurídica ni una cotización de infraestructura.

## Migración del historial si se decide avanzar

- Copiar y verificar el origen antes de transformar; conservar IDs/relaciones y conciliar conteos y montos por ciclo y cliente.
- Convertir cada ciclo antiguo en un corte histórico de procedencia limitada. Su fecha disponible es la carga: marcarla como aproximación, no inventar fecha de facturación.
- Extraer saldos de todos los estados, incluidos filtrados y sin email. Separar los atributos del mail del saldo.
- Migrar PAGO antiguo como clasificación/evidencia histórica no verificada; preservar su valor original para auditoría.
- Conservar `saldado_en` como inferencia histórica y reconstruir transiciones con los cortes disponibles. No presentarlo como fecha exacta de pago.
- Migrar bajas, clientes inactivos, claves sin maestro y mensajes con proveedor/ID. No crear adjuntos o textos completos que nunca se guardaron.
- Marcar los archivos fuente antiguos como no disponibles si no existen. No fabricar huellas ni resultados de validación retroactivos.
- Hacer conciliación antes/después y correr en comparación con envíos deshabilitados. Durante el cambio, mantener un solo emisor de mails.
- Plan de vuelta atrás: conservar el sistema origen y exportar las nuevas gestiones antes de restaurar. No se puede “desenviar” un mail; su registro debe sobrevivir al rollback.
