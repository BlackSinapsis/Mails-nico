# Workflow de Cloudflare Pages

Type: task
Modo: AFK
Status: open
Blocked by: 24
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `.github/workflows/pages.yml`

## Decisión cerrada

El front de Aldia va a Cloudflare Pages y se despliega con el CD de GitHub. Juan conecta el proyecto cuando [OrderByte01/aldia](https://github.com/OrderByte01/aldia) tenga código. Este ticket solo deja el workflow. No se pushea y no se toca `Juanrocod/Mails-nico`.

## Resultado

El workflow construye `frontend` con `npm run build` y publica `frontend/dist`.

## Criterios de aceptación

- Root del build: `frontend`. Comando: `npm run build`. Salida: `dist`.
- `VITE_API_URL` sale de un secret o una variable del entorno de GitHub, no de un valor de producción escrito en el archivo.
- No corre contra `Juanrocod/Mails-nico`.
- No crea el proyecto en Cloudflare. Eso está en la lista de Juan, para cuando Julián lo pida.

## Pregunta

¿Qué archivo tiene que existir para que GitHub construya el front, sin conectar todavía el panel de Cloudflare?
