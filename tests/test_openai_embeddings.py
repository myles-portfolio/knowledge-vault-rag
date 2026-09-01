from types import SimpleNamespace

from knowledge_rag.embeddings import OpenAIEmbeddingProvider


class FakeEmbeddingsClient:
    """Minimal fake for the OpenAI embeddings endpoint."""

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def create(
        self,
        *,
        model: str,
        input: str,
        dimensions: int,
    ) -> SimpleNamespace:
        self.calls.append(
            {
                "model": model,
                "input": input,
                "dimensions": dimensions,
            }
        )

        return SimpleNamespace(
            data=[
                SimpleNamespace(
                    embedding=[0.1, 0.2, 0.3, 0.4]
                )
            ]
        )


def test_openai_provider_returns_embedding() -> None:
    fake_embeddings = FakeEmbeddingsClient()

    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="test-model",
        dimensions=4,
        embeddings_endpoint=fake_embeddings,
    )

    result = provider.embed("Synthetic input")

    assert result == [0.1, 0.2, 0.3, 0.4]


def test_openai_provider_sends_expected_request() -> None:
    fake_embeddings = FakeEmbeddingsClient()

    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        model="test-model",
        dimensions=4,
        embeddings_endpoint=fake_embeddings,
    )

    provider.embed("Synthetic input")

    assert fake_embeddings.calls == [
        {
            "model": "test-model",
            "input": "Synthetic input",
            "dimensions": 4,
        }
    ]


def test_openai_provider_reports_dimensions() -> None:
    fake_embeddings = FakeEmbeddingsClient()

    provider = OpenAIEmbeddingProvider(
        api_key="test-key",
        dimensions=1536,
        embeddings_endpoint=fake_embeddings,
    )

    assert provider.dimensions == 1536