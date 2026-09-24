# Mapa Wayfinder — Aldia

Label: `wayfinder:map` · Tracker: markdown en [`wayfinder/issues/`](wayfinder/issues/)

## Destino

El producto se llama Aldia, sin tilde. El operador carga la lista de clientes una vez y, cada unos 15 días, un archivo de deudores con un monto y un mail por cliente. Guardar el corte y enviar son dos actos. El envío se confirma a mano, por Yahoo, con un tope de 150. El lunes 2026-09-28 ese ciclo, el que ya corre, tiene que dejar de mentir en el saldo. En este mismo recorrido entran la capa 1 y la capa 2: las pantallas nuevas y las que ya están, con una UI moderna de CRM y el modo oscuro por defecto.

## Notas

Decisiones cerradas: [decisiones-pendientes.md](decisiones-pendientes.md), [respuestas-lavish.md](respuestas-lavish.md), [flujo-cobro-dos-tipos.md](flujo-cobro-dos-tipos.md), [project-context.md](project-context.md). El formulario para Nico ya está en [formulario-nico.md](formulario-nico.md). Los pasos de Julián y de Juan están en [lista-para-hacer.md](lista-para-hacer.md).

Estándares que un ticket de código tiene que cumplir: [buenas-practicas.md](buenas-practicas.md), el corte que Julián confirmó (D-29). Entran ahora las filas de «Entra ahora»: caso de uso fuera del router, invariantes con test, fecha de corte, errores con fila, columna, valor y motivo, docs apagados, logs sin datos personales, Sentry en el plan gratis, baja por POST, `formatPesos` y fechas de Argentina, etiquetas y foco, TanStack Query en las listas que se toquen, Zod y React Hook Form en el próximo formulario que se toque. Licencias nuevas: MIT, Apache-2.0, BSD o ISC. `cssutils` sigue como excepción fechada hasta la primera reventa.

D-29 deja la capa 2 y el modo oscuro fuera de la columna «se practica cuando dispare». Esas dos entran en este mapa. El pase de teléfono también: la pantalla se piensa para escritorio y desde el celular se puede mirar y mandar el lote (D-27).

Reglas que ningún ticket rompe. El preview no escribe. 5 mails cada 30 segundos. El merge no pisa `prefiere_no_recibir_email`. El historial no se borra. Un comprobante no acredita el saldo. Una fila por cliente. La clave repetida bloquea y no se suma. No se parte el abono del trabajo extra.

**Cómo se toma un ticket.** El detalle está en el archivo. `Type`, `Status` y `Blocked by` quedan en inglés. `Archivos` es la lista exclusiva de lo que ese ticket puede escribir. Se puede leer el resto del repo.

Frontera: `Status: open`, sin `Asignado`, y cada número de `Blocked by` con `Status: resolved`. `humano`, `espera` y `no-hacer` no se toman. Dos agentes toman los dos de número más bajo que cumplan eso, cada uno en su worktree. Esos dos no comparten archivos. Antes de editar código, el agente pone `Status: claimed` y `Asignado`.

No se pushea a [OrderByte01/aldia](https://github.com/OrderByte01/aldia) ni se toca `Juanrocod/Mails-nico` desde un ticket. Aldia, cuando Julián lo cree, queda vacío y no es un fork. El código de la app no se renombra en este recorrido de planificación.

## Decisiones hasta ahora

- [D-01](decisiones-pendientes.md): la organización [OrderByte01](https://github.com/OrderByte01) ya existe. Las dos cuentas figuran en People. Falta confirmar la etiqueta Owner y crear [OrderByte01/aldia](https://github.com/OrderByte01/aldia), privado, vacío y sin ser un fork. Sin push y sin tocar `Juanrocod/Mails-nico`. El producto se llama Aldia. Pasos en [lista-para-hacer.md](lista-para-hacer.md).
- [D-02](decisiones-pendientes.md): el código queda en sociedad. La práctica elegida es esa organización, con los dos como Owner.
- [D-03](decisiones-pendientes.md): sigue la clave del seed hasta que Aldia corra en [OrderByte01/aldia](https://github.com/OrderByte01/aldia) y rehacen el login.
- [D-04](decisiones-pendientes.md): Neon tiene que poder dormir. El techo sigue duro y puede llegar a USD 15 si los CU-h no entran. Julián anota la medición antes de tocar el pool.
- [D-07](decisiones-pendientes.md): piloto corto, sin inscripción en AAIP. Se revisa al cerrarlo.
- [D-27](decisiones-pendientes.md): también se manda el corte desde el celular. Escritorio primero. Desde el teléfono se consulta y se ve.
- [D-29](buenas-practicas.md): Julián confirmó ese corte. La capa 2 y el modo oscuro entran con este review.
- [Excel](decisiones-pendientes.md): una fila por cliente. La clave repetida bloquea.
- [Envío](respuestas-lavish.md): como máximo 150 mails por vez, por Yahoo. La corrida de 600 queda como medición. Guardar y enviar siguen separados. La confirmación es manual.
- [Deuda](flujo-cobro-dos-tipos.md): un monto y un mail. El abono y los trabajos extra no se separan.
- [Frontend](decisiones-pendientes.md): Cloudflare Pages, desplegado con el CD de GitHub. El API sigue en Render.
- [Capa 1 y capa 2](respuestas-lavish.md): las dos entran al terminar este review. Oscuro por defecto. El resto de lo que estaba afuera sigue afuera.
- [Facturación](formulario-nico.md): la conexión espera a Nico. El formulario ya está escrito.
- [PR de documentación](decisiones-pendientes.md): todavía no.
- [Manual](respuestas-lavish.md): manual o video corto cuando el MVP se pueda usar.
- [Q22](decisiones-pendientes.md): mejor esfuerzo, sin plazo. No se define ahora.
- [La campaña de 600 ya está medida](wayfinder/issues/41-campana-de-600-medida.md): SQLite local, 84 min 59 s de reloj, piso de 59 min 30 s. No es un envío ni una lectura de CU-h.
- Q15 a Q18, Q20, Q21 y Q23 no se reabren. El detalle está en [grilling-decisiones-15-23.md](grilling-decisiones-15-23.md).

## Sin especificar todavía

- La región, el storage, si el gráfico cae a cero y si el host lleva `-pooler`. Los CU-h desde el 31 de agosto de 2026 son 77,44 y Render está en Starter. El arreglo del pool espera el resto.
- Lo que conteste el dueño del programa de facturación. Las preguntas ya están en el formulario.
- La causa de los tres huecos de 339 s, 625 s y 635 s en la corrida de 600. No hay una línea de log en el medio. No se le inventa una causa en el aviso de tiempo.
- El canal y el plazo de soporte, cuando Q22 les importe.

## Fuera de alcance

El detalle de lo que no se construye está en [No construir esto](wayfinder/issues/28-no-construir-esto.md). Lo que espera un hecho concreto está en [Esperar el disparador](wayfinder/issues/29-esperar-el-disparador.md).

Queda afuera de este recorrido: partir abono y trabajos, varias facturas como deudas distintas, sumar filas repetidas, la API de facturación, mandar 600 mails, el PR de documentación, la inscripción en AAIP, cambiar la clave del seed, el arreglo del pool antes de la medición, el manual o el video, y el resto de la lista vieja (DSO, forecast, cohortes, kanban, pixel, portal de pago, informes por IA, notas y tareas como módulo, fork de Twenty, `empresa_id`, Framer Motion). El modo oscuro no está en esa lista: entra como default.
