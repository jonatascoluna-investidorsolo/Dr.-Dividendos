from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import csv, io, zipfile
from typing import Iterable

@dataclass(frozen=True)
class StatementRow:
    document_type: str
    company_cvm_code: str | None
    company_name: str | None
    reference_period: str | None
    disclosure_date: str | None
    version: int | None
    statement: str | None
    account_code: str | None
    account_name: str | None
    value: float | None
    exercise_order: str | None
    raw: dict[str, str]

class CVMTableParser:
    """Parser for CVM's CSV-in-ZIP files. It tolerates column-case variations."""
    def _read_csv(self, raw: bytes) -> Iterable[dict[str, str]]:
        text = raw.decode("latin-1")
        sample = text[:8192]
        dialect = csv.Sniffer().sniff(sample, delimiters=";,	")
        reader = csv.DictReader(io.StringIO(text), dialect=dialect)
        for row in reader:
            yield {str(k).strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

    @staticmethod
    def _get(row: dict[str, str], *names: str) -> str | None:
        normalized = {k.upper().strip(): v for k, v in row.items()}
        for name in names:
            value = normalized.get(name.upper())
            if value not in (None, ""):
                return value
        return None

    @staticmethod
    def _float(value: str | None) -> float | None:
        if value in (None, ""):
            return None
        try:
            return float(value.replace(".", "").replace(",", "."))
        except ValueError:
            try: return float(value)
            except ValueError: return None

    def parse_zip(self, path: str | Path, document_type: str) -> list[StatementRow]:
        rows: list[StatementRow] = []
        with zipfile.ZipFile(path) as zf:
            for member in zf.namelist():
                if not member.lower().endswith(".csv"):
                    continue
                statement = Path(member).stem
                with zf.open(member) as fh:
                    for raw in self._read_csv(fh.read()):
                        rows.append(StatementRow(
                            document_type=document_type,
                            company_cvm_code=self._get(raw, "CD_CVM"),
                            company_name=self._get(raw, "DENOM_CIA", "DENOM_SOCIAL"),
                            reference_period=self._get(raw, "DT_REFER"),
                            disclosure_date=self._get(raw, "DT_RECEB", "DT_RECEBIMENTO"),
                            version=int(self._get(raw, "VERSAO") or 1),
                            statement=statement,
                            account_code=self._get(raw, "CD_CONTA"),
                            account_name=self._get(raw, "DS_CONTA"),
                            value=self._float(self._get(raw, "VL_CONTA")),
                            exercise_order=self._get(raw, "ORDEM_EXERC"),
                            raw=raw,
                        ))
        return rows
