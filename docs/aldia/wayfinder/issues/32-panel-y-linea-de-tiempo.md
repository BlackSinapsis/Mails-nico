# Panel y línea de tiempo

Type: task
Modo: AFK
Status: open
Blocked by: 19, 25, 31
Fase: 2 · CRM
Tamaño: M
Archivos:
- `frontend/src/components/envios/EnvioDrawer.tsx`
- `frontend/src/pages/ClientePerfilPage.tsx`
- `frontend/src/pages/SeguimientoPage.tsx`

## Decisión cerrada

El panel del registro se abre al lado de la lista. La historia es la de los envíos, no un módulo de notas. El movimiento es el de Sistema de movimiento. El título es el corte y la fecha, no la racha.

## Resultado

Desde seguimiento, la ficha y Hoy se abre el consorcio sin perder la lista. La línea de tiempo muestra cortes, mails, respuestas, comprobantes y pausas.

## Criterios de aceptación

- `Sheet` de shadcn sobre Radix, ya en el repo. `Esc` cierra. Se puede pasar al siguiente y al anterior. La URL identifica el registro.
- Una línea por corte: fecha, saldo, si salió el mail, el motivo si no salió, el comprobante y la pausa. Sin pestaña de notas ni de tareas.
- El comprobante se lee del buzón al abrir y no se escribe en `uploads/`. Si el mensaje ya no está, la pantalla lo dice.
- El panel usa las clases de 200 ms / 150 ms. Con `prefers-reduced-motion`, el desplazamiento pasa a opacidad.
- `SeguimientoPage.tsx` espera a la tabla densa. Acá solo se engancha la apertura del panel.
- Pausar sigue siendo la acción ya construida. No se duplica el endpoint.

## Pregunta

¿Cómo se lee la historia de un consorcio sin salir de la lista y sin inventar un módulo de notas?
