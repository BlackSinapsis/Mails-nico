# Filas, clave repetida y tope del Excel

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `backend/app/services/excel_parser.py`
- `backend/app/services/excel_joiner.py`
- `backend/tests/test_excel_parser.py`
- `backend/tests/test_excel_joiner.py`
- `backend/tests/test_ciclos.py`

## Decisión cerrada

Una fila por cliente. La clave repetida bloquea. No se suman facturas. El monto argentino se lee. La clave numérica sale en 8 dígitos. Una fila ilegible no entra al conjunto que salda.

## Resultado

El parser de deudores devuelve las filas válidas y la lista de errores. Una clave repetida, un monto ilegible o una clave vacía impiden armar el corte. La racha de cada clave se lee en una sola consulta.

## Criterios de aceptación

- Cada error trae fila, columna, valor y motivo, en castellano.
- Clave inválida, monto ilegible o clave repetida bloquean. Monto 0 o negativo es aviso y no bloquea.
- La clave numérica (`42`, `42.0`) se normaliza a 8 dígitos. `150.000,50` se lee como importe.
- Un archivo de más de unos pocos MB, o un XML descomprimido por encima del tope, se rechaza antes de `load_workbook`. Un `.xls` que no es xlsx no responde 500.
- `dedupe_deudores` deja de quedarse con la última fila. `test_dedupe_deudores_conserva_la_ultima_fila` pasa a esperar el bloqueo. El resto de `test_ciclos.py` no se reescribe: lo toma Guardar el corte sin enviar.
- `_ciclos_consecutivos_deudor` deja de consultar una vez por clave. Un test de cientos de filas cuenta las queries.
- No se edita el router ni la pantalla. Eso es Preview de errores en pantalla.
- Dinero en `Decimal`. Tests con el valor esperado escrito a mano.

## Pregunta

¿Cómo se impide que una fila mala, o una clave repetida, salde en silencio a quien seguía en el corte anterior?
