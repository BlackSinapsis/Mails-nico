# Hoy, al lado del dashboard

Type: task
Modo: AFK
Status: open
Blocked by: 23, 19
Fase: 2 · CRM
Tamaño: M
Archivos:
- `frontend/src/pages/HoyPage.tsx`
- `frontend/src/App.tsx`
- `frontend/src/components/layout/Sidebar.tsx`

## Decisión cerrada

Hoy se suma al lado del dashboard. No lo borra. Es una cola de excepciones: comprobantes por revisar, sin email, rebotes y pausas vencidas.

## Resultado

Al entrar, el operador puede abrir Hoy y ver qué tiene que mirar. El dashboard de cifras sigue en su ruta.

## Criterios de aceptación

- Ruta nueva. El sidebar, que ya cerró el rediseño, gana un ítem. No se redibuja el shell entero.
- Los datos salen del dashboard y del seguimiento. No hay una tabla de tareas.
- Cada fila abre el consorcio. `formatPesos`. Carga, vacío y error.
- En 390 px la lista se lee.
- No se edita `DashboardPage.tsx`.

## Pregunta

¿Qué mira el operador al entrar, sin perder el dashboard de cifras?
