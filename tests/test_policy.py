from pathlib import Path

from knowledge_rag.policy import (
    AIAccess,
    evaluate_note_policy,
    note_type_is_excluded,
    path_is_excluded,
)


def test_allowed_policy() -> None:
    policy = evaluate_note_policy({"ai_access": "allowed"})

    assert policy.ai_access is AIAccess.ALLOWED
    assert policy.may_index is True
    assert policy.may_use_external_embeddings is True
    assert policy.may_send_to_external_generation is True


def test_local_only_policy() -> None:
    policy = evaluate_note_policy({"ai_access": "local-only"})

    assert policy.ai_access is AIAccess.LOCAL_ONLY
    assert policy.may_index is True
    assert policy.may_use_external_embeddings is False
    assert policy.may_send_to_external_generation is False


def test_exclude_policy() -> None:
    policy = evaluate_note_policy({"ai_access": "exclude"})

    assert policy.ai_access is AIAccess.EXCLUDE
    assert policy.may_index is False
    assert policy.may_use_external_embeddings is False
    assert policy.may_send_to_external_generation is False


def test_missing_policy_defaults_to_local_only() -> None:
    policy = evaluate_note_policy({})

    assert policy.ai_access is AIAccess.LOCAL_ONLY


def test_invalid_policy_defaults_to_local_only() -> None:
    policy = evaluate_note_policy({"ai_access": "something-else"})

    assert policy.ai_access is AIAccess.LOCAL_ONLY


def test_excluded_path_matches_folder() -> None:
    vault = Path("examples/sample-vault")
    note = vault / "10 Journal" / "Private Entry.md"

    assert path_is_excluded(
        vault,
        note,
        ("10 Journal",),
    ) is True


def test_nonexcluded_path_does_not_match() -> None:
    vault = Path("examples/sample-vault")
    note = vault / "20 Learning" / "Azure RBAC.md"

    assert path_is_excluded(
        vault,
        note,
        ("10 Journal",),
    ) is False


def test_excluded_note_type_matches_case_insensitively() -> None:
    metadata = {"type": "Journal"}

    assert note_type_is_excluded(
        metadata,
        ("journal",),
    ) is True


def test_note_type_not_excluded() -> None:
    metadata = {"type": "study-note"}

    assert note_type_is_excluded(
        metadata,
        ("journal",),
    ) is False