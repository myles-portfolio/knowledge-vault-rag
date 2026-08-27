from knowledge_rag.ingest.models import DocumentChunk


def chunk_markdown(content: str, max_chars: int = 1800) -> list[DocumentChunk]:
    """Chunk Markdown by heading sections, splitting oversized sections by paragraph."""
    sections = _split_sections(content)
    chunks: list[DocumentChunk] = []

    for heading, section_text in sections:
        for piece in _split_oversized(section_text, max_chars=max_chars):
            if piece.strip():
                chunks.append(
                    DocumentChunk(
                        index=len(chunks),
                        content=piece.strip(),
                        heading_path=heading,
                    )
                )
    return chunks


def _split_sections(content: str) -> list[tuple[str | None, str]]:
    sections: list[tuple[str | None, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") and stripped.lstrip("#").startswith(" "):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = stripped.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, "\n".join(current_lines).strip()))

    return sections


def _split_oversized(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    pieces: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip()
        if current and len(candidate) > max_chars:
            pieces.append(current)
            current = paragraph
        else:
            current = candidate

    if current:
        pieces.append(current)

    return pieces
