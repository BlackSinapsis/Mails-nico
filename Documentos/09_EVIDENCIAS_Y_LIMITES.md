# Evidencias de la revisión y límites

Fecha: 13/09/2026. Repositorio local: `Juanrocod/Mails-nico`.

Referencia de código observada: `b8d0072220e1c3f2acdd613c9afa7d90a21dd7ff`. Los documentos y datos ficticios locales son archivos de trabajo adicionales; esta referencia no representa una versión de Twenty.

## Revisión funcional

Se inspeccionaron modelos de cliente, ciclo y envío; parser y unión; aceptación de archivos y saldados; cálculos de resumen, evolución y continuidad; historial de cliente; etiquetas, series y tablas del dashboard; reintentos y seguimiento de correo. La revisión de UI anterior incorporó dos evaluaciones independientes autorizadas por el usuario y observación de pantallas locales, incluido móvil y teclado. Ese material se conserva en 10.

## Ejecución de tests existentes

Se ejecutaron `test_dashboard.py`, `test_saldado.py`, `test_antiguedad.py`, `test_excel_parser.py` y `test_excel_joiner.py`: **44 passed**, con 45 advertencias de deprecación de dependencias. Duración informada por pytest: 4,81 s. Se usó SQLite en memoria y configuración sintética de test, no la base local ni credenciales reales.

Los tests validan el contrato anterior. Por ejemplo, algunos esperan que PAGO corte la antigüedad: que ese test pase no significa que la regla sea correcta para el objetivo aclarado. La propuesta requiere cambiar expectativas con criterios del documento 07, no agregar pruebas que solo repitan la implementación.

## Reproducciones aisladas

Se ejecutó un script con un motor SQLite en memoria nuevo por caso. Invoca directamente servicios y la parte de persistencia de la confirmación; no inicia la aplicación ni su lector IMAP y **no consume la respuesta de streaming**, por lo que no inicia envíos SMTP. No es una prueba HTTP de autenticación ni de envío de mails. El caso R09 es un contraejemplo matemático, no una ejecución de la aplicación.

| Caso | Entrada y resultado observado | Conclusión |
|---|---|---|
| R01 | Mismo archivo A=$100.000 confirmado dos veces → 2 ciclos, rachas 1 y 2; cero mensajes enviados | Falta idempotencia de corte; racha no equivale a recordatorios |
| R02 | A=$100.000; siguiente archivo solo encabezados → deuda actual 0 y registro anterior saldado | No diferencia un cero declarado de una carga sin filas |
| R03 | A=$150.000; siguiente monto textual `150.000,50` → deuda actual 0 y anterior saldado | El descarte silencioso puede provocar una regularización falsa |
| R04 | A presente el 01/01 y 16/01; cambiar mail viejo a PAGO mueve inicio 01/01 → 16/01. Cambiar actual a PAGO deja deuda $100.000 y 1 deudor, pero ranking de antigüedad vacío | Correo e historial del saldo están acoplados |
| R05 | A=$100.000 → $60.000 → ausencia. Reducciones API: sin base, $40.000, $60.000; fórmula de perfil “Saldado histórico” $60.000 y saldo actual “—” | Nombres/totales diferentes sin explicación; ausencia válida merece cero al corte |
| R06 | A=$100.000 → ausencia → $120.000 | La reaparición reinicia racha en 1; comportamiento a conservar |
| R07 | Dos filas A=$100.000 y A=$25.000 | Conserva $25.000 y descarta una fila; política actual de última fila |
| R08 | A=$100.000 → $70.000; volver a subir el primero → saldo $100.000 y tercer ciclo; preview solo dice que repite | No hay fecha de corte para identificar archivo viejo |
| R09 | $100.000 → $80.000 puede deberse a pago $20.000, o pago $70.000 + cargos $50.000 | Los cobros brutos no son identificables a partir de dos saldos |

Resultado estructurado preservado en [evidencias/RESULTADOS_CORTES.json](evidencias/RESULTADOS_CORTES.json). El script auxiliar queda en `evidencias/reproducir_cortes.py` como apoyo para una futura revisión; no es una suite de aceptación del producto objetivo.

## Hechos de interfaz derivados de fuente, no de nueva prueba de usuario

- El dashboard principal usa el último corte de cada mes para el gráfico y los ciclos como columna “Recordatorios”.
- La ficha dibuja cero en ciclos sin registro pero la tarjeta actual muestra guion si el cliente no aparece en el activo.
- Variación con base cero se muestra como falta de ciclo anterior.
- “Cobrado” se calcula en API pero no tiene una tarjeta en el dashboard actual.
- Las consultas se realizan separadamente sin una revisión de corte compartida. La mezcla por concurrencia es un riesgo deducido, no una carrera reproducida.

## Investigación externa

Twenty: modelo de datos, navegación, vistas, fichas, automatizaciones, correo, importación, API, extensiones, permisos, planes y autoalojamiento. Fuentes oficiales y aplicación al negocio en el documento 05. README/licencia y opciones de integración en 06. La comparación previa de SuiteCRM, Frappe CRM y EspoCRM permanece en 10.

Se detectaron límites/inconsistencias documentales en composición de mails y disponibilidad de campañas; por eso se exige prueba en versión fijada. No se asume equivalencia entre la rama main, la documentación actual y una edición desplegada.

## Pendiente de validar

- Export real de facturación, total de control, reglas de clave y composición del saldo.
- Recuperación ante fallos, concurrencia, publicación atómica y durabilidad de envíos en un despliegue real.
- Flujo completo con correo externo autorizado, adjuntos y cambios de cuenta.
- Instalación concreta de Twenty, español, permisos, adjuntos, vinculación a consorcios y migración histórica.
- Pruebas con el operador, accesibilidad formal y rendimiento con el volumen real.

No se reemplazó el dataset de demostración, no se corrigió código de aplicación, no se migró a Twenty y no se crearon tickets. Los hallazgos prueban límites del comportamiento actual; los documentos de reglas y aceptación proponen cómo corregirlos.
