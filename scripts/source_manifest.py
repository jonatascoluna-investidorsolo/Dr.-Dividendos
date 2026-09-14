import json
from pathlib import Path
from dd_engine.cvm.source_registry import source_manifest

out = Path('data/reference/cvm_sources.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(source_manifest(), ensure_ascii=False, indent=2), encoding='utf-8')
print(out)
