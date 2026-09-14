from __future__ import annotations
import argparse, json
from pathlib import Path
from dd_engine.cvm.client import CVMClient
from dd_engine.cvm.fca import parse_fca_zip
from dd_engine.cvm.universe import load_excel_universe
from dd_engine.validation import validate_universe, write_validation_csv


def main():
    p = argparse.ArgumentParser(description="Validate Doutor dos Dividendos universe against official CVM FCA.")
    p.add_argument("--excel", required=True)
    p.add_argument("--fca", help="Use a local FCA zip; otherwise download official FCA.")
    p.add_argument("--year", type=int, default=2026)
    p.add_argument("--out", default="artifacts/universe_validation.csv")
    args = p.parse_args()
    items = load_excel_universe(args.excel)
    fca = Path(args.fca) if args.fca else Path("data/raw") / f"fca_cia_aberta_{args.year}.zip"
    if not fca.exists():
        CVMClient().download_fca(args.year, fca)
    mappings = parse_fca_zip(fca)
    rows = validate_universe(items, mappings)
    write_validation_csv(rows, args.out)
    counts = {}
    for r in rows: counts[r.status] = counts.get(r.status, 0) + 1
    summary = {"universe_size": len(items), "mapping_rows": len(mappings), "status_counts": counts, "output": str(args.out)}
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
