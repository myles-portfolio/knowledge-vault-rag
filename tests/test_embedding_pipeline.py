from knowledge_rag.embedding_pipeline import (
    ChunkForEmbedding,
    embed_chunks,
)
from knowledge_rag.embeddings import DeterministicEmbeddingProvider


def test_allowed_chunk_is_embedded() -> None:
    provider = DeterministicEmbeddingProvider()

    chunks = [
        ChunkForEmbedding(
            chunk_id=1,
            content="Synthetic allowed content.",
            ai_access="allowed",
        )
    ]

    result = embed_chunks(chunks, provider)

    assert len(result) == 1
    assert result[0].chunk_id == 1


def test_local_only_chunk_is_not_embedded() -> None:
    provider = DeterministicEmbeddingProvider()

    chunks = [
        ChunkForEmbedding(
            chunk_id=1,
            content="Synthetic private content.",
            ai_access="local-only",
        )
    ]

    result = embed_chunks(chunks, provider)

    assert result == []


def test_unknown_policy_is_not_embedded() -> None:
    provider = DeterministicEmbeddingProvider()

    chunks = [
        ChunkForEmbedding(
            chunk_id=1,
            content="Synthetic content.",
            ai_access="unexpected",
        )
    ]

    result = embed_chunks(chunks, provider)

    assert result == []