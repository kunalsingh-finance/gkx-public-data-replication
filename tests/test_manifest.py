import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

module_path = Path(__file__).resolve().parents[1] / "scripts/verify_public_manifest.py"
spec = importlib.util.spec_from_file_location("public_manifest", module_path)
manifest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manifest)


def test_manifest_rejects_changed_evidence_and_accepts_windows_line_endings(tmp_path):
    (tmp_path / "manifests").mkdir()
    content = b"frozen evidence\n"
    (tmp_path / "evidence.txt").write_bytes(content.replace(b"\n", b"\r\n"))
    record = {"path": "evidence.txt", "size_bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    (tmp_path / "manifests/public_artifact_manifest.json").write_text(json.dumps({"files": [record]}))
    assert manifest.verify(tmp_path) == 1
    (tmp_path / "evidence.txt").write_text("altered evidence\n")
    with pytest.raises(ValueError, match="identity mismatch"):
        manifest.verify(tmp_path)


def test_manifest_rejects_path_escape(tmp_path):
    (tmp_path / "manifests").mkdir()
    (tmp_path / "manifests/public_artifact_manifest.json").write_text(json.dumps({"files": [{"path": "../outside.txt"}]}))
    with pytest.raises(ValueError, match="manifest path"):
        manifest.verify(tmp_path)
