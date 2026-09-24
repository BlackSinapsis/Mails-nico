# Estándares de ingeniería y de uso — Mails-nico

Fecha: 23/09/2026. Código leído: `master` (misma base que `b8d0072`). Reglas de producto: `CLAUDE.md`, `CONTEXT.md`, `PRODUCT.md`, `DESIGN.md`, `.claude/rules/`, `docs/adr/`. Este texto fija cómo se construye y cómo se usa. Los hallazgos de seguridad, el recorte de código y la estrategia de producto siguen en sus documentos; acá se cita el archivo que hay que cambiar.

Un PR se mide contra la checklist del final. La auditoría visual (tipografía, color, densidad) queda en `evaluacion-ui.md`. La prueba de punta a punta queda en `e2e-report.md`.

Licencias de librerías nuevas: MIT, Apache-2.0, BSD, ISC. El allowlist y la excepción de `cssutils` están en `estrategia-enterprise.md` y en [D-09](decisiones-pendientes.md).

## Qué cabe en USD 50

El cliente paga unos **USD 50 por mes** por el uso, el mantenimiento y el soporte de Juan y Julián (`project-context.md`). La infraestructura apunta a USD 10 (Q14, [D-04](decisiones-pendientes.md)). Después de ese piso quedan del orden de USD 40 para el tiempo de los dos: acompañar el corte, arreglar lo que se rompa y sumar funciones de a una. El producto sigue siendo enterprise y revendible. A este precio, enterprise quiere decir tres cosas que el fee alcanza a sostener:

1. **La deuda no miente.** Un corte inválido no se aplica, un mail no se manda dos veces por un doble clic, un adjunto no se cobra como pago acreditado, una baja no la dispara un antivirus.
2. **El soporte entra en el fee.** Sesión por corte, un canal, un runbook y una copia probada. Cada hora de incendio sale de esos USD 40. Lo que ahorra una hora de soporte (un error que el operador puede corregir solo, un log sin cazar datos a mano, Sentry en el plan gratis) entra ahora.
3. **Se puede vender de nuevo.** Repo privado, titular claro, dependencias permisivas, una instancia por cliente cuando haya otro. El segundo cliente paga su propia infra.

El proyecto también sirve para aprender a operar un producto enterprise. Esa práctica se anota y se hace cuando dispara el hecho de la última columna. Implementarla antes gasta el fee en herramienta que este cliente no usa.

| Práctica | Entra ahora | Se practica cuando dispare | Disparador |
| --- | --- | --- | --- |
| Caso de uso fuera del router; una transacción al guardar el corte | Sí | Un módulo de consultas por tabla | Nunca como barrido. La racha de `excel_joiner.py` sí se lee de una vez, porque son cientos de queries en el Excel real |
| Invariantes del corte con un test cada una | Sí | Fuzzer de contrato, schema OpenAPI diff en cada PR, Postgres de CI para enums | El CI existe y dos personas se pisan el contrato |
| Fecha de corte única; el mismo archivo no crea dos ciclos | Sí | Header `Idempotency-Key` como plataforma | Haya una API para otro sistema (ADR-0007) |
| Errores de fila con fila, columna, valor y motivo | Sí | Problem details RFC 9457 con `type` URI y `application/problem+json` | Un segundo cliente consuma la API, o el front necesite tipos de error estables |
| Apagar `/docs` en producción; no loguear email ni token | Sí | `structlog`, programa de CSP y HSTS, revocación fina de JWT | Un incidente o un contrato de reventa lo pida |
| Sentry en el plan Developer (USD 0) | Sí | Cola durable (Procrastinate) y estado «incierto» | Un reinicio de Render duplique un mail, o se revenda ([D-11](decisiones-pendientes.md) sigue postergada) |
| La baja por POST; backup probado una vez | Sí | TOTP, cookie `HttpOnly`, ASVS nivel 2, SOC 2, pentest | Compartan una clave varias personas, o un contrato lo exija |
| Rotar la clave de producción y el manejo de credenciales | No, en pausa (D-03) | El seed sin clave por defecto, cambio en el primer ingreso, un usuario por persona | Julián lo retome; hasta entonces prod sigue con la clave inicial |
| TanStack Query en las listas que hoy muestran «0» si la red falla | Sí | Generar `domain.ts` desde OpenAPI | El contrato deje de moverse |
| Zod + React Hook Form en el próximo formulario que se toque | Sí | Migrar todos los formularios en un PR aparte | — |
| `formatPesos` y fechas en hora de Argentina | Sí | Librería de i18n | Haya un segundo idioma |
| Etiqueta en el login, foco visible, estado con punto y texto, confirmación que dice el efecto | Sí | Certificación WCAG, pase mobile, virtualizar 600 filas, presupuesto de Core Web Vitals en campo | [D-27](decisiones-pendientes.md), o la tabla se mida lenta en la máquina del operador |
| Un test del recorrido falla → corrige maestro → reenvía | Sí | Playwright en cada PR, Vitest de todas las páginas | El paso manual del PR falle dos veces |
| Allowlist de licencias el día que haya CI | Sí | Reemplazar `cssutils` | La primera reventa ([D-09](decisiones-pendientes.md)) |
| Modo oscuro, webfont, bandeja «Hoy», kanban, OAuth | No | Esas pantallas | Después del piloto, y solo si el operador las pidió ([D-19](decisiones-pendientes.md), [D-25](decisiones-pendientes.md)–[D-28](decisiones-pendientes.md)) |

Si Julián no confirma este corte, sigue abierto como [D-29](decisiones-pendientes.md). Hasta entonces, un PR que solo agregue una fila de «se practica cuando dispare» está fuera de alcance.

---

## 1. Backend

Stack vigente: Python 3.12, FastAPI, SQLAlchemy 2, Pydantic v2, Alembic, pytest. SQLite en tests y dev; PostgreSQL (Neon) en producción. El código corre en los dos.

