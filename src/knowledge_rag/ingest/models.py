from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class MarkdownDocument:
    path: Path
    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DocumentChunk:
    index: int
    content: str
    heading_path: str | None = None
