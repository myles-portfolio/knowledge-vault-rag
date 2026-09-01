from pathlib import Path

from knowledge_rag.logging_utils import safe_note_reference


def test_safe_note_reference_is_vault_relative() -> None:
    vault = Path("examples/sample-vault")
    note = vault / "20 Learning" / "Azure RBAC.md"

    result = safe_note_reference(vault, note)

    assert result == "20 Learning/Azure RBAC.md"


def test_safe_note_reference_does_not_include_absolute_path() -> None:
    vault = Path("examples/sample-vault")
    note = vault / "20 Learning" / "Azure RBAC.md"

    result = safe_note_reference(vault, note)

    assert str(vault.resolve()) not in result