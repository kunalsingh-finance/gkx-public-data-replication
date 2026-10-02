"""Verify committed public files without recreating research data or fitting models."""
from pathlib import Path
import hashlib
import json


def canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    return raw.replace(b"\r\n", b"\n")


def verify(root: Path) -> int:
    manifest = json.loads((root / "manifests/public_artifact_manifest.json").read_text())
    seen = set()
    for record in manifest["files"]:
        relative = Path(record["path"])
        path = (root / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(root.resolve()) or record["path"] in seen:
            raise ValueError("Invalid or duplicate manifest path")
        seen.add(record["path"])
        data = canonical_bytes(path)
        if len(data) != record["size_bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise ValueError(f"Public artifact identity mismatch: {record['path']}")
    return len(seen)


if __name__ == "__main__":
    print(f"Verified {verify(Path(__file__).resolve().parents[1])} committed public files (LF-normalized UTF-8 text).")
