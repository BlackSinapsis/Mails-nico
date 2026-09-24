# Agenda de la reunión

23/09/2026. Q15–Q18, Q20, Q21 y Q23 no se reabren. El mapa es [mapa-wayfinder.md](mapa-wayfinder.md).

Julián cerró el 23/09 los tres choques de interfaz. No están en la votación. Hoy convive con el dashboard. Hay paleta de comandos. «Marcar como pago» es un diálogo, no un toast de deshacer. El detalle está en el brief.

El 24/09/2026 contestó en la página Lavish y cerró la sesión.

## Cerrado el 24/09/2026

### D-01. Repos

Pasar el canónico a una organización. Los dos quedan como admins. Los públicos se archivan después de confirmar el clone. El repo de Juan se deja, porque ya está andando. Este MVP, con los cambios, va a un repo privado donde los dos son admin. Cuando conecte y funcione bien, desconectan el de Juan. Si se puede hacer una organización con los proyectos de los dos, mejor.

### D-04. Techo

Duro en el piloto, y hasta USD 15 si la medición de CU-h no entra. Quiere que Neon pueda dormir. No ve problema en eso, y el techo se puede estirar a 15.

### D-02. Titular

Sociedad, con la práctica que les sirva a los dos.

### D-03. Clave

Seguir con la clave del seed durante el piloto (`operario` / la clave del seed, la que ya está en el piloto). Sigue así hasta que el MVP ande en el repo nuevo y rehacen el login.

### Q22. Soporte

Mejor esfuerzo, sin plazo. Dijo que no aporta nada ahora y que queda para definir.

### Excel

Una fila por cliente. La clave repetida bloquea.

### Neon

Julián anotó 77,44 CU-h desde el 31 de agosto de 2026. Render está en Starter. Siguen sin anotar el gráfico, el storage, la región y si el host lleva `-pooler`. El arreglo del pool espera esos datos. Cloudflare Pages queda para cuando el repo tenga código.

### Frontend

Cloudflare Pages. Lo usan como front y lo despliegan con el CD de GitHub.

### D-27. Celular

También se manda el corte desde el celular. La pantalla es responsive: pensada sobre todo para escritorio, y consultable y visible desde el teléfono.

### D-29. Buenas prácticas

Confirmó el corte de [buenas-practicas.md](buenas-practicas.md). La capa 2 y el modo oscuro quedan aparte de esa espera: sus notas de la misma sesión ya las metieron en este review.

### PR de documentación

Todavía no se abre.

### D-07. AAIP

Piloto corto sin inscripción, y revisar al cerrarlo.

### Envío, deuda y pantallas

Cada lote manda como máximo 150 mails, por Yahoo. No se envían 600. La corrida de 600 queda como medición: sirve para saber.

El abono y los trabajos extra no van separados. Importa cuánto debe el cliente, y el seguimiento según hace cuánto tiempo.

El modo oscuro entra como default. Sigue afuera el resto de la lista: DSO, forecast y cohortes, kanban de gestión, pixel de apertura, portal de pago, informes por IA, notas y tareas como módulo, fork de Twenty, `empresa_id` y Framer Motion.

La capa 1 y la capa 2 entran cuando termine este review. En la capa 1 hay que corregir los errores que hoy ve el operador. En la capa 2 entran las pantallas nuevas y las que ya están, con la UI mejorada y moderna, inspirada en otros CRM. Lo que la página dice que no entra el lunes sigue fuera de ese lunes. Lo que figuraba en paralelo, antes de dar el piloto por cerrado, es parte del e2e.

Guardar y enviar siguen siendo dos actos. Se confirma antes de enviar. La confirmación de envío es manual.

La conexión con el programa de facturación espera a Nico. Hay que averiguar la plataforma. El formulario para el dueño de ese sistema está en [formulario-nico.md](formulario-nico.md).

El manual o el video corto se hace cuando el MVP esté listo para que el cliente sepa usarlo.

## Sigue abierto

| | Pregunta | Opciones | Recomendación | Qué cambia en el mapa |
| --- | --- | --- | --- | --- |
| [cssutils](#cssutils) | ¿La excepción LGPL de `cssutils` vive hasta la reventa? | Excepción hasta la primera entrega a otra empresa. Reemplazar el inliner antes del piloto. Aceptar LGPL también en el artefacto que se entrega. | Excepción fechada en el CI. Reemplazar antes de la primera reventa. | [CI](wayfinder/issues/24-ci-de-pruebas-y-licencias.md) lleva esa única excepción. El reemplazo está en [Esperar el disparador](wayfinder/issues/29-esperar-el-disparador.md). |
| [Segunda empresa](#segunda-empresa) | Cuando haya otro cliente, ¿otra instancia o una sola base? | Otra instancia (otro Render, otra base, el mismo artefacto). Un VPS con una base por cliente. Una sola base con `empresa_id`. | Otra instancia mientras sean pocos. No se agrega `empresa_id`. | Nada del piloto ni de la experiencia. Está en [No construir esto](wayfinder/issues/28-no-construir-esto.md). |

## cssutils

LGPL, por `premailer`. No obliga a publicar esta app por usarla en el servidor. Estorba el día que se entregue un instalable a otra empresa. El piloto convive con la excepción.

## Segunda empresa

Q7: un solo cliente. Cuando exista el segundo, otra base y otra clave Fernet. Un VPS compartido sólo si alguien opera parches y restores.

## No reabrir

Filas inválidas, pausa, selección, cancelar pendientes, diff del maestro, poll de 10 minutos, fecha de corte. Fork de Twenty, no. De Twenty, ideas, y en la fase de experiencia los comportamientos nombrados en el mapa, con librerías permisivas.