### 1.1 Capas

Entra ahora sacar la escritura de `confirmar_ciclo` del router. Un repositorio por modelo es práctica de aprendizaje: no hay un segundo equipo ni un límite de agregados que lo pague.

Tres costuras, y solo se escribe la tercera cuando una consulta se repite o esconde una invariante.

| Capa | Hace | No hace |
| --- | --- | --- |
| Router (`app/routers/`) | HTTP, auth, código de estado, abrir el archivo subido | Reglas de corte, SQL de negocio, SMTP |
| Caso de uso (`app/services/`) | Una operación del operador, una transacción, las invariantes | `HTTPException`, armar HTML de respuesta |
| Consultas | Filtros reutilizados (último envío por clave, ciclo activo) | Un módulo por tabla que solo reexpone `session.get` |

Hoy el router ya delega el parseo y el cruce (`excel_parser`, `excel_joiner`, `ciclo_service`), y `get_db` solo abre y cierra la sesión (`backend/app/core/database.py`). El caso de uso de confirmar no está ahí: `confirmar_ciclo` en `backend/app/routers/ciclos.py` desactiva el ciclo anterior, marca saldados, inserta el ciclo y los envíos, hace `commit` y después dispara el SMTP. Ese bloque es el caso de uso. Al separar «guardar corte» de «enviar campaña» (Q11), el router queda en dos endpoints y la escritura pasa a `ciclo_service`.

La primera consulta que merece salir del bucle es la racha. `join_deudores` carga el maestro de una vez (`ClienteMaestro.clave_union.in_(claves)`) y después llama a `_ciclos_consecutivos_deudor` por clave (`excel_joiner.py`). Con un Excel de ~600 filas son cientos de queries. Una sola lectura del último `Envio` por clave reemplaza ese bucle. Recién esa función justifica un módulo de consultas de envíos, compartido con `dashboard_service`.

No se agrega un repositorio por modelo en un PR aparte. Es una capa que nadie llama.

### 1.2 Modelo e invariantes

`CONTEXT.md` sigue siendo el glosario, sin detalles de implementación. El código que puede romper una regla vive junto al modelo, en una función pura testeable.

Invariantes que el piloto tiene que poder enunciar en un test, no solo en un comentario:

- Hay un solo ciclo activo. Aceptar otro lo desactiva en la misma transacción.
- Un `FILTRADO` tiene `motivo_filtrado`. Un `NO_CONTESTADO` no lo tiene.
- Transiciones de comunicación: `NO_CONTESTADO` → `CONTESTADO` | `PAGO` | `REBOTADO`; `CONTESTADO` → `PAGO` solo por el operador. El resto se rechaza. Hoy `POST` de override en `ciclos.py` chequea el salto a mano (`Solo se permite CONTESTADO → PAGO`); la misma tabla tiene que usarla el watcher.
- `PAGO` es un adjunto inferido. No escribe `saldado_en` ni cambia el saldo del corte. El saldo lo cambia el corte siguiente (ausencia = regularizado), no el mail.
- `prefiere_no_recibir_email` no vuelve a `false` por un Excel. La reactivación es una acción explícita.
- La clave de unión normalizada es 8 dígitos. El monto es `Decimal` / `Numeric(12, 2)`, nunca `float`.
- Excluir (monto mínimo, baja, pausa, sin email, no seleccionado) no modifica saldo ni racha.
- El preview no escribe. Sigue siendo cierto en `preview`; deja de serlo el día que un endpoint de «borrador» guarde sin esa distinción en el nombre.

Estados nuevos del piloto (`PAUSADO`, `NO_SELECCIONADO`, `cancelado por nuevo corte`) se agregan al enum de PostgreSQL con `ALTER TYPE … ADD VALUE` en una migración propia, y al literal de `frontend/src/types/domain.ts` en el mismo PR. SQLite en tests no tiene ese enum nativo: el test cubre la transición en Python y la migración se prueba contra PostgreSQL cuando el CI tenga un servicio, o se documenta el límite en el PR.

`EstadoEnvio` hoy mezcla comunicación (`NO_CONTESTADO`), exclusión (`FILTRADO`, `SIN_EMAIL`) y una inferencia de cobro (`PAGO`). Se mantiene así en el piloto. Separar comprobante, gestión y saldo es [D-14](decisiones-pendientes.md), después del piloto.

### 1.3 Transacciones e idempotencia

`get_db` no hace `commit`. Cada caso de uso termina en un `commit` o deja que el `close` revierta. Un caso de uso que escribe a medias y sigue (el `commit` de `confirmar_ciclo` y después el stream SMTP) parte el corte en dos momentos: la cartera ya cambió y los mails todavía no salieron. Eso es correcto solo si son dos casos de uso. Dentro de cada uno:

- Guardar corte: un `commit` al final. Si algo falla, el ciclo anterior sigue vigente.
- Enviar un mail: persistir el intento, hablar con SMTP, persistir el resultado. Un mail confirmado no se reabre porque el siguiente falle. El rate limit (5 cada 30 segundos, ADR-0002) vive en este caso de uso y no se saltea en tests de integración que hablen con SMTP real. Los tests que no envían inyectan el transporte.

Idempotencia, en este orden:

1. La fecha de corte es única. Aceptar dos veces el mismo corte no crea dos ciclos (hoy `Ciclo.numero = count + 1` en `confirmar_ciclo` sí puede).
2. El mismo archivo y la misma fecha, repetidos, devuelven el corte ya aceptado.
3. Reenviar exige ciclo activo, `saldado_en` nulo, y que no haya `message_id` de un envío ya aceptado por el servidor. El hueco de «el SMTP aceptó y el proceso murió» es [D-11](decisiones-pendientes.md): en el piloto no se reintenta solo.

