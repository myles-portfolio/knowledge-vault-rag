from knowledge_rag.config import settings
from knowledge_rag.embedding_factory import get_embedding_provider
from knowledge_rag.embeddings import (
    DeterministicEmbeddingProvider,
    OpenAIEmbeddingProvider,
)


def test_factory_uses_deterministic_provider_without_api_key(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        settings,
        "openai_api_key",
        None,
    )

    provider = get_embedding_provider()

    assert isinstance(
        provider,
        DeterministicEmbeddingProvider,
    )


def test_factory_uses_openai_provider_with_api_key(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        settings,
        "openai_api_key",
        "test-key",
    )

    provider = get_embedding_provider()

    assert isinstance(
        provider,
        OpenAIEmbeddingProvider,
    )