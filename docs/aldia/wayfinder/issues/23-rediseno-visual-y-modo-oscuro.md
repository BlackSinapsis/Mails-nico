# Rediseño visual y modo oscuro

Type: task
Modo: AFK
Status: open
Blocked by: 09, 20
Fase: 2 · CRM
Tamaño: L
Archivos:
- `frontend/src/index.css`
- `frontend/src/main.tsx`
- `frontend/index.html`
- `frontend/src/components/layout/AppLayout.tsx`
- `frontend/src/components/layout/Sidebar.tsx`
- `frontend/src/components/layout/AuthGuard.tsx`
- `frontend/src/components/layout/ErrorBoundary.tsx`

## Decisión cerrada

La capa 2 entra con este review. El modo oscuro es el default. No hay un toggle de tema. No hay Framer Motion. La fuente es la del sistema. De Twenty, Attio y Linear se copian jerarquía y densidad, con los tokens que ya tiene la app. Librerías MIT. El shell es de este ticket. Cada pantalla la termina el ticket que ya es dueño de ese archivo.

## Resultado

`html` abre con la clase `dark`. El sidebar y el encabezado usan los tokens nuevos. En el teléfono la barra no tapa el contenido.

## Criterios de aceptación

- Tokens `--surface`, `--panel`, `--input`, radios 4/6/10, sombras suaves, sin reemplazar la escala OKLCH existente. Escala 12/13/14/16/20/24. Montos con `tabular-nums` donde el shell dibuja un importe.
- El oscuro es el único tema. No se agrega un botón para volver al claro.
- El shell lo pueden usar login, dashboard, corte, seguimiento, clientes, plantilla y configuración. Este ticket escribe el layout, no esas páginas.
- En 390 px la navegación se puede abrir y cerrar, y el foco no queda debajo.
- La inicialización de Sentry que haya dejado el ticket anterior sigue arrancando.
- No se agrega `cmdk` ni la ruta Hoy. Esos tickets esperan y escriben sus propios archivos.

## Pregunta

¿Cómo queda el marco de la app en oscuro, pensado para escritorio y usable en el teléfono, sin repintar todavía cada pantalla?
