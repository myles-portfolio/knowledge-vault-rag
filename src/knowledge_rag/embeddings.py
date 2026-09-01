from abc import ABC, abstractmethod
from hashlib import sha256
from typing import Any, Protocol, cast

from openai import OpenAI


class EmbeddingsEndpoint(Protocol):
    """Subset of the embeddings API required by this application."""

    def create(
        self,
        *,
        model: str,
        input: str,
        dimensions: int,
    ) -> Any:
        ...


class EmbeddingProvider(ABC):
    """Interface implemented by embedding providers."""

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Number of dimensions returned by this provider."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return an embedding vector for the supplied text."""


class DeterministicEmbeddingProvider(EmbeddingProvider):
    """Small deterministic provider intended for tests and local development."""

    def __init__(self, dimensions: int = 8) -> None:
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, text: str) -> list[float]:
        digest = sha256(text.encode("utf-8")).digest()

        values = [
            digest[index % len(digest)] / 255.0
            for index in range(self.dimensions)
        ]

        magnitude = sum(value * value for value in values) ** 0.5

        if magnitude == 0:
            return values

        return [
            value / magnitude
            for value in values
        ]


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """Embedding provider backed by the OpenAI API."""

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
        embeddings_endpoint: EmbeddingsEndpoint | None = None,
    ) -> None:
        if embeddings_endpoint is None:
            client = OpenAI(api_key=api_key)

            self._embeddings = cast(
                EmbeddingsEndpoint,
                client.embeddings,
            )
        else:
            self._embeddings = embeddings_endpoint

        self._model = model
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, text: str) -> list[float]:
        response = self._embeddings.create(
            model=self._model,
            input=text,
            dimensions=self._dimensions,
        )

        return response.data[0].embedding