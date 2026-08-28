from hashlib import sha256
from pathlib import Path
from uuid import UUID, uuid5


DOCUMENT_NAMESPACE = UUID("3de7f156-0d87-4b4c-9ab6-3fb7838d8f49")


def document_identity(vault_path: Path, note_path: Path) -> str:
    relative_path = note_path.resolve().relative_to(vault_path.resolve())
    normalized = relative_path.as_posix().lower()
    return str(uuid5(DOCUMENT_NAMESPACE, normalized))


def content_hash(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()