from pathlib import Path
from dd_engine.cvm.acquisition import sha256_file, build_manifest


def test_sha256_file(tmp_path: Path):
    p = tmp_path / "x.bin"
    p.write_bytes(b"abc")
    assert sha256_file(p) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_manifest_has_dfp_and_itr(tmp_path: Path, monkeypatch):
    def fake_download(url, dest, **kwargs):
        from dd_engine.cvm.acquisition import AcquisitionResult
        return AcquisitionResult("CVM", url, None, "UNREACHABLE", None, "now", "offline")
    monkeypatch.setattr("dd_engine.cvm.acquisition.download", fake_download)
    out = build_manifest(2026, tmp_path)
    assert [x.source for x in out] == ["DFP", "ITR"]
    assert all(x.status == "UNREACHABLE" for x in out)
