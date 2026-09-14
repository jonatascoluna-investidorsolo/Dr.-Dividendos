from __future__ import annotations

from dataclasses import asdict
from fastapi import FastAPI, HTTPException, Query

from .db import DatabaseNotConfigured
from .db.repository import company_detail, list_companies, quality_summary, radar, ranking
from .models import CompanyInput
from .quality_gate import evaluate_quality_gate
from .service import calculate_company

app = FastAPI(
    title="Doutor dos Dividendos API",
    version="2.4.0",
    description="API de consulta do motor financeiro e dos dados persistidos.",
)


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.4.0", "database": "configured" if _db_configured() else "not_configured"}


@app.post("/calculate")
def calculate(company: CompanyInput):
    return asdict(calculate_company(company))


def _db_configured() -> bool:
    from .db import database_url
    return bool(database_url())


def _db_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except DatabaseNotConfigured:
        raise HTTPException(503, "Banco de dados não configurado")
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@app.get("/api/ativos")
def ativos(limit: int = Query(200, ge=1, le=500), offset: int = Query(0, ge=0)):
    return {"items": _db_call(list_companies, limit, offset), "limit": limit, "offset": offset}


@app.get("/api/ativos/{ticker}")
def ativo(ticker: str):
    result = _db_call(company_detail, ticker.upper())
    if not result:
        raise HTTPException(404, "Ativo não encontrado")
    return result


@app.get("/api/ranking/{metric}")
def ranking_api(metric: str, limit: int = Query(20, ge=1, le=100), ascending: bool = False):
    return {"metric": metric, "items": _db_call(ranking, metric, limit, ascending)}


@app.get("/api/radar")
def radar_api(limit: int = Query(50, ge=1, le=200)):
    return {"items": _db_call(radar, limit)}


@app.get("/api/qualidade-dados")
def qualidade_dados():
    return _db_call(quality_summary)
