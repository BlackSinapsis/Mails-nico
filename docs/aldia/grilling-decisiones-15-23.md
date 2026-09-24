# Grilling — decisiones Q15–Q23

Rama de referencia: `codex/handoff-analysis` (ddd2f7b) en `BlackSinapsis/Mails-nico`. Decisiones Q1–Q14 en `Documentos/12_GRILLING_ENTREGA_Y_EVOLUCION.md`.

## Twenty (decidido 23/09/2026)

- El fork profundo de Twenty sigue descartado como punto de partida (`Documentos/06`, opción D).
- Twenty sí es la referencia principal de UI y funcionalidades para mejorar la app, adaptadas al stack actual (React + shadcn/ui).
- Objetivo: un producto completo y a medida del cliente, aprovechando al máximo lo de Twenty. Se aprovechan sus funcionalidades y patrones.
- Licencia (decidido 23/09/2026): la app se mantiene cerrada y reutilizable para otras empresas. De Twenty se toman solo ideas (diseño, pantallas, modelo de datos); no se copia código AGPL ni comercial. Se reconstruye con librerías de licencia permisiva (MIT, Apache-2.0, BSD).
- Nivel buscado: enterprise, con todo lo que implica, y listo para desarrollo colaborativo y mantenimiento con Juan (upstream `Juanrocod/Mails-nico`).

## Credenciales de acceso (23/09/2026)

- Producción usa hoy la clave inicial de `seed_user.py`, que está en un repo público. Es temporal y hay que rotarla ya.
- Manejo definitivo a implementar en el piloto: el seed sin clave por defecto (exige `SEED_PASSWORD`, o genera una aleatoria y la muestra una sola vez), cambio de clave obligatorio en el primer ingreso, política mínima de clave, un usuario por persona (operario, Juan, Julián) con log de accesos, y las claves guardadas en un gestor de contraseñas compartido, nunca en el repo ni en el chat.

## Q15 — Filas inválidas (decidido 23/09/2026: opción A con matices)

- Un error de clave o monto, o una clave repetida, bloquea el corte. El operador corrige en Excel y re-sube.
- El preview muestra los errores por fila, columna, valor y motivo, y permite descargarlos.
- Un monto en 0 o negativo es un aviso, no un bloqueo.
- Un archivo sin filas válidas exige confirmar explícitamente "cartera sin deuda".
- Las claves numéricas se normalizan a 8 dígitos y se aceptan montos con formato argentino.
- El corte anterior sigue vigente hasta que se sube un archivo limpio. La edición dentro de la app queda para después del piloto.

## Q16 — Levantar una pausa (decidido 23/09/2026: opciones A + C)

- La pausa se levanta siempre a mano.
- La fecha de revisión es opcional; por defecto propone el próximo corte (+15 días).
- Al vencer la fecha, el cliente aparece en "pausas vencidas" y en el preview, pero sigue excluido.
- La pausa sobrevive a las importaciones de deudores y del maestro.
- Si el cliente queda regularizado, la pausa se cierra como "resuelta por regularización". Si vuelve a deber, recibe mails otra vez y el antecedente queda en su ficha.
- Modelo mínimo sugerido (Q16): `pausado_desde`, `pausa_motivo`, `pausa_revisar_el` en `ClienteMaestro` y `MotivoFiltrado.PAUSADO`.

## Q17 — Filtros de la primera entrega (decidido 23/09/2026: opción A mínima)

- Monto mínimo general, pausa por cliente y selección manual de destinatarios.
- Selección mínima: checkbox por fila y "Enviar seleccionados"; después "Continuar con el resto" sobre el mismo corte.
- Los no seleccionados tienen un estado propio (por ejemplo `NO_SELECCIONADO`), nunca "fallido", y quedan fuera de "Reenviar todos".
- Cada excluido muestra su motivo: pausa, baja, monto mínimo, sin email o no seleccionado.
- Excluir nunca cambia el saldo ni la racha.
- Umbrales por cliente y filtros combinados quedan para después del piloto.

## Q18 — Corte nuevo con envíos pendientes (decidido 23/09/2026: A + aviso B)

- Al aceptar un corte nuevo se cancelan los envíos pendientes del anterior, registrados como "cancelado por nuevo corte".
- Antes de cada mail se revalida: ciclo activo, no saldado, sin baja ni pausa.
- Si hay una campaña en curso, la UI pide confirmar "esto cancela N envíos pendientes".
- El lote de prueba y su continuación usan el mismo corte mientras no se acepte otro.
- El reenvío individual exige ciclo activo y `saldado_en IS NULL`.

## Q19 — Envío con resultado incierto (postergado 23/09/2026)

- Se deja para después del piloto: el usuario considera que el caso no va a ocurrir en la práctica.
- Riesgo que queda abierto: un error después de que el servidor aceptó el mail se ve como fallido y "Reenviar todos" podría duplicarlo.

## Q20 — Cambios manuales y maestro posterior (decidido 23/09/2026: opción A)

- Preview del maestro con diff antes de aplicar: altas, cambios, conflictos con ediciones manuales y emails que quedarían vacíos.
- El operador resuelve cada conflicto; por defecto se conserva el valor editado a mano (marca tipo `email_editado_manual_en`).
- Nunca se reemplaza un email existente por uno vacío.
- Pausas, bajas y `activo` no se tocan nunca desde el maestro.

## Q21 — Demora del seguimiento (decidido 23/09/2026: recomendación aceptada)

- Se mantiene el polling cada 10 minutos durante el piloto y se miden las CU-h reales de Neon.
- Si no entra en el presupuesto: primero optimizar (`/health` sin DB, saltear el poll sin envíos recientes, leer headers primero y UID incremental), después pasar a 30 minutos con "última revisión hh:mm" visible.
- El watcher también sigue a los `CONTESTADO`, para capturar un comprobante posterior.

## Q22 — Disponibilidad para soporte (a definir)

- Queda sin definir por ahora. Recomendación registrada: sesiones agendadas por corte o campaña, respuesta en un día hábil, backup manual antes de cada importación y un runbook corto.

## Q23 — Fecha de los datos (decidido 23/09/2026: opción B)

- Fecha de corte obligatoria al importar (por defecto hoy, editable), guardada aparte de `creado_en`.
- Evolución, antigüedad y "deudor desde" usan la fecha de corte; `creado_en` queda para auditoría.
- En el flujo normal no se acepta una fecha menor o igual a la del corte vigente; en el piloto las cargas atrasadas o rectificaciones las resuelven Juan y Julián.
- El preview muestra "Datos al dd/mm, cargado hoy" y avisa si pasaron más de 15 días desde el último corte.
