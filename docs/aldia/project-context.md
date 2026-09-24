# Contexto del proyecto Mails-nico

## Objetivo

- Llevar la app que ya funciona en producción a un producto enterprise, a medida del cliente actual (empresa de mantenimiento de ascensores que cobra a consorcios).
- Adaptar lo mejor de CRM y apps de cobranza del mercado (Twenty, Attio, HubSpot, Upflow y otros), sólo como ideas.
- La experiencia del operario tiene que parecerse a esos productos: más funcionalidad que el mínimo del piloto, una UI claramente más moderna y animaciones con criterio. La integridad de la deuda sigue primero. Quedan afuera DSO, portal de pago, tracking de aperturas y reportes por IA.
- Que el proyecto sirva para aprender y practicar cómo se construye y opera un producto enterprise.

## Modelo de negocio

- Cobro estimado al cliente: unos USD 50 por mes, que cubren el uso de la app, el mantenimiento y el soporte de Juan y Julián.
- Se van a ir agregando funcionalidades con el tiempo.
- Producto cerrado y revendible a otras empresas más adelante.

El producto se llama Aldia, sin tilde. El repo privado, cuando exista, es `OrderByte01/aldia`. El dueño importa primero la lista completa de clientes y, cada unos 15 días, un archivo de deudores con un monto por cliente y un mail. El lunes 2026-09-28 es el MVP de integridad de ese ciclo: el sistema que ya funciona, robustecido para que el saldo no mienta. El manual o el video corto, en castellano simple, queda para cuando ese MVP se pueda usar. El detalle del ciclo está en [flujo-cobro-dos-tipos.md](flujo-cobro-dos-tipos.md).

## Lo que Julián cerró el 24/09/2026

El canónico pasa a una organización, con Juan y Julián como admins. El repo de Juan sigue andando. Este MVP, con los cambios, va a un repo privado de los dos. Cuando conecte y funcione, desconectan el de Juan. Si pueden armar una organización con los proyectos de los dos, mejor. Los públicos se archivan después de confirmar el clone.

El código queda en sociedad, con la práctica que les sirva a los dos. La clave del seed sigue durante el piloto, hasta que el MVP corra en el repo nuevo y rehacen el login.

Durante el piloto el techo sigue duro, y puede llegar a USD 15 si la medición de CU-h no entra. Julián quiere que Neon pueda dormir. Esa medición la anota él antes de tocar el pool, y sigue pendiente. El front va a Cloudflare Pages y se despliega con el CD de GitHub. En el teléfono la UI es responsive, pensada primero para el escritorio, y desde ahí también se manda un lote.

El Excel trae una fila por cliente. Una clave repetida bloquea. Cada envío tiene un tope de 150 mails, por Yahoo. La corrida de 600 queda como medición.

Abono y trabajos extra siguen juntos. Se anota cuánto debe el cliente y hace cuánto. La confirmación de envío sigue a mano. Capa 1 y capa 2 entran al terminar este review. El modo oscuro queda como default. Lo demás de lo que estaba afuera sigue afuera. Confirmó el corte de buenas-practicas.md, y la capa 2 y el modo oscuro ya entran con este review.

Si algo queda trabado, el soporte es mejor esfuerzo y sin plazo. El piloto corto no inscribe la base. Lo revisan al cerrarlo. El PR de documentación no se abre todavía.

La conexión con facturación espera a Nico. Las preguntas para el dueño de esa plataforma están en [formulario-nico.md](formulario-nico.md). El registro completo está en [decisiones-pendientes.md](decisiones-pendientes.md).

## Restricciones

- Infraestructura barata pero confiable. Techo duro en el piloto: USD 10 por mes, y hasta USD 15 si la medición de CU-h no entra.
- Datos de la empresa: manejo seguro, bases bien diseñadas, backups y restauración probada.
- Licencias: de Twenty sólo ideas; dependencias con licencia permisiva (MIT, Apache-2.0, BSD).
- El canónico pasa a una organización. El repo de Juan (`Juanrocod/Mails-nico`) sigue hasta que el privado conecte y funcione.

## Documentos relacionados

- [Decisiones del grilling](grilling-decisiones-15-23.md)
- [Decisiones pendientes](decisiones-pendientes.md)
- [Formulario para Nico](formulario-nico.md)
- [Mapa Wayfinder](mapa-wayfinder.md)
- Estrategia enterprise
- Evaluación de infraestructura
- Auditoría de seguridad
- Auditoría ponytail
