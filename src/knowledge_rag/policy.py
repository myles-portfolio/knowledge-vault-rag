from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any


class AIAccess(StrEnum):
    """Supported privacy states for note content."""

    ALLOWED = "allowed"
    LOCAL_ONLY = "local-only"
    EXCLUDE = "exclude"


@dataclass(frozen=True, slots=True)
class ContentPolicy:
    """Resolved policy decisions for one note."""

    ai_access: AIAccess

    @property
    def may_index(self) -> bool:
        """Whether the note may enter the local searchable index."""
        return self.ai_access is not AIAccess.EXCLUDE

    @property
    def may_use_external_embeddings(self) -> bool:
        """Whether note content may be sent to an external embedding API."""
        return self.ai_access is AIAccess.ALLOWED

    @property
    def may_send_to_external_generation(self) -> bool:
        """Whether retrieved note content may be sent to an external LLM."""
        return self.ai_access is AIAccess.ALLOWED


def evaluate_note_policy(metadata: dict[str, Any]) -> ContentPolicy:
    """Resolve frontmatter into an effective privacy policy.

    Missing, malformed, or unknown values fall back to local-only so
    externally permitted access must be explicitly granted.
    """
    value = metadata.get("ai_access")

    if not isinstance(value, str):
        return ContentPolicy(ai_access=AIAccess.LOCAL_ONLY)

    try:
        access = AIAccess(value.strip().lower())
    except ValueError:
        access = AIAccess.LOCAL_ONLY

    return ContentPolicy(ai_access=access)


def path_is_excluded(
    vault_path: Path,
    note_path: Path,
    excluded_paths: tuple[str, ...],
) -> bool:
    """Return True when a note resides in a configured excluded path."""

    # Store and compare paths in vault-relative POSIX form so policy
    # behavior is portable between Windows and Linux.
    relative_path = (
        note_path.resolve()
        .relative_to(vault_path.resolve())
        .as_posix()
        .lower()
    )

    return any(
        relative_path == excluded.lower().strip("/")
        or relative_path.startswith(excluded.lower().strip("/") + "/")
        for excluded in excluded_paths
    )


def note_type_is_excluded(
    metadata: dict[str, Any],
    excluded_note_types: tuple[str, ...],
) -> bool:
    """Return True when the note's frontmatter type is excluded."""

    note_type = metadata.get("type")

    # Notes without a usable type are not excluded by type policy.
    if not isinstance(note_type, str):
        return False

    normalized = note_type.strip().lower()

    return normalized in {
        value.strip().lower()
        for value in excluded_note_types
    }