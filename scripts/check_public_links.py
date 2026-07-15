"""Check local Markdown links in the public candidate."""

from pathlib import Path
import re


MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")


def _local_target(document: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split("#", maxsplit=1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    return (document.parent / target).resolve()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if any(part in {".venv", "build"} for part in document.parts):
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = _local_target(document, raw_target)
            if target is not None and not target.exists():
                missing.append(f"{document.relative_to(root).as_posix()} -> {raw_target}")
    if missing:
        raise FileNotFoundError("Broken local Markdown links:\n" + "\n".join(missing))
    print("All local Markdown links resolve.")


if __name__ == "__main__":
    main()
