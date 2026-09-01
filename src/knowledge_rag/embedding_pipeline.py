from dataclasses import dataclass

from knowledge_rag.embeddings import EmbeddingProvider
from knowledge_rag.policy import AIAccess


@dataclass(frozen=True, slots=True)
class ChunkForEmbedding:
    """Chunk data required by the embedding pipeline."""

    chunk_id: int
    content: str
    ai_access: str


@dataclass(frozen=True, slots=True)
class EmbeddedChunk:
    """Embedding result ready for persistence."""

    chunk_id: int
    vector: list[float]


def may_use_external_embedding(chunk: ChunkForEmbedding) -> bool:
    """Return True only when chunk content may leave the local system."""

    try:
        access = AIAccess(chunk.ai_access.strip().lower())
    except ValueError:
        return False

    return access is AIAccess.ALLOWED


def embed_chunks(
    chunks: list[ChunkForEmbedding],
    provider: EmbeddingProvider,
) -> list[EmbeddedChunk]:
    """Embed only chunks permitted for the supplied external provider."""

    results: list[EmbeddedChunk] = []

    for chunk in chunks:
        if not may_use_external_embedding(chunk):
            continue

        vector = provider.embed(chunk.content)

        results.append(
            EmbeddedChunk(
                chunk_id=chunk.chunk_id,
                vector=vector,
            )
        )

    return results