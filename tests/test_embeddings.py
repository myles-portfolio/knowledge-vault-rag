from knowledge_rag.embeddings import DeterministicEmbeddingProvider


def test_embedding_is_deterministic() -> None:
    provider = DeterministicEmbeddingProvider()

    first = provider.embed("Azure RBAC")
    second = provider.embed("Azure RBAC")

    assert first == second


def test_different_text_produces_different_embedding() -> None:
    provider = DeterministicEmbeddingProvider()

    first = provider.embed("Azure RBAC")
    second = provider.embed("PostgreSQL")

    assert first != second


def test_embedding_has_expected_dimensions() -> None:
    provider = DeterministicEmbeddingProvider(dimensions=8)

    result = provider.embed("Example")

    assert len(result) == 8