from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv, io, zipfile
from typing import Iterable

@dataclass(frozen=True)
class ArchiveTable:
    member: str
    columns: tuple[str, ...]
    row_count: int


def _decode(raw: bytes) -> str:
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("latin-1", errors="replace")


def inspect_csv_zip(path: str | Path, include_terms: Iterable[str] = ()) -> list[ArchiveTable]:
    terms = tuple(t.lower() for t in include_terms)
    out: list[ArchiveTable] = []
    with zipfile.ZipFile(path) as zf:
        for member in zf.namelist():
            if not member.lower().endswith(".csv"):
                continue
            if terms and not any(t in member.lower() for t in terms):
                continue
            raw = zf.read(member)
            text = _decode(raw)
            reader = csv.reader(io.StringIO(text), delimiter=';')
            try:
                header = next(reader)
            except StopIteration:
                continue
            rows = sum(1 for _ in reader)
            out.append(ArchiveTable(member, tuple(x.strip() for x in header), rows))
    return out
