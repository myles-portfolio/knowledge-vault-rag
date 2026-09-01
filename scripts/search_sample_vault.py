from knowledge_rag.db import get_connection
from knowledge_rag.embeddings import DeterministicEmbeddingProvider
from knowledge_rag.retrieval import semantic_search


def main() -> None:
    provider = DeterministicEmbeddingProvider(dimensions=1536)

    with get_connection() as conn:
        results = semantic_search(
            conn,
            provider,
            query="Azure permissions and role assignments",
            limit=5,
        )

    for result in results:
        print(
            result.source_path,
            result.heading_path,
            round(result.distance, 4),
        )


if __name__ == "__main__":
    main()