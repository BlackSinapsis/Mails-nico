# Lista para hacer

El producto se llama Aldia, sin tilde. El mapa está en [mapa-wayfinder.md](mapa-wayfinder.md). Cada nombre de abajo es un ticket en [wayfinder/issues/](wayfinder/issues/).

Dos agentes pueden codear a la vez. Cada uno agarra un ticket en su propio worktree, el abierto de número más bajo que nadie haya marcado `claimed` y cuyos `Blocked by` ya estén `resolved`. Antes de tocar código pone `Status: claimed` y `Asignado`. El ticket lista los archivos que puede escribir. Esos dos no comparten archivos.

## Lo que hacen los agentes

Se pueden tomar ya, de a dos:

- Filas, clave repetida y tope del Excel
- Diff del maestro
- Fecha de corte
- Escapar el HTML del mail
- La firma no es un pago
- Seguir a quien contestó
- Baja por POST
- Pesos y fechas de Argentina
- Etiquetas, foco y estado visible
- Docs apagados y logs sin datos
- Render no vuelve a free
- CI de pruebas y licencias

Cuando se liberan, también de a dos:

- Preview de errores en pantalla, después de las filas, la fecha de corte y los pesos.
- El logout invalida la sesión, después de la fecha de corte.
- Sentry en el plan gratis, después de las etiquetas y los logs.
- Workflow de Cloudflare Pages, después del CI. Solo el archivo del workflow.

- Guardar el corte sin enviar, después del preview, el logout y los logs. Separa guardar de enviar, confirma a mano, corta en 150 por Yahoo y deja mandar el lote desde el teléfono.
- Rediseño visual y modo oscuro, después de las etiquetas y de Sentry. El oscuro queda por defecto. Puede ir junto con guardar el corte: no comparten archivos.

- Cancelar envíos obsoletos, después de guardar el corte.
- Plantilla, logo y previa, después del HTML escapado y del rediseño. Puede ir junto con cancelar.

- Pausar recordatorios, después de cancelar y del diff del maestro.

- Tests de invariantes, después de la pausa. Puede ir junto con las listas.
- Listas honestas y marcar pago, después de cancelar, la pausa y las etiquetas.

- Dashboard creíble, después de las listas, la fecha de corte, la pausa y los pesos.
- Sistema de movimiento, después del rediseño. Puede ir junto con el dashboard.

- Tabla densa de registros, después de las listas, el dashboard, el rediseño, Sentry y la pausa.
- Hoy, al lado del dashboard, después del rediseño y del dashboard. Puede ir junto con la tabla.
- Neon puede dormir, después de los logs, del watcher, de Sentry, y de que Julián haya anotado los CU-h en Leer el panel de Neon. Puede ir junto con la tabla.

- Menú de comandos, después del rediseño y de la tabla.
- Panel y línea de tiempo, después del dashboard, la tabla y el movimiento.

- Recortar lo que sobra, al final, después de Sentry, la tabla, el rediseño y el menú de comandos.

Leer el panel de Neon, Ensayar los dos cortes, No construir esto, Esperar el disparador, el PR de documentación y La campaña de 600 ya está medida no los toma un agente.

## Lo que tiene que hacer Julián a mano

