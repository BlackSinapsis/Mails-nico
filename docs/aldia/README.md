# Plan de Aldia

Esta rama es el plan de Aldia, copiado para que se pueda leer acá y, más adelante, moverlo a [OrderByte01/aldia](https://github.com/OrderByte01/aldia).

La implementación no arranca desde esta rama. Julián revisa primero.

La conversación completa del agente que armó este plan está en [cursor.com/agents/bc-e3888865-dbcf-40ea-ad14-c88145c1b21c](https://cursor.com/agents/bc-e3888865-dbcf-40ea-ad14-c88145c1b21c).

## Por dónde empezar

- [Mapa](mapa-wayfinder.md): el recorrido, las reglas y lo que ya está cerrado.
- [Lista para hacer](lista-para-hacer.md): qué puede tomar un agente, y qué hacen Julián y Juan a mano.

## Tickets

Cada archivo está en [wayfinder/issues/](wayfinder/issues/). En cada línea: número, título, estado, y qué lo bloquea. Los números que no aparecen no tienen ticket.

- 01. [Filas, clave repetida y tope del Excel](wayfinder/issues/01-filas-clave-repetida-y-tope.md) — abierto — nada lo bloquea
- 02. [Diff del maestro](wayfinder/issues/02-diff-del-maestro.md) — abierto — nada lo bloquea
- 03. [Fecha de corte](wayfinder/issues/03-fecha-de-corte.md) — abierto — nada lo bloquea
- 04. [Escapar el HTML del mail](wayfinder/issues/04-escapar-el-html-del-mail.md) — abierto — nada lo bloquea
- 05. [La firma no es un pago](wayfinder/issues/05-la-firma-no-es-un-pago.md) — abierto — nada lo bloquea
- 06. [Seguir a quien contestó](wayfinder/issues/06-seguir-a-quien-contesto.md) — abierto — nada lo bloquea
- 07. [Baja por POST](wayfinder/issues/07-baja-por-post.md) — abierto — nada lo bloquea
- 08. [Pesos y fechas de Argentina](wayfinder/issues/08-pesos-y-fechas-de-argentina.md) — abierto — nada lo bloquea
- 09. [Etiquetas, foco y estado visible](wayfinder/issues/09-etiquetas-foco-y-estado-visible.md) — abierto — nada lo bloquea
- 10. [Docs apagados y logs sin datos](wayfinder/issues/10-docs-apagados-y-logs-sin-datos.md) — abierto — nada lo bloquea
- 11. [Render no vuelve a free](wayfinder/issues/11-render-no-vuelve-a-free.md) — abierto — nada lo bloquea
- 12. [Preview de errores en pantalla](wayfinder/issues/12-preview-de-errores-en-pantalla.md) — abierto — lo bloquean [01](wayfinder/issues/01-filas-clave-repetida-y-tope.md), [03](wayfinder/issues/03-fecha-de-corte.md) y [08](wayfinder/issues/08-pesos-y-fechas-de-argentina.md)
- 13. [El logout invalida la sesión](wayfinder/issues/13-el-logout-invalida-la-sesion.md) — abierto — lo bloquea [03](wayfinder/issues/03-fecha-de-corte.md)
- 14. [Guardar el corte sin enviar](wayfinder/issues/14-guardar-el-corte-sin-enviar.md) — abierto — lo bloquean [12](wayfinder/issues/12-preview-de-errores-en-pantalla.md), [13](wayfinder/issues/13-el-logout-invalida-la-sesion.md) y [10](wayfinder/issues/10-docs-apagados-y-logs-sin-datos.md)
- 15. [Cancelar envíos obsoletos](wayfinder/issues/15-cancelar-envios-obsoletos.md) — abierto — lo bloquea [14](wayfinder/issues/14-guardar-el-corte-sin-enviar.md)
- 16. [Pausar recordatorios](wayfinder/issues/16-pausar-recordatorios.md) — abierto — lo bloquean [15](wayfinder/issues/15-cancelar-envios-obsoletos.md) y [02](wayfinder/issues/02-diff-del-maestro.md)
- 17. [Tests de invariantes](wayfinder/issues/17-tests-de-invariantes.md) — abierto — lo bloquea [16](wayfinder/issues/16-pausar-recordatorios.md)
- 18. [Listas honestas y marcar pago](wayfinder/issues/18-listas-honestas-y-marcar-pago.md) — abierto — lo bloquean [15](wayfinder/issues/15-cancelar-envios-obsoletos.md), [16](wayfinder/issues/16-pausar-recordatorios.md) y [09](wayfinder/issues/09-etiquetas-foco-y-estado-visible.md)
- 19. [Dashboard creíble](wayfinder/issues/19-dashboard-creible.md) — abierto — lo bloquean [03](wayfinder/issues/03-fecha-de-corte.md), [16](wayfinder/issues/16-pausar-recordatorios.md), [08](wayfinder/issues/08-pesos-y-fechas-de-argentina.md) y [18](wayfinder/issues/18-listas-honestas-y-marcar-pago.md)
- 20. [Sentry en el plan gratis](wayfinder/issues/20-sentry-en-el-plan-gratis.md) — abierto — lo bloquean [09](wayfinder/issues/09-etiquetas-foco-y-estado-visible.md) y [10](wayfinder/issues/10-docs-apagados-y-logs-sin-datos.md)
- 21. [Neon puede dormir](wayfinder/issues/21-neon-puede-dormir.md) — abierto — lo bloquean [06](wayfinder/issues/06-seguir-a-quien-contesto.md), [10](wayfinder/issues/10-docs-apagados-y-logs-sin-datos.md), [20](wayfinder/issues/20-sentry-en-el-plan-gratis.md) y [27](wayfinder/issues/27-leer-el-panel-de-neon.md)
- 22. [Plantilla, logo y previa](wayfinder/issues/22-plantilla-logo-y-previa.md) — abierto — lo bloquean [04](wayfinder/issues/04-escapar-el-html-del-mail.md) y [23](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md)
- 23. [Rediseño visual y modo oscuro](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md) — abierto — lo bloquean [09](wayfinder/issues/09-etiquetas-foco-y-estado-visible.md) y [20](wayfinder/issues/20-sentry-en-el-plan-gratis.md)
- 24. [CI de pruebas y licencias](wayfinder/issues/24-ci-de-pruebas-y-licencias.md) — abierto — nada lo bloquea
- 25. [Tabla densa de registros](wayfinder/issues/25-tabla-densa-de-registros.md) — abierto — lo bloquean [18](wayfinder/issues/18-listas-honestas-y-marcar-pago.md), [19](wayfinder/issues/19-dashboard-creible.md), [23](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md), [20](wayfinder/issues/20-sentry-en-el-plan-gratis.md) y [16](wayfinder/issues/16-pausar-recordatorios.md)
- 27. [Leer el panel de Neon](wayfinder/issues/27-leer-el-panel-de-neon.md) — lo hace una persona — nada lo bloquea
- 28. [No construir esto](wayfinder/issues/28-no-construir-esto.md) — no se hace — nada lo bloquea
- 29. [Esperar el disparador](wayfinder/issues/29-esperar-el-disparador.md) — en espera — nada lo bloquea
- 30. [PR de documentación](wayfinder/issues/30-pr-de-documentacion.md) — en espera — nada lo bloquea
- 31. [Sistema de movimiento](wayfinder/issues/31-sistema-de-movimiento.md) — abierto — lo bloquea [23](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md)
- 32. [Panel y línea de tiempo](wayfinder/issues/32-panel-y-linea-de-tiempo.md) — abierto — lo bloquean [19](wayfinder/issues/19-dashboard-creible.md), [25](wayfinder/issues/25-tabla-densa-de-registros.md) y [31](wayfinder/issues/31-sistema-de-movimiento.md)
- 33. [Menú de comandos](wayfinder/issues/33-menu-de-comandos.md) — abierto — lo bloquean [23](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md) y [25](wayfinder/issues/25-tabla-densa-de-registros.md)
- 34. [Hoy, al lado del dashboard](wayfinder/issues/34-hoy-al-lado-del-dashboard.md) — abierto — lo bloquean [23](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md) y [19](wayfinder/issues/19-dashboard-creible.md)
- 36. [Recortar lo que sobra](wayfinder/issues/36-recortar-lo-que-sobra.md) — abierto — lo bloquean [20](wayfinder/issues/20-sentry-en-el-plan-gratis.md), [25](wayfinder/issues/25-tabla-densa-de-registros.md), [23](wayfinder/issues/23-rediseno-visual-y-modo-oscuro.md) y [33](wayfinder/issues/33-menu-de-comandos.md)
- 37. [Ensayar los dos cortes](wayfinder/issues/37-ensayar-los-dos-cortes.md) — lo hace una persona — lo bloquean [04](wayfinder/issues/04-escapar-el-html-del-mail.md), [05](wayfinder/issues/05-la-firma-no-es-un-pago.md), [07](wayfinder/issues/07-baja-por-post.md), [14](wayfinder/issues/14-guardar-el-corte-sin-enviar.md), [15](wayfinder/issues/15-cancelar-envios-obsoletos.md), [16](wayfinder/issues/16-pausar-recordatorios.md), [18](wayfinder/issues/18-listas-honestas-y-marcar-pago.md) y [19](wayfinder/issues/19-dashboard-creible.md)
- 38. [Workflow de Cloudflare Pages](wayfinder/issues/38-workflow-de-cloudflare-pages.md) — abierto — lo bloquea [24](wayfinder/issues/24-ci-de-pruebas-y-licencias.md)
- 41. [La campaña de 600 ya está medida](wayfinder/issues/41-campana-de-600-medida.md) — cerrado — nada lo bloquea
- 42. [Owner y repo privado vacío](wayfinder/issues/42-owner-y-repo-privado-vacio.md) — lo hace una persona — nada lo bloquea

## El resto de esta carpeta

- [Contexto del proyecto](project-context.md)
- [Decisiones pendientes](decisiones-pendientes.md)
- [Decisiones del grilling (Q15–Q23)](grilling-decisiones-15-23.md)
- [Respuestas de Lavish](respuestas-lavish.md)
- [Buenas prácticas](buenas-practicas.md)
- [Flujo de cobro](flujo-cobro-dos-tipos.md)
- [Plan para la reunión con Juan](plan-para-juan.md)
- [Preguntas para el dueño](preguntas-dueno.md)
- [Formulario para Nico](formulario-nico.md)
- [API y exportes](api-y-exportes.md)
- [Informe de la prueba de punta a punta](e2e-report.md)
