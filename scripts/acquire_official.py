#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from dd_engine.cvm.acquisition import build_manifest

p=argparse.ArgumentParser(description="Aquisição auditável de DFP/ITR oficiais da CVM")
p.add_argument('--year',type=int,default=2026)
p.add_argument('--output',default='data/cvm/raw')
a=p.parse_args()
res=build_manifest(a.year,Path(a.output))
print(json.dumps([r.__dict__ for r in res],ensure_ascii=False,indent=2))
raise SystemExit(0 if all(r.status=='DOWNLOADED' for r in res) else 2)