El botón de confirmar se deshabilita al enviar. El servidor igual rechaza el duplicado: el navegador no es la única puerta.

### 1.4 Errores, OpenAPI y paginación

Entra ahora el cuerpo con `errores[]` (fila, columna, valor, motivo): el operador corrige el Excel sin llamar a Juan. El sobre completo de [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) (`type` como URI, `application/problem+json`, negociación de contenido) es la forma que se adopta el día que un segundo cliente consuma la API. Hasta entonces el mismo JSON puede ir como `application/json`, modelado con Pydantic, sin un paquete nuevo. FastAPI todavía no trae el RFC como default (el soporte nativo está propuesto).

Ejemplo de fila inválida, que es el error que el operador va a ver:

```json
{
  "type": "https://mails-nico.local/problems/fila-invalida",
  "title": "El archivo tiene filas que no se pueden importar",
  "status": 422,
  "detail": "Corregí estas filas en el Excel y volvé a subirlo.",
  "errores": [
    {"fila": 14, "columna": "monto", "valor": "abc", "motivo": "no es un importe"}
  ]
}
```

Hoy `HTTPException(detail=str(e))` en `ciclos.py` y `maestro.py` aplana eso a un string. El frontend no puede armar la tabla de errores ni ofrecer la descarga (Q15). Los `type` se documentan una vez y no cambian de texto entre releases: el cliente muestra `title` y `detail`; el código mira `type`.

Validación de request de Pydantic sigue en 422, con el mismo sobre, y la lista `detail` actual de FastAPI pasa a `errores` para no tener dos formas.

OpenAPI (`/openapi.json`) describe los endpoints. En producción se apagan `/docs`, `/redoc` y el schema público. Guardar el schema en el repo y fallar el CI si cambia es la práctica de la tabla de arriba, para cuando dos personas se pisen el contrato. Hasta entonces, `domain.ts` y el backend se actualizan en el mismo PR.

Paginación con cursor: se practica cuando una lista se mida lenta o el historial pese en la respuesta. El ciclo activo de ~600 envíos sigue en una sola respuesta. Dashboard y antigüedad se calculan en SQL (`dashboard_service`), no cargando filas en el cliente: eso sí entra ahora, porque un KPI mal agregado es una hora de soporte.

### 1.5 Configuración

`Settings` en `backend/app/core/config.py` ya lee el entorno con pydantic-settings. Reglas:

- Un secreto vive en el entorno del proceso o cifrado en `configuracion_sistema`. Nunca en el repo, en un default del código ni en el log.
- `YAHOO_EMAIL` y `YAHOO_APP_PASSWORD` son obligatorios en `Settings` aunque el operador ya los carga en Configuración. Pasarlos a opcionales: si faltan en el entorno y faltan en la base, el caso de uso de envío falla con un problem `credenciales-ausentes`, no el proceso al importar `Settings`.
- `ACCESS_TOKEN_EXPIRE_HOURS` y el ejemplo del `.env` dicen lo mismo. Hoy el código usa 8 horas y el ejemplo habla de 24 para el refresh (auditoría de seguridad, F4).
- Prod y dev usan `SECRET_KEY` y `ENCRYPTION_KEY` distintas. Cambiar `ENCRYPTION_KEY` deja las contraseñas de aplicación ilegibles: el caso de uso lo captura (`InvalidToken`) y pide cargarlas de nuevo.

### 1.6 Logging

El formato JSON de `logging_config.py` se mantiene. Cada línea de negocio lleva `envio_id` o `ciclo_id`, el resultado y la duración. No lleva email, nombre, monto, `Message-ID` ni el path de `/unsubscribe/{token}`.

Hoy se rompe en dos lugares: `smtp_sender.py` loguea `envio.email` y `message_id`, y `RequestLoggingMiddleware` loguea `request.url.path` completo, que en la baja incluye el token. El access log de gunicorn repite esa URL. El arreglo es loguear la ruta de la ruta (`/unsubscribe/{token}`), no el valor.

Un identificador de request (header que entra o uno generado) se agrega al log de la request que ya existe. `structlog` es práctica de aprendizaje: el formatter JSON actual alcanza hasta que leer logs de Render cueste más de una sesión de soporte. Sentry en el plan gratis sí entra: un stack del watcher ahorra esa sesión y cuesta USD 0.

### 1.7 Migraciones

Cadena única `0001` → `0006`, y el próximo archivo es `0007`. No se edita una revisión ya aplicada. `entrypoint.sh` corre `alembic upgrade head` en cada deploy: una migración que falle deja el servicio caído, así que cada revisión se prueba en SQLite (el `upgrade` de los tests o un paso del CI) antes de mergear.

- `batch_alter_table` en cambios de columnas, para SQLite y PostgreSQL.
- Un valor nuevo de enum de PostgreSQL va en su propia revisión, con el `downgrade` explícito sobre lo que se puede revertir. Borrar un valor de enum no se promete.
- Expandir y contraer: una columna nueva entra nullable o con default, el código la escribe, un release posterior la exige. No se renombra una columna en el mismo release que deja de leer el nombre viejo.
- Datos de producción no se migran «a ojo» dentro de `upgrade` sin un conteo de filas afectadas escrito en el mensaje del PR.
- Dos PR con migraciones paralelas reordenan `down_revision` al integrar. Hay un solo head.

### 1.8 Pirámide de tests

Se testea en la costura pública. Un test que se rompe al renombrar un privado, sin cambiar el comportamiento, está de más. Vocabulario de los tests: el de `CONTEXT.md` (corte, envío, maestro, filtrado).

| Nivel | Qué demuestra | Dónde está hoy | Qué falta |
| --- | --- | --- | --- |
| Unitario | Parser, cruce, clasificador, transiciones, dinero, fecha de corte | `test_excel_parser`, `test_excel_joiner`, `test_reply_classifier`, parte de `test_saldado` | Transiciones como tabla; normalización a 8 dígitos y montos `1.234,50` (Q15) |
| Integración | HTTP + base, un caso de uso | La mayoría de los ~190 tests, `TestClient` y SQLite en memoria (`conftest.py`) | Un test del recorrido falla → corrige maestro → reenvía → aparece en enviados (`docs/PENDIENTES.md`) |
| Contrato | La respuesta cumple el schema OpenAPI, incluidos los problem details | No existe | Práctica de aprendizaje hasta que dos personas se pisen el contrato. Recién ahí, un schema guardado y un diff en CI |
| Punta a punta | El operador completa un corte y una campaña contra un SMTP de mentira | No existe en el repo | Un recorrido a mano escrito en el PR alcanza para el piloto. Playwright contra Mailpit (MIT) entra cuando ese paso falle dos veces, no como compuerta de cada PR |

Fixtures: `client`, `db`, `auth_headers`, `test_user` quedan. El `db` de sesión compartida y el `delete` de `ConfiguracionSistema` al final son frágiles: un test que olvida limpiar envíos contamina al siguiente. Cada test abre transacción y revierte, o trunca las tablas de negocio en el teardown.

Factories: funciones en `backend/tests/factories.py` (`envio()`, `cliente()`, `ciclo()`), con `Decimal` y estados válidos. Los tests de `test_maestro.py` y `test_saldado.py` arman el mismo `Envio(...)` muchas veces. No se agrega `factory_boy` mientras esas funciones alcancen.

SMTP, IMAP y el reloj se inyectan. Un test de rate limit usa el override que `enviar_ciclo` ya acepta (`rate_limit_override`); no duerme 30 segundos.

El orden de trabajo sigue siendo uno vertical: un test rojo, el mínimo código, recién después el siguiente caso. Los nombres describen el comportamiento (`test_clave_repetida_no_crea_ciclo`), no el método.

### 1.9 Rendimiento

Presupuesto del backend en el piloto: un corte de ~600 deudores se previsualiza en menos de 2 segundos en la base de producción, y la campaña completa respeta 5 mails / 30 s (cerca de una hora). Esa hora es el diseño, no un objetivo a bajar saltándose el rate limit.

- La racha por fila (1.1) es el primer arreglo medible. Se mide con un Excel de 600 filas en el test, contando queries, antes y después.
- `/health` deja de abrir una sesión en cada probe. El watcher y el balanceador preguntan seguido; Neon Free se despierta por eso (Q21). El chequeo de base pasa a un endpoint aparte o a un intervalo largo.
- Listas históricas se agregan en SQL. Un endpoint que hace `query(Envio).all()` para un KPI se considera un bug de rendimiento.
- Índices que ya importan y se mantienen: `envios.ciclo_id`, `envios.clave_union`, `envios.message_id`.
- El watcher pide tamaño y encabezados antes del cuerpo completo (`imap_watcher.py` baja `RFC822`). El tope de adjunto y el de Excel son de la auditoría de seguridad; el estándar es un límite declarado en el endpoint de upload (el logo ya lo tiene en 2 MB, el Excel no).

---

## 2. Frontend

React 18 en las reglas del repo; `frontend/package.json` declara React 19.2. El estándar es la versión que el lockfile instala, y el README del repo se actualiza cuando se toque (ticket de documentación del mapa). Vite, TypeScript, Tailwind, shadcn/ui, TanStack Query 5, React Router 6. Axios queda en `src/services/api.ts` como único cliente.

`react-hook-form` está en dependencias y no hay ningún `useForm` en `src/`. Zod no está. No se agrega otra librería de formularios ni de validación: Zod es MIT, encaja en el allowlist, y se suma el día que se migre el primer formulario.

### 2.1 Carpetas

Se mantiene el corte actual:

```
src/pages/          una ruta, compone
src/components/     layout, envios, upload, dashboard, maestro, profile, ui/
src/services/       funciones HTTP, sin estado de React
src/hooks/          estado de servidor y efectos
src/types/domain.ts tipos de la API
src/lib/            formato, estados, utilidades puras
```

`components/ui/` no se edita a mano. Una página que pasa de un archivo ilegible se parte en componentes de esa página, no en una carpeta `features/` nueva. Los tipos de la API tienen una sola fuente. Hasta que el schema OpenAPI esté estable, esa fuente es `domain.ts`, escrita a mano y revisada contra el backend en el mismo PR. Generar tipos desde OpenAPI reemplaza el archivo cuando el contrato de errores deje de cambiar.

### 2.2 Estado y datos

Estado de servidor: TanStack Query. `QueryClient` ya está en `main.tsx` (`staleTime` 30 s, un reintento) y ningún componente llama `useQuery`. `useCiclo` guarda el ciclo, el preview y el progreso en `useState` y traga el error del preview (`finally` sin `catch`).

Las keys que ya documenta `.claude/rules/frontend.md` se usan de verdad: `['ciclo', 'activo']`, `['envios', estado]`, `['maestro']`, `['plantilla']`. Invalidar `['envios']` después de confirmar, pausar o marcar un pago. El preview es estado de UI (el archivo elegido, todavía no persistido): vive en el estado del asistente, no en la cache.

Reglas de la cache:

- Una mutación que cambia el corte invalida ciclo, envíos y dashboard.
- El error de red conserva el dato anterior y muestra un aviso. No se reemplaza la tabla por una pantalla vacía.
- El progreso de envío es una query del estado en el servidor (o el SSE que escribe en esa cache). Si el operador recarga, la barra sale de lo persistido, no de la memoria del tab. El comentario de `PENDIENTES.md` dice que la barra ya se reconstruye; el estándar es que esa reconstrucción lea filas, no `_ids_en_proceso` en el proceso de Render.

### 2.3 Formularios y validación

React Hook Form para todo formulario con más de un campo y reglas. Zod para el esquema, compartible con el mensaje que se muestra. El resolver oficial de hook-form es MIT.

Orden de migración, cuando se toque la pantalla: login (`LoginPage.tsx`, hoy `useState`), credenciales (`ConfiguracionPage.tsx`), plantilla, alta de cliente. La edición inline del maestro puede seguir en estado local si son dos campos; al sumar el diff de Q20 pasa a un formulario con la lista de conflictos.

El esquema de Zod rechaza en el cliente lo que el servidor ya rechaza (email, monto, color hex de la plantilla). El servidor sigue siendo la autoridad. El cliente muestra el error al lado del campo, con el texto del problem detail.

No se usan librerías copyleft ni de licencia mixta para el texto rico. Si más adelante hay notas con formato, Tiptap (MIT). BlockNote queda afuera (MPL).

### 2.4 Carga, vacío y error

Cada lista declara los tres. El vacío dice qué significa y cuál es el paso siguiente (`DESIGN.md` ya lo pide para Sin email y Filtrados). `NuevoEnvioPage` tiene `emptyState` por tabla; el patrón se copia a Seguimiento, Maestro y Dashboard.

- Carga: `Skeleton` de la misma forma que la tabla, no un spinner genérico que mueva el layout.
- Vacío: una frase y, si hay una acción, un solo botón (subir Excel, ir al maestro, refrescar).
- Error: qué pasó, en una frase, y cómo reintentar. `ErrorBoundary` hoy dice «Recargá la página» y no ofrece reintentar la consulta. El boundary cubre el crash de render; el error de `useQuery` se maneja en la página y deja el resto de la app usable.
- El progreso de una campaña usa `aria-live="polite"` además de la barra. Al terminar, el cartel distingue enviados de pedidos (ya está en el flujo; el texto entra en la guía de microcopy).

### 2.5 Accesibilidad (WCAG 2.2 AA)

El objetivo de `PRODUCT.md` y `DESIGN.md` es AA, y los criterios de abajo entran ahora porque el operador los choca (login sin etiqueta, confirmación que no dice el efecto, estado solo por color). Una certificación o un pase mobile completo es práctica de aprendizaje hasta [D-27](decisiones-pendientes.md) o una reventa que lo pida. La versión de referencia es [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (recomendación W3C). AA incluye el nivel A.

| Criterio | Qué se exige acá | Dónde mirar |
| --- | --- | --- |
| 1.3.1 / 3.3.2 Nombre y etiqueta | Cada control tiene `<label>` visible, asociado. Un `placeholder` no alcanza | `LoginPage.tsx`: Usuario y Contraseña son solo placeholder |
| 1.3.5 Propósito del campo | `autocomplete="username"` y `autocomplete="current-password"` en el login; `new-password` en el cambio de clave | Mismos formularios. Permite al gestor de contraseñas completar |
| 1.4.1 Uso del color | Estado = punto + texto, nunca solo color | Ya en `DESIGN.md`. Se mantiene en los estados nuevos (pausa, no seleccionado) |
| 1.4.3 Contraste | Texto normal ≥ 4,5:1, grande ≥ 3:1 | Tokens de `DESIGN.md`. El gris de placeholder sobre `bg-gray-50` del login se mide al pasar esa pantalla a los tokens |
| 2.4.7 / 2.4.11 Foco visible y no tapado | El anillo de foco no queda debajo de la barra lateral ni de un diálogo | Sidebar fija en ~240 px; en 390 px de ancho el foco de una fila no puede quedar oculto |
| 2.5.7 Arrastre | Soltar un Excel también se puede con un botón de elegir archivo | `FileDropzone` |
| 2.5.8 Tamaño del objetivo | 24×24 px CSS como mínimo en los botones de icono (editar, eliminar, reactivar) | `MaestroPage.tsx` |
| 3.3.1 / 3.3.3 Error identificado y sugerido | El error nombra el campo y dice cómo corregirlo | Tabla de filas del Excel; login («Usuario o contraseña incorrectos» está bien si no revela cuál falló) |
| 3.3.7 Datos repetidos | No volver a pedir email o clave que el sistema ya tiene, salvo que el operador los esté cambiando | Diff del maestro (Q20) |
| 3.3.8 Autenticación | Pegar la clave está permitido. No hay captcha ni puzzle. El gestor de contraseñas funciona | Login y cambio de clave |
| 4.1.2 Nombre accesible | Iconos con `aria-label` en castellano («Editar», «Eliminar», «Reactivar») | Maestro ya tiene varios. Las columnas `th aria-hidden` de acciones se quedan si el botón de la celda tiene nombre |
| Tablas | `<th scope="col">` y un nombre de tabla (`<caption>` visible o `aria-labelledby` al título de la solapa) | `NuevoEnvioPage`, `MaestroPage`, `DashboardPage` |

El teclado recorre solapas, filas y diálogos en el orden visual. Un diálogo atrapa el foco y lo devuelve al botón que lo abrió (Radix Dialog ya lo hace: se usa ese primitivo, no un `div` propio).

### 2.6 Montos y fechas (es-AR)

Una sola función en `src/lib/formato.ts`. Hoy `pesos()` está copiada en `DashboardPage.tsx` y `ClientePerfilPage.tsx`, y `NuevoEnvioPage` concatena `"$"` con `toLocaleString("es-AR")`. `5000.50` puede verse como `5.000,5` porque no se fijan los decimales.

```ts
export function formatPesos(valor: number | string): string {
  return new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(valor));
}
```

El valor sigue siendo decimal en la API (string o number estable). El cliente no suma montos para un total oficial: el total lo manda el servidor. `tabular-nums` se queda en cada columna de importe.

Fechas de calendario (fecha de corte, «deudor desde») se formatean en `America/Argentina/Buenos_Aires` con `date-fns` y locale `es`, patrón `dd/MM/yyyy`. Un instante (enviado, última revisión IMAP) lleva también `HH:mm`. No se usa `toLocaleDateString()` suelto ni la zona del navegador para una fecha de corte: un operador en otra zona no puede correr el día del corte. `new Date(iso)` sin zona, como en el gráfico de `DashboardPage` (`new Date(anio, mes, 1)`), se revisa cuando se muestre la fecha de corte (Q23): esa fecha es un día, no un timestamp.

No hay segunda locale. No se agrega una librería de i18n. Los textos viven en los componentes, en castellano rioplatense, hasta que exista otro idioma.

### 2.7 Presupuesto de rendimiento

Medir Core Web Vitals en campo (LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 al percentil 75, [web.dev](https://web.dev/articles/vitals)) es práctica de aprendizaje: esta app no compite en una búsqueda. Entra ahora que la tabla del corte se pueda leer y que la barra de progreso no empuje el layout. Si en la máquina del operador ordenar 600 filas se siente trabado, ahí se virtualiza.

- Recharts entra solo en las rutas del dashboard y del perfil (`React.lazy` de la página). El login no lo descarga.
- 600 filas sin virtualizar se aceptan en el piloto si el INP de ordenar o filtrar sigue bajo 200 ms en la máquina del operador. Si no, se virtualiza la tabla (TanStack Virtual es MIT; se suma cuando la medición lo pida).
- Imágenes: el logo del mail tiene tope de 2 MB en el servidor. La UI no reserva un hero. El favicon actual alcanza.
- Skeletons con el alto final de la fila, para no empujar el contenido al llegar los datos.

### 2.8 Tests de componentes

Vitest y Testing Library (MIT) el día que se agregue el script `test` al `package.json`. Cubren funciones puras y comportamiento, no el markup de shadcn.

Primeros tests: `formatPesos` y `formatFecha`; el vacío de una solapa; el diálogo de confirmar que muestra «Esto cancela N envíos pendientes»; el deshabilitado del botón cuando hay filas inválidas. Playwright cubre los dos recorridos del apartado 3.2 contra Mailpit. No se fotografían pantallas enteras como aserción: un cambio de copy rompería el test sin romper el producto.

---

## 3. UX de flujo

Esto no rediseña la pantalla. La personalidad visual está en `PRODUCT.md` y `DESIGN.md`: herramienta de trabajo, números primero, un acento por acción. Acá está lo que el operador tiene que lograr.

El glosario de la interfaz usa las palabras del operador. En los documentos de producto el ciclo se llama **corte** cuando se habla del Excel, y **envío** o **campaña** cuando se habla de los mails. La UI hoy dice «Nuevo envío» para las dos cosas. Al separar guardar de enviar, los botones se llaman «Guardar corte» y «Enviar recordatorios».

### 3.1 Trabajos del operador

El operador es el dueño de la empresa de ascensores. Entra a hacer una tarea, no a recorrer el producto (`PRODUCT.md`).

| Cuando… | Quiere… | Para… |
| --- | --- | --- |
| Cierra la quincena | Subir el Excel completo, ver qué cambió y dejar el historial al día | Saber la cartera aunque ese día no mande mails |
| Decide reclamar | Elegir un lote, confirmar, y ver que salió | No escribir un mail por consorcio |
| Entre cortes | Ver quién contestó, quién rebotó y quién sigue debiendo | No perder un deudor ni dar por cobrado un adjunto |
| Cambia un contacto | Actualizar el maestro sin pisar una baja, una pausa ni un email que corrigió a mano | Que el próximo corte use el dato correcto |
| Algo falla | Entender la fila, el mail o la caída, y seguir | No reenviar de más ni dar por saldada una deuda |

Juan y Julián acompañan los dos primeros cortes. El producto se prueba con el operador, no con ellos como usuarios sustitutos.

### 3.2 Recorridos

1. **Corte.** Elegir archivo → el sistema muestra filas inválidas (fila, columna, valor, motivo) y permite descargarlas → con errores de clave, monto o clave repetida no se puede guardar → montos en 0 o negativos son aviso → fecha de corte, por defecto hoy → guardar deja el corte anterior vigente hasta el éxito → el dashboard cambia sin haber mandado mails.
2. **Campaña.** Sobre el corte guardado, ver para enviar / sin email / filtrados / pausados / no seleccionados, cada uno con su motivo → elegir filas → si hay envíos pendientes del corte anterior, confirmar «Esto cancela N envíos pendientes» → barra con enviados sobre el total y tiempo aproximado (600 mails son cerca de una hora) → se puede cerrar el navegador y volver → al terminar, cuántos salieron y cuántos no.
3. **Seguimiento.** Solapas por estado, refrescar ahora, última revisión con hora → un pago dice que es un comprobante recibido, no una acreditación → pausar un cliente no toca el saldo → la pausa se levanta a mano.
4. **Maestro.** Diff antes de aplicar: altas, cambios, conflictos con lo editado a mano, emails que quedarían vacíos → por defecto se conserva lo editado a mano → nunca se reemplaza un email por vacío → bajas y pausas no entran en el diff como cambios aplicables.
5. **Primera vez.** Entrar, cambiar la clave, cargar el maestro, revisar la plantilla, probar SMTP e IMAP, recién después un lote chico acordado con el cliente.

### 3.3 Heurísticas de Nielsen, aplicadas

Las diez heurísticas de [Nielsen Norman Group](https://www.nngroup.com/articles/ten-usability-heuristics/) se usan como lista de revisión del flujo. Lo que ya se cumple no se reabre.

| # | Heurística | En este producto |
| --- | --- | --- |
| 1 | Visibilidad del estado | Barra de campaña, conteos en la barra lateral, «Datos al dd/mm, cargado hoy», «última revisión hh:mm». Un envío en curso no aparece como fallido. |
| 2 | Correspondencia con el mundo real | Corte, deuda, comprobante, pausa, baja. «PAGO» en la solapa se acompaña de «comprobante recibido». Montos en pesos, fechas en dd/mm. |
| 3 | Control y libertad | Guardar sin enviar. Deshacer una pausa. Cancelar el diálogo de un corte nuevo. No hay deshacer de un mail ya aceptado por el servidor: se dice antes. |
| 4 | Consistencia | Los mismos nombres de estado en sidebar, tabla y ficha. Un solo formato de dinero. Voseo en todos los botones. |
| 5 | Prevención de errores | El archivo inválido no se aplica. El segundo clic no crea otro corte. Eliminar y dar de baja piden confirmación con el nombre del consorcio. |
| 6 | Reconocer, no recordar | Motivo de cada excluido visible en la fila. El operador no reconstruye el contexto entre el corte y la ficha. |
| 7 | Flexibilidad | Atajos y paleta de búsqueda quedan para después del piloto. En el piloto, el lote chico y «continuar con el resto» son la flexibilidad que importa. |
| 8 | Estética y diseño minimalista | La cubre `DESIGN.md`. Una acción primaria por pantalla. |
| 9 | Recuperación de errores | La fila dice cómo corregirla. Un fallo de SMTP dice que se revisen las credenciales y deja el resto del lote en un estado conocido. |
| 10 | Ayuda | Una línea de contexto en el corte («el Excel es la cartera completa») y el runbook para Juan y Julián. No un tour de diez pasos. |

### 3.4 Acciones destructivas

Confirmación con el efecto concreto, no un «¿Estás seguro?».

- Eliminar un cliente: el `window.confirm` de `MaestroPage.tsx` ya nombra a la persona y dice que se puede reactivar. Pasa a un diálogo del sistema de diseño, con el mismo texto, foco en «Cancelar».
- Guardar un corte mientras hay campaña o pendientes: «Esto cancela N envíos pendientes». El número sale del servidor.
- Dar de baja desde el mail: el GET deja de aplicar el cambio (auditoría de seguridad, F1). Una página con un botón. El prefetch de un antivirus no puede silenciar a un consorcio para siempre.
- Reenviar todos: no incluye no seleccionados, ni inciertos, ni los que ya tienen `message_id`. Si el proceso se cayó a mitad, el runbook manda a mirar la carpeta de enviados antes de tocar ese botón ([D-11](decisiones-pendientes.md)).
- Limpiar la base (`scripts/limpiar_db_produccion.py`): sigue en dry-run salvo `--ejecutar`. No es una acción de la UI.

Deshacer, cuando el dominio lo permite: levantar una pausa, reactivar un dado de baja, descartar un preview. Un corte ya aceptado lo corrigen Juan y Julián en el piloto (Q13), con una copia previa. No se promete un deshacer de un minuto para un mail salido.

### 3.5 Operaciones largas

La campaña es la operación larga. El feedback:

- Total, enviados, pendientes, fallidos, y una estimación honesta («alrededor de una hora» para 600, calculada con 5/30 s).
- La página se puede cerrar. Al volver, el mismo progreso, leído del servidor.
- Un fallo de un destinatario no detiene el lote ni lo marca entero como fallido.
- Al final, un resumen que permanece hasta que el operador lo cierra: enviados, no enviados, y el enlace a los no enviados.
- El refresco IMAP dice «última revisión» aunque el resultado sea «nada nuevo». Diez minutos de silencio sin esa hora parecen un sistema colgado.

### 3.6 Microcopy

Castellano rioplatense, voseo, trato de trabajo. Frases cortas. El verbo es la acción. Sin signos de admiración, sin «¡ups!», sin «éxito» como única palabra.

| Se escribe | No se escribe | Por qué |
| --- | --- | --- |
| Guardar corte | Confirmar envío (cuando todavía no se manda) | Separa las dos operaciones |
| Enviar recordatorios | Disparar campaña | El operador manda mails de deuda |
| Esto cancela 12 envíos pendientes | ¿Estás seguro? | Dice el efecto |
| Comprobante recibido. No confirma que el pago esté acreditado | Pago | La inferencia ya está aclarada en el drawer; el título de la solapa tiene que aguantar solo |
| Fila 14, columna Monto: «abc» no es un importe | Error de validación | Q15 |
| Revisá la clave y la contraseña de aplicación en Configuración | Error 502 | El operador puede actuar |
| Última revisión: 14:32 | Actualizado | Hora concreta |
| Podés reactivarlo desde Mostrar inactivos | (sin acentos, como el confirm actual) | «después» lleva tilde; se corrige al pasar el diálogo |
| Cartera sin deuda. Guardar igual | El archivo está vacío | Hace falta la confirmación explícita de Q15 |

Los errores de login no dicen si falló el usuario o la clave. Los de archivo sí dicen la fila: el Excel es del operador, la clave no.

### 3.7 Puesta en marcha

No hay un asistente de producto. Hay una lista de cuatro pasos, visible en Configuración hasta completarla, porque sin eso el primer corte falla tarde:

1. Cambiar la clave inicial (cuando [D-03](decisiones-pendientes.md) esté hecho, el primer ingreso no sigue con la clave del seed).
2. Cargar el maestro y ver el conteo de consorcios con email.
3. Probar conexión: SMTP e IMAP por separado, con el resultado de cada uno.
4. Revisar asunto, monto mínimo y el pie del mail.

El primer corte real se hace junto al operador, con un lote chico (Q9), no como tarea para descubrir solo. Una frase fija arriba del primer preview: «Este archivo tiene que ser la cartera completa. Quien no esté va a figurar como regularizado.»

### 3.8 Prueba de uso con el operador, durante el piloto

Hay un solo operador. La prueba no es una muestra: es observación de las dos sesiones reales (primer y segundo corte), con su Excel, en su máquina. Quien facilita es Juan o Julián. Quien opera es el cliente. No se le pide que «piense en voz alta» como consigna de laboratorio; se le pide que haga el trabajo y se anota dónde se detiene.

Antes de la sesión: copia de la base, casilla de prueba o lote de tres direcciones acordadas, y el runbook de restauración a mano. No se manda el lote grande en la primera sesión.

Tareas de la primera sesión, en orden, sin ayudar salvo que pida ayuda (anotar el pedido):

1. Entrar y decir en una frase para qué sirve la pantalla en la que cayó.
2. Subir el Excel. Si hay errores, corregirlos fuera y volver a subirlo.
3. Decir cuántos consorcios deben, cuántos no tienen email y cuántos no se van a reclamar, sin que el facilitador señale la cifra.
4. Guardar el corte sin enviar, ir al dashboard y señalar qué cambió.
5. Elegir el lote chico y enviar. Decir cómo sabe que terminó, incluso si cierra el navegador a la mitad y vuelve.
6. Abrir un contestado y un comprobante, y decir si lo daría por cobrado.

Segunda sesión, con el corte siguiente: un ausente queda regularizado, una pausa sigue afuera, los pendientes del corte anterior no salen, la fecha de corte no es la de hoy si él carga un archivo atrasado (en el piloto eso lo resuelven Juan y Julián, y se observa si el operador entiende por qué el sistema se lo niega).

Se anota, por tarea: lo logró solo, lo logró con una pregunta, o no lo logró. La frase textual cuando se detiene. El lugar (pantalla y control). No se puntúa estética. Al final, tres preguntas: qué haría distinto la próxima quincena, qué número no le creyó, qué tuvo miedo de apretar.

El piloto se considera usable para dejarlo solo cuando las tareas 2, 3, 4 y 5 salen sin pregunta en el segundo corte, y cuando él explica la diferencia entre comprobante y deuda. Si no, se extiende el acompañamiento: eso ya es una salida prevista del ticket 21 del mapa, no un fracaso de la prueba.

---

## 4. Checklist de revisión y definición de hecho

Dos ejes, como en una revisión seria: ¿respeta estos estándares? y ¿hace lo que pedía la decisión (Q, ADR o ticket)? Un eje no compensa al otro.

### Revisión

- El caso de uso nuevo no escribe SQL ni `commit` en el router.
- Las invariantes del 1.2 que el cambio toca tienen un test con un valor esperado escrito a mano, no recalculado igual que el código.
- Dinero en `Decimal`. Fechas de corte como día de calendario.
- Errores nuevos usan el sobre de problem details y un `type` estable.
- No se loguea email, nombre, token ni `Message-ID`.
- Migración: un head, `batch_alter_table` si cambia columnas, `downgrade` posible o una frase que diga por qué no.
- El frontend muestra carga, vacío y error. Textos en voseo, montos por `formatPesos`.
- Controles nuevos con etiqueta, foco visible y nombre accesible. El estado no depende solo del color.
- Una acción que cancela envíos, borra o da de baja nombra el efecto y la cantidad.
- Dependencia nueva: licencia en el allowlist, anotada en el PR.
- El diff no copia código de Twenty ni pega fragmentos de `twenty-front` / `twenty-server`.
- Si se pospuso algo a propósito (rate limit, preview sin DB, un solo locale), el PR lo dice en una línea.

### Definición de hecho

Hecho, a este precio, es la columna «Entra ahora». Una fila de «se practica cuando dispare» no es parte del hecho salvo que el disparador ya haya ocurrido.

- El comportamiento pedido está en el código y en un test que falla si se saca.
- `pytest` del backend en verde. Si el PR toca UI de flujo, el recorrido afectado se probó (Playwright cuando exista; hasta entonces, el paso manual escrito en el PR: qué pantalla, qué se hizo, qué se vio).
- OpenAPI y `domain.ts` describen lo mismo, incluidos los errores.
- Una migración aplicada sobre una base vacía y, si cambia datos, el conteo esperado está en el PR.
- Textos visibles revisados contra la guía del 3.6.
- Documentación tocada si cambia una regla de `CONTEXT.md`, un ADR o un runbook. Un ADR aceptado no se reescribe: se supersede.
- Sin secretos, sin `.env`, sin claves de ejemplo reales.

Olores que se miran y se discuten, sin ser un rechazo automático: el mismo bloque copiado, un `switch` de estados repetido en tres archivos, un parámetro que solo anticipa un segundo cliente, una función que solo pasa la llamada al módulo de al lado.

---

## 5. Fuentes

Consultadas el 23/09/2026.

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/), recomendación W3C. Criterios nuevos respecto de 2.1 que aplican: 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8. AA incluye el nivel A.
- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), Problem Details for HTTP APIs. El soporte nativo de FastAPI sigue en discusión ([PR 15951](https://github.com/fastapi/fastapi/pull/15951)); el contrato se implementa con Pydantic.
- [Core Web Vitals](https://web.dev/articles/vitals): LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1, percentil 75. INP reemplazó a FID.
- [10 heurísticas de usabilidad](https://www.nngroup.com/articles/ten-usability-heuristics/), Nielsen Norman Group.
- [Diátaxis](https://diataxis.fr/) para ubicar este texto: es explicación y referencia de trabajo, no un tutorial. El índice está en [README.md](README.md).
- Código y reglas del repo citados arriba. Decisiones de producto: [grilling-decisiones-15-23.md](grilling-decisiones-15-23.md), `Documentos/12` en `codex/handoff-analysis`, `estrategia-enterprise.md`.
- Zod (MIT) y React Hook Form (MIT) como par de validación. TanStack Query 5 ya está en el `package.json`.
