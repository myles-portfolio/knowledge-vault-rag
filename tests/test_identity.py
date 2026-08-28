from pathlib import Path

from knowledge_rag.ingest.identity import content_hash, document_identity


def test_document_identity_is_stable() -> None:
    vault = Path("examples/sample-vault")
    note = vault / "20 Learning" / "Azure RBAC.md"

    first = document_identity(vault, note)
    second = document_identity(vault, note)

    assert first == second


def test_document_identity_changes_with_path() -> None:
    vault = Path("examples/sample-vault")

    first = document_identity(
        vault,
        vault / "20 Learning" / "Azure RBAC.md",
    )
    second = document_identity(
        vault,
        vault / "40 Reference" / "Azure RBAC.md",
    )

    assert first != second


def test_content_hash_is_stable() -> None:
    assert content_hash("hello") == content_hash("hello")


def test_content_hash_changes_with_content() -> None:
    assert content_hash("hello") != content_hash("hello world")