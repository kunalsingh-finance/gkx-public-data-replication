"""Create a deterministic SHA-256 manifest of public release artifacts."""

from pathlib import Path
import hashlib
import json
from verify_public_manifest import canonical_bytes


EXCLUDED_PARTS: set[str] = {".git", ".venv", "build", "__pycache__", ".pytest_cache"}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output_path = root / "manifests" / "public_artifact_manifest.json"
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in EXCLUDED_PARTS or part.endswith(".egg-info") for part in path.parts) or path == output_path:
            continue
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(canonical_bytes(path)).hexdigest(),
                "size_bytes": len(canonical_bytes(path)),
            }
        )
    output_path.write_text(json.dumps({"manifest_version": 2, "text_identity": "UTF-8 text with CRLF normalized to LF; binary bytes unchanged", "files": records}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
