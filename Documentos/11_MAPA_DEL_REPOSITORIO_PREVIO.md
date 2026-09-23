> Antecedente preservado el 13/09/2026. Para el objetivo actualizado de cortes quincenales, las reglas y decisiones vigentes de análisis están en [00_INDICE.md](00_INDICE.md) y documentos 01–09. Este archivo conserva la revisión previa; no implica decisiones de implementación aprobadas.

# Mapa inicial del repositorio

Revisión estática del commit b8d0072 · 13/09/2026. No verifica producción ni ejecución de tests.

## 01 · Qué hace — Una mesa de trabajo para cobrar mejor

La empresa de mantenimiento de ascensores carga quién debe y el sistema prepara recordatorios personalizados para cada consorcio. Después permite seguir respuestas y ver la evolución de la deuda. El Excel informa la deuda; el correo aporta señales de respuesta. No hay conciliación bancaria.

## 02 · El recorrido — De una planilla a un seguimiento

Primero se carga el maestro de clientes, que aporta nombres y correos. En cada nueva ronda se sube el Excel de deudores. La vista previa separa para enviar, sin email y filtrados. Al confirmar se archiva el ciclo anterior, se crea el nuevo y se guardan sus envíos. SMTP manda los mensajes; SSE informa el progreso; IMAP revisa respuestas cada 10 minutos.

## 03 · Los datos — Un cliente puede aparecer en muchos ciclos

ClienteMaestro guarda el contacto actual y su baja voluntaria. Ciclo representa una ronda de trabajo. Envio conserva el monto, destinatario y estado de ese cliente en esa ronda. Plantilla define el mensaje; ConfiguracionSistema guarda proveedor y credenciales cifradas; User permite entrar. La relación Ciclo → Envio tiene clave foránea; la unión con el maestro se hace por clave_union.

## Módulos

- **Pantallas** — `frontend/src/App.tsx · pages/`: Login; Dashboard; Nuevo envío; Seguimiento; Maestro; Plantilla; Configuración; Perfil de cliente.
- **Comunicación** — `frontend/src/services/api.ts · hooks/`: Agrega el token, renueva la sesión si vence y consulta la API. React Query mantiene datos de servidor en pantalla.
- **Entrada del servidor** — `backend/app/main.py · routers/`: FastAPI registra ocho routers, seguridad HTTP, CORS, archivos subidos y el proceso de lectura de correo.
- **Excel y cruces** — `backend/app/services/excel_parser.py · excel_joiner.py`: Lee, elimina duplicados y cruza por clave; aplica bajas, monto mínimo y validación del correo.
- **Ciclos y envío** — `backend/app/routers/ciclos.py · services/smtp_sender.py`: La confirmación crea los registros. Una tarea en memoria envía por SMTP y comunica avances por SSE.
- **Respuestas** — `backend/app/services/imap_watcher.py · reply_classifier.py`: Relaciona respuestas con Message-ID y clasifica texto, adjuntos y rebotes.
- **Indicadores** — `backend/app/services/dashboard_service.py · ciclo_service.py`: Reconstruye evolución y antigüedad. Marca saldado por ausencia en el siguiente Excel.
- **Persistencia** — `backend/app/models/ · alembic/versions/`: Seis modelos y seis migraciones. SQLAlchemy permite SQLite local y PostgreSQL en producción según configuración.

## Hallazgos y límites

### Alta · riesgo por concurrencia: Dos procesos no comparten la cola

smtp_sender.py guarda el límite y los IDs en variables locales al proceso. gunicorn.conf.py configura dos workers por defecto. Pedidos atendidos por workers distintos pueden no ver los envíos del otro y superar el límite agregado. Falta reproducirlo con concurrencia controlada.

Evidencia: backend/app/services/smtp_sender.py; backend/gunicorn.conf.py.

### Media · contradicción comprobada: La vista previa puede escribir una plantilla

No crea ciclos ni envíos, pero llama a load_plantilla(), que crea y confirma una plantilla si aún no existe. Por eso “preview no escribe nada” no es estrictamente cierto en una base nueva.

Evidencia: backend/app/routers/ciclos.py; backend/app/services/db_config.py.

### Media · dato perdido: La localidad no llega al envío final

El cruce dispone de localidad, pero Envio no la conserva y smtp_sender construye el mensaje con localidad=None. Una plantilla que use esa variable pierde ese dato.

Evidencia: backend/app/services/excel_joiner.py; backend/app/models/envio.py; backend/app/services/smtp_sender.py.

### Media · interpretación del negocio: Pago no significa dinero acreditado

El clasificador considera adjuntos e incluso partes image/* como PAGO; una imagen de firma puede producir esa señal. Saldado por ausencia también depende de que el Excel nuevo esté completo. Son inferencias, no comprobación bancaria.

Evidencia: backend/app/services/reply_classifier.py; backend/app/services/ciclo_service.py.

### Media · despliegue y documentos: El mapa escrito quedó atrás del código

CLAUDE.md dice React 18, pero package.json declara React 19. render.yaml dice plan free mientras docs/PENDIENTES.md registra un cambio a Starter. CONTEXT.md aún pide definir columnas ya documentadas como confirmadas. El hosting real no fue consultado.

Evidencia: frontend/package.json; CLAUDE.md; CONTEXT.md; render.yaml; docs/PENDIENTES.md.

### Límite de alcance: Hay funciones futuras y pruebas pendientes

POST /ciclos/desde-api devuelve 501: la integración automática aún es futura. Hay una suite backend, pero no se ejecutó en este análisis: pytest no está disponible en el Python inspeccionado. No hay script de tests frontend en package.json.

Evidencia: backend/app/routers/ciclos.py; backend/tests/; frontend/package.json.

## Recorrido de lectura

CONTEXT.md → CLAUDE.md → frontend/src/App.tsx → backend/app/routers/ciclos.py → excel_parser.py y excel_joiner.py → models/envio.py → smtp_sender.py → imap_watcher.py → dashboard_service.py → backend/tests/.

## Skills e instrucciones

Se aplicó la skill Lavish para la explicación visual. No se encontró una skill llamada initialize map o pokoke en el repositorio; .claude/skills contiene .gitkeep. Las instrucciones existentes están en CLAUDE.md y .claude/rules; las decisiones en docs/adr. Este mapa es documentación de consulta, no una nueva skill ni una modificación de esas reglas.
