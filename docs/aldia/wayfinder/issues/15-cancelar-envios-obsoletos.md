# Cancelar envíos obsoletos

Type: task
Modo: AFK
Status: open
Blocked by: 14
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/services/ciclo_service.py`
- `backend/app/routers/ciclos.py`
- `backend/app/services/smtp_sender.py`
- `backend/tests/test_ciclos.py`
- `backend/tests/test_smtp_sender.py`
- `frontend/src/pages/NuevoEnvioPage.tsx`
- `frontend/src/components/upload/ProgresoEnvio.tsx`
- `frontend/src/types/domain.ts`
- `frontend/src/services/ciclos.ts`

## Decisión cerrada

Q18 no se reabre. Un corte nuevo frena lo que todavía no salió. Cada mail se vuelve a mirar un instante antes de salir. El número del diálogo sale del servidor.

## Resultado

Aceptar un corte nuevo cancela los envíos que todavía no salieron del anterior. Durante la campaña se ve esta campaña.

## Criterios de aceptación

- Al guardar un corte nuevo, los pendientes del anterior quedan «cancelado por nuevo corte». No salen después de haber sido saldados.
- Si hay una campaña en curso, la confirmación dice «Esto cancela N envíos pendientes».
- Antes de cada mail se revalida: ciclo activo, no saldado, sin baja y sin pausa. La pausa, cuando exista, la respeta esta revalidación. Hasta que Pausar recordatorios cierre, la revalidación igual deja el hueco nombrado en el código, sin columnas nuevas.
- El reenvío de una fila exige ciclo activo y `saldado_en` vacío.
- Mientras la barra de esta campaña está activa, la tabla es la de esta campaña y «Reenviar todos» no se puede apretar.
- El aviso de fin permanece hasta que el operador lo cierra: enviados, fallidos, enlace a seguimiento. Junto a la barra, el piso `ceil(restantes / 5) * 30 s`, rotulado como mínimo. No se suman los huecos de la corrida de 600 ni se les inventa una causa.
- No se agrega una migración. El estado nuevo, si hace falta un valor de enum, ya entró en la `0009`. Si no alcanza, se para y se anota: no se abre una `0010` en paralelo con Pausar recordatorios.

## Pregunta

¿Qué pasa con los mails que todavía no salieron cuando entra un corte nuevo?
