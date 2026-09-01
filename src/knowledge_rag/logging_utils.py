from pathlib import Path


def safe_note_reference(vault_path: Path, note_path: Path) -> str:
    """Return a vault-relative reference suitable for normal application logs."""

    return (
        note_path.resolve()
        .relative_to(vault_path.resolve())
        .as_posix()
    )