La organización ya existe: [OrderByte01](https://github.com/OrderByte01). Las dos cuentas ya aparecen en People. No hace falta crearla ni mandar otra invitación.

1. Entrá con tu cuenta personal de GitHub a [People de OrderByte01](https://github.com/orgs/OrderByte01/people). GitHub lista ahí a todos, también a los que son Owner. Mirá la etiqueta de tu usuario y la de Juanrocod. Las dos tienen que decir Owner. Owner es el admin. GitHub no tiene un rol Admin. Si alguna fila dice Member, abrí el menú de esa fila y cambiala a Owner. No dejes a ninguno como Member.
2. Los dos siguen entrando con su propia cuenta personal.
3. Creá el repo en [New repository](https://github.com/organizations/OrderByte01/repositories/new). Repository name: `aldia`, para que quede en [OrderByte01/aldia](https://github.com/OrderByte01/aldia). Elegí Private. Dejá sin marcar Add a README, Add .gitignore y Choose a license, para que quede vacío. No lo marques como fork. No importes `Juanrocod/Mails-nico` ni `BlackSinapsis/Mails-nico`. No pases a privado un repo público que ya es fork: mientras siga en la red de forks, GitHub no lo deja hacer privado.
4. No hagas push. [OrderByte01/aldia](https://github.com/OrderByte01/aldia) queda vacío.
5. No abras ni cambies `Juanrocod/Mails-nico`. No toques el deploy de Render ni el de Cloudflare de ese repo.

Cuando Juan te pase los números del panel de Neon, anotalos en [Leer el panel de Neon](wayfinder/issues/27-leer-el-panel-de-neon.md): CU-h del período, si el gráfico cae a cero o es una recta, la región, y si el host de la connection string lleva `-pooler`. Recién con esa nota se puede cambiar el pool. No lo cambies vos en el panel.

Pasale a Nico [formulario-nico.md](formulario-nico.md), para el dueño del programa de facturación. La conexión no se construye hasta que contesten.

Dejá la clave del seed (`operario` / la clave del seed, la que ya está en el piloto) como está. Se cambia cuando Aldia corra en [OrderByte01/aldia](https://github.com/OrderByte01/aldia) y rehacen el login.

No abras el PR de documentación. No inscribas la base en AAIP: el piloto es corto y lo revisan al cerrarlo. No armes horario de soporte. El manual o el video corto lo hacen cuando el MVP se pueda usar.

El ensayo con el operador, los dos primeros cortes y un lote chico, es [Ensayar los dos cortes](wayfinder/issues/37-ensayar-los-dos-cortes.md). Esperá a que esos tickets estén cerrados. No manden 600 mails.

## Lo que tiene que hacer Juan a mano

Juan tiene la cuenta de Neon, la de Render y Cloudflare Pages.

1. Entrá con Juanrocod a [People de OrderByte01](https://github.com/orgs/OrderByte01/people). Tu fila tiene que decir Owner. Si dice Member, no la dejes así: Julián la cambia a Owner en esa misma pantalla. Seguís entrando con Juanrocod.
2. No entres a editar `Juanrocod/Mails-nico`. No cambies el repo conectado en Render ni en Cloudflare.

Neon, en [console.neon.tech](https://console.neon.tech), el proyecto de producción:

3. Abrí el proyecto. En el dashboard, o en Monitoring / Usage, leé los CU-h del período de facturación y las fechas de ese período. Anotá si la curva de compute se cae a cero o se queda plana. Anotá también el storage.
4. Anotá la región que muestra el proyecto (Settings, o el encabezado del proyecto).
5. Apretá Connect y mirá el host de la connection string. Anotá si contiene `-pooler`. No aprietes reset password. No cambies el compute. No desactives el suspend / scale to zero. No edites la connection string que ya usa Render.
6. Pasale esos cuatro datos a Julián: CU-h, forma del gráfico, región, y si el host lleva `-pooler`.

Copia, antes del primer corte real:

7. En Connect, copiá la connection string directa, la del host sin `-pooler` si las dos están a la vista.
8. En tu máquina, `pg_dump` de esa URL a un archivo. Cifralo y guardalo fuera de la laptop.
9. En el proyecto, Create branch (una branch nueva, no la de producción). Restaura el dump ahí. Comprobá que podés contar clientes, cortes y envíos, y que el login responde. Anotá cuánto tardó. No restaures encima de la branch de producción.

Render, en [dashboard.render.com](https://dashboard.render.com):

10. Abrí el servicio web que hoy despliega `Juanrocod/Mails-nico`.
11. Settings, Build & Deploy. El repositorio tiene que seguir diciendo `Juanrocod/Mails-nico`. No aprietes Connect ni cambies la rama.
12. En Settings, mirá el Instance Type. Anotá si dice Free o Starter. No guardes un cambio de plan en este paso. Si dice Free, avisale a Julián y pará: un blueprint con `plan: free` puede volver a bloquear el SMTP. No apliques el `render.yaml` del repo mientras diga `plan: free`.

Cloudflare queda para después. No crees el proyecto de Pages ni desconectes el que ya está. Cuando Julián diga que hay que desplegar Aldia y [OrderByte01/aldia](https://github.com/OrderByte01/aldia) ya tenga código:

13. [dash.cloudflare.com](https://dash.cloudflare.com), Workers & Pages, Create, Pages, Connect to Git.
14. Autorizá la org OrderByte01 si te lo pide. Elegí `OrderByte01/aldia`. No elijas `Juanrocod/Mails-nico`.
15. Root directory: `frontend`. Build command: `npm run build`. Build output directory: `dist`.
16. Variable de entorno `VITE_API_URL` con la URL pública del backend en Render, sin barra al final.
17. Cuando el deploy de Pages responda, en el servicio de Render agregá esa URL de Pages a `ALLOWED_ORIGINS`. Dejá la URL vieja hasta que el corte nuevo se haya abierto en las dos.
18. Recién ahí, en Render, Settings, cambiá el repo conectado a `OrderByte01/aldia`. En Cloudflare, desconectá el proyecto que construía `Juanrocod/Mails-nico`.
19. El subdominio `api` que apunte al backend va en DNS only, nube gris. No actives el proxy naranja delante del SSE.
20. No pases el front a Vercel Pro. Cuando Pages responda, este uso comercial deja de estar en Vercel Hobby.
