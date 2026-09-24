# Menú de comandos

Type: task
Modo: AFK
Status: open
Blocked by: 23, 25
Fase: 2 · CRM
Tamaño: M
Archivos:
- `frontend/src/components/command/CommandMenu.tsx`
- `frontend/src/components/layout/AppLayout.tsx`
- `frontend/package.json`
- `frontend/package-lock.json`

## Decisión cerrada

Hay paleta `cmdk` para saltar y actuar, además del campo de la tabla. `cmdk` es MIT. La paleta no se anima al entrar.

## Resultado

Con Ctrl+K o Cmd+K el operador salta a un consorcio, a una pantalla o a una acción. En el teléfono el mismo menú se puede abrir desde un botón.

## Criterios de aceptación

- Acciones: ir al dashboard, a Hoy, a un corte nuevo, a un consorcio por nombre o clave.
- El campo de filtro de la tabla abierta sigue existiendo.
- No se copia código de Twenty.
- `package.json` espera a la tabla densa.
- `AppLayout.tsx` espera al rediseño. Este ticket agrega la paleta. No vuelve a pintar el sidebar.

## Pregunta

¿Desde qué atajo se salta a un consorcio o a una pantalla, sin sacar el filtro de la tabla?
