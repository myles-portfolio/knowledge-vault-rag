from knowledge_rag.config import settings
from knowledge_rag.db import get_connection
from knowledge_rag.embedding_store import embed_missing_chunks
from knowledge_rag.embeddings import DeterministicEmbeddingProvider


def main() -> None:
    provider = DeterministicEmbeddingProvider(dimensions=1536)

    with get_connection() as conn:
        count = embed_missing_chunks(
            conn,
            provider,
        )

    print(f"embedded chunks: {count}")


if __name__ == "__main__":
    main()