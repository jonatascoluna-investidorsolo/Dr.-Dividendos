from dd_engine.cvm.source_registry import CVM_SOURCES, source_manifest

def test_required_sources_present():
    names = {s.name for s in CVM_SOURCES}
    assert {'CVM DFP','CVM ITR','CVM FCA','CVM Cadastro'} <= names

def test_manifest_shape():
    rows = source_manifest()
    assert all('url' in x and 'cadence' in x and 'priority' in x for x in rows)
