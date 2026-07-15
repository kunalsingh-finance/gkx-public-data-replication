"""Fail on restricted artifacts, local paths, or credential-like text."""

from pathlib import Path
import re


TEXT_SUFFIXES: set[str] = {".md", ".txt", ".py", ".toml", ".yaml", ".yml", ".json", ".csv", ".cff", ".gitignore"}
PATH_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"[A-Za-z]:\\Users\\"),
    re.compile(r"/Users/"),
    re.compile(r"/home/"),
)
SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
PROHIBITED_SUFFIXES: set[str] = {".pdf", ".zip", ".pyc", ".env"}
PROHIBITED_NAMES: set[str] = {"official_ML_Codes", "predictions", "portfolio_weights", "__pycache__", ".pytest_cache"}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if any(part in {".git", ".venv", "build", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        if path.is_dir() and path.name in PROHIBITED_NAMES:
            findings.append(f"prohibited directory: {path.relative_to(root).as_posix()}")
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in PROHIBITED_SUFFIXES:
            findings.append(f"prohibited file type: {path.relative_to(root).as_posix()}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 2_000_000:
            continue
        text = path.read_text(encoding="utf-8")
        if path.name != "scan_public_tree.py" and any(pattern.search(text) for pattern in PATH_PATTERNS):
            findings.append(f"machine-specific path: {path.relative_to(root).as_posix()}")
        if path.name != "scan_public_tree.py" and any(pattern.search(text) for pattern in SECRET_PATTERNS):
            findings.append(f"credential-like content: {path.relative_to(root).as_posix()}")
    if findings:
        raise ValueError("Public-tree scan failed:\n" + "\n".join(findings))
    print("Public tree contains no prohibited artifacts, local paths, or credential-like content.")


if __name__ == "__main__":
    main()
