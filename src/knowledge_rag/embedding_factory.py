from knowledge_rag.config import settings
from knowledge_rag.embeddings import (
    DeterministicEmbeddingProvider,
    EmbeddingProvider,
    OpenAIEmbeddingProvider,
)


def get_embedding_provider() -> EmbeddingProvider:
    """Create the configured embedding provider."""

    if settings.openai_api_key:
        return OpenAIEmbeddingProvider(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
            dimensions=1536,
        )

    return DeterministicEmbeddingProvider(
        dimensions=1536,
    )