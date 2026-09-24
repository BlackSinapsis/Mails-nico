# CI de pruebas y licencias

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `.github/workflows/ci.yml`

## Decisión cerrada

D-29 confirma el allowlist el día que hay CI. `cssutils` (LGPL, vía premailer) es la única excepción, hasta la primera reventa. El reemplazo del inliner está en Esperar el disparador. No se abre el PR de documentación.

## Resultado

Cada PR corre lint, tipos, pytest y el build del frontend, y falla si aparece una licencia fuera de la lista.

## Criterios de aceptación

- El workflow corre ruff o el lint que ya use el repo, `tsc`, pytest y `npm run build`. Sin secretos de producción.
- El allowlist es MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, y las permisivas que ya están (Unlicense, PSF, MIT-CMU).
- AGPL, GPL, SSPL, BUSL y licencia desconocida fallan el CI.
- `cssutils` es la única excepción, con fecha y con el reemplazo apuntado a Esperar el disparador.
- Playwright no corre en cada push.
- El workflow de Pages es otro archivo y espera a este, para no compartir la carpeta a medias: este ticket crea `.github/workflows/ci.yml` y no `pages.yml`.

## Pregunta

¿Qué corre solo en cada PR para que dos personas no pisen una regla de corte ni una licencia?
