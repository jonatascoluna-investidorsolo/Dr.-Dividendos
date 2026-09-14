from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Iterator

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # pragma: no cover
    psycopg = None
    dict_row = None


class DatabaseNotConfigured(RuntimeError):
    pass


def database_url() -> str | None:
    return os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")


@contextmanager
def connection() -> Iterator[Any]:
    url = database_url()
    if not url:
        raise DatabaseNotConfigured("DATABASE_URL/SUPABASE_DB_URL is not configured")
    if psycopg is None:
        raise RuntimeError("psycopg is required for PostgreSQL persistence")
    with psycopg.connect(url, row_factory=dict_row) as conn:
        yield conn


def fetch_all(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return list(cur.fetchall())


def fetch_one(sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None


def execute(sql: str, params: tuple[Any, ...] = ()) -> None:
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
