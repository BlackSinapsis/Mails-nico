# La campaña de 600 ya está medida

Type: task
Modo: AFK
Status: resolved
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- (ninguno)

## Decisión cerrada

No se envían 600 mails. El tope de un envío es 150, por Yahoo. Esta corrida queda como medición. No es una lectura de CU-h.

## Answer

SQLite local. El rate limit de 5 cada 30 segundos no se tocó. El monto mínimo de la plantilla se puso en 0 solo en esa base.

- Primer mail 22:20:16 UTC. Último mail 23:45:14 UTC.
- 5098,6 s de reloj (84 min 59 s). 600 archivos SMTP y 600 `message_id`.
- 119 huecos entre tandas de 5. 116 midieron 30,04 s. Sin los tres huecos largos, el piso es 59 min 30 s.
- Huecos sin línea de log en el medio: 339 s, 625 s y 635 s. La causa no se especifica.
- RSS, 221 muestras cada 15 s en 550/600: 116–127 MB. El mismo proceso llegó al 600.
- SQLite de 196.608 bytes y 0 envíos a 516.096 bytes y 600 envíos.
- Recarga en «5 / 600»: la barra volvió y el proceso completó los 600.
- `SIGTERM` cerca del 575: el mismo proceso vació la cola. `SIGKILL` en un corte de 8, con 5 `message_id`, no reanudó y no duplicó.
- `_poll_inbox` de 600 tardó 26,660 s y solo miró `NO_CONTESTADO`. Seguir también a `CONTESTADO` es un ticket abierto.

## Pregunta

¿Cuánto tardó y cuánta memoria usó una campaña de 600 en la prueba local?
