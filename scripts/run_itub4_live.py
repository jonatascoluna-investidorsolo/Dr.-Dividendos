#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from dd_engine.cvm.itub4 import prepare_itub4


def main() -> int:
    p = argparse.ArgumentParser(description="Baixa e valida DFP/ITR oficiais da CVM para ITUB4.")
    p.add_argument("--year", type=int, default=2026)
    p.add_argument("--cvm-code", required=True, help="Código CVM confirmado no FCA/Cadastro")
    p.add_argument("--output", default="data/cvm/itub4")
    args = p.parse_args()
    result = prepare_itub4(args.year, Path(args.output), args.cvm_code)
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    return 0 if result.status == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
