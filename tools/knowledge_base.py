import re
from pathlib import Path

_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
_cache: str | None = None


def _clean_text(text: str) -> str:
    # Collapse runs of 3+ whitespace-only lines into one blank line
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    # Remove lines that are just whitespace
    lines = [line for line in text.split('\n') if line.strip() or line == '']
    return '\n'.join(lines)


def load_knowledge() -> str:
    global _cache
    if _cache is not None:
        return _cache

    # Only use The Law of Root — it's the authoritative, complete reference.
    # The Learning to Play guide is redundant and adds ~15k tokens of noise.
    filepath = _KNOWLEDGE_DIR / "law_of_root.txt"
    if filepath.exists():
        _cache = _clean_text(filepath.read_text(encoding="utf-8"))
    else:
        _cache = ""
    return _cache
