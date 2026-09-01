from dataclasses import dataclass
from typing import Any

from knowledge_rag.policy import AIAccess


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    """Minimal retrieved content needed for generation policy checks."""

    source_path: str
    content: str
    ai_access: str
    metadata: dict[str, Any]


def may_send_chunk_to_external_generation(chunk: RetrievedChunk) -> bool:
    """Return True only when retrieved content is explicitly externally allowed."""

    try:
        access = AIAccess(chunk.ai_access.strip().lower())
    except ValueError:
        # Unknown stored values fail closed.
        return False

    return access is AIAccess.ALLOWED


def filter_external_generation_context(
    chunks: list[RetrievedChunk],
) -> list[RetrievedChunk]:
    """Return only retrieved chunks permitted for external generation."""

    return [
        chunk
        for chunk in chunks
        if may_send_chunk_to_external_generation(chunk)
    ]