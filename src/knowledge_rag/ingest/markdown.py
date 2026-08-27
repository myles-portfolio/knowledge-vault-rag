from pathlib import Path

import frontmatter

from knowledge_rag.ingest.models import MarkdownDocument


DEFAULT_EXCLUDED_PARTS = {".git", ".obsidian", ".stversions", ".trash"}


def discover_markdown_files(vault_path: Path) -> list[Path]:
    """Return Markdown files under a vault while skipping implementation state."""
    files: list[Path] = []
    for path in vault_path.rglob("*.md"):
        if any(part in DEFAULT_EXCLUDED_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def load_markdown(path: Path) -> MarkdownDocument:
    """Load Markdown body and YAML frontmatter from one note."""
    note = frontmatter.load(path)
    metadata = dict(note.metadata)
    title = _title_from_content(note.content) or path.stem
    return MarkdownDocument(
        path=path,
        title=title,
        content=note.content.strip(),
        metadata=metadata,
    )


def _title_from_content(content: str) -> str | None:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None
