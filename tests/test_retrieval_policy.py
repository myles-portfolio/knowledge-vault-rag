from knowledge_rag.retrieval_policy import (
    RetrievedChunk,
    filter_external_generation_context,
    may_send_chunk_to_external_generation,
)


def make_chunk(ai_access: str) -> RetrievedChunk:
    return RetrievedChunk(
        source_path="Example.md",
        content="Synthetic test content.",
        ai_access=ai_access,
        metadata={},
    )


def test_allowed_chunk_may_be_sent_externally() -> None:
    chunk = make_chunk("allowed")

    assert may_send_chunk_to_external_generation(chunk) is True


def test_local_only_chunk_may_not_be_sent_externally() -> None:
    chunk = make_chunk("local-only")

    assert may_send_chunk_to_external_generation(chunk) is False


def test_unknown_policy_fails_closed() -> None:
    chunk = make_chunk("unexpected-value")

    assert may_send_chunk_to_external_generation(chunk) is False


def test_generation_context_filters_local_only_content() -> None:
    allowed = make_chunk("allowed")
    local_only = make_chunk("local-only")

    result = filter_external_generation_context(
        [allowed, local_only]
    )

    assert result == [allowed]