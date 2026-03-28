from pathlib import Path

_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
_cache: str | None = None


def load_knowledge() -> str:
    global _cache
    if _cache is not None:
        return _cache

    parts: list[str] = []
    for filename in ("root_rules.txt", "law_of_root.txt"):
        filepath = _KNOWLEDGE_DIR / filename
        if filepath.exists():
            parts.append(filepath.read_text(encoding="utf-8"))

    _cache = "\n\n---\n\n".join(parts)
    return _cache
