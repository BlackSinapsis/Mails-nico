import os, sys, io, asyncio, json
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend'))
os.environ.update(DATABASE_URL='sqlite:///:memory:', SECRET_KEY='audit_only_synthetic_secret_not_used_for_login', ENCRYPTION_KEY=Fernet.generate_key().decode(), YAHOO_EMAIL='', YAHOO_APP_PASSWORD='', GMAIL_EMAIL='', GMAIL_APP_PASSWORD='')
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile
import openpyxl
from app.core.database import Base
from app.models import *
from app.models.ciclo import Ciclo
from app.models.envio import Envio, EstadoEnvio
from app.models.cliente_maestro import ClienteMaestro
from app.routers.ciclos import confirmar_ciclo, preview_ciclo
from app.routers.maestro import historial_cliente
from app.services.dashboard_service import resumen, evolucion, morosos, deudor_desde_por_clave
from app.services.excel_parser import parse_deudores, dedupe_deudores

def database():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return Session(engine)

def excel(rows):
    wb = openpyxl.Workbook()
    wb.active.append(['nro cliente', 'nombre', 'monto'])
    for k, amount in rows:
        wb.active.append([k, 'Consorcio ' + str(k), amount])
    b = io.BytesIO(); wb.save(b)
    return b.getvalue()

async def confirm(db, rows):
    # Do not consume StreamingResponse: no SMTP task starts. No app lifespan/IMAP.
    await confirmar_ciclo(file=UploadFile(io.BytesIO(excel(rows)), filename='corte.xlsx'), db=db, current_user=None)
    return db.query(Ciclo).filter(Ciclo.activo == True).one()

results = []
def record(name, data): results.append({'caso': name, 'resultado_observado': data})

async def main():
    with database() as db:
        await confirm(db, [('A', 100000)])
        await confirm(db, [('A', 100000)])
        record('R01 archivo repetido', {'ciclos': db.query(Ciclo).count(), 'rachas': [e.ciclo_numero for e in db.query(Envio).order_by(Envio.ciclo_numero)], 'recordatorios_reales': db.query(Envio).filter(Envio.message_id.isnot(None)).count()})
    with database() as db:
        first = await confirm(db, [('A', 100000)])
        await confirm(db, [])
        record('R02 archivo solo encabezados', {'ciclos': db.query(Ciclo).count(), 'deuda_actual': str(resumen(db).deuda_total), 'saldado_anterior': db.query(Envio).filter(Envio.ciclo_id == first.id).one().saldado_en is not None})
    with database() as db:
        await confirm(db, [('A', 150000)])
        await confirm(db, [('A', '150.000,50')])
        record('R03 monto textual argentino', {'deuda_actual': str(resumen(db).deuda_total), 'saldado_anterior': db.query(Envio).one().saldado_en is not None})
    with database() as db:
        first = await confirm(db, [('A', 100000)])
        first.creado_en = datetime(2026, 1, 1, tzinfo=timezone.utc); db.commit()
        second = await confirm(db, [('A', 100000)])
        second.creado_en = datetime(2026, 1, 16, tzinfo=timezone.utc); db.commit()
        before = str(deudor_desde_por_clave(db, {'A'}).get('A'))
        db.query(Envio).filter(Envio.ciclo_id == first.id).one().estado = EstadoEnvio.PAGO; db.commit()
        after_old_reply = str(deudor_desde_por_clave(db, {'A'}).get('A'))
        db.query(Envio).filter(Envio.ciclo_id == second.id).one().estado = EstadoEnvio.PAGO; db.commit()
        record('R04 correo PAGO altera continuidad del Excel', {'desde_antes': before, 'desde_despues_pago_antiguo': after_old_reply, 'deuda_actual_con_pago_actual': str(resumen(db).deuda_total), 'deudores_actuales': resumen(db).deudores, 'lista_antiguedad': len(morosos(db)), 'desde_con_pago_actual': deudor_desde_por_clave(db, {'A'}).get('A')})
    with database() as db:
        await confirm(db, [('A', 100000)])
        await confirm(db, [('A', 60000)])
        await confirm(db, [])
        history = historial_cliente('A', db=db, current_user=None)
        record('R05 reducciones parciales e historico', {'reducciones_api_por_corte': [str(c.cobrado) for c in evolucion(db)], 'saldado_historico_formula_perfil': str(sum((i.monto for i in history.items if i.saldado_en), Decimal(0))), 'saldo_actual_en_ficha': '—' if not any(i.ciclo_activo for i in history.items) else 'presente'})
    with database() as db:
        await confirm(db, [('A', 100000)])
        await confirm(db, [])
        await confirm(db, [('A', 120000)])
        record('R06 reaparicion tras ausencia valida', {'racha_actual': db.query(Envio).join(Ciclo).filter(Ciclo.activo == True).one().ciclo_numero, 'serie_saldos': [str(c.deuda_total) for c in evolucion(db)]})
    parsed, dropped = dedupe_deudores(parse_deudores(excel([('A', 100000), ('A', 25000)])))
    record('R07 duplicados', {'monto_conservado': str(parsed[0].monto), 'filas_descartadas': dropped})
    with database() as db:
        await confirm(db, [('A', 100000)])
        await confirm(db, [('A', 70000)])
        preview = await preview_ciclo(file=UploadFile(io.BytesIO(excel([('A', 100000)])), filename='viejo.xlsx'), db=db, current_user=None)
        await confirm(db, [('A', 100000)])
        record('R08 archivo viejo sin fecha de corte', {'saldo_antes': '70000', 'saldo_despues': str(resumen(db).deuda_total), 'preview_repiten': preview.repiten, 'preview_nuevos': preview.nuevos, 'cortes': db.query(Ciclo).count()})
    record('R09 limite matematico de dos fotos', {'saldo_anterior': 100000, 'saldo_actual': 80000, 'reduccion_observable': 20000, 'historia_posible_1': 'pago 20000, cargos 0', 'historia_posible_2': 'pago 70000, cargos 50000', 'conclusion': 'las dos historias producen el mismo Excel; el cobro real no es identificable con saldos solos'})
    out = ROOT / 'Documentos' / 'evidencias' / 'RESULTADOS_CORTES.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str) + '\n')
    print(json.dumps(results, ensure_ascii=False, indent=2, default=str))

asyncio.run(main())
