# ADR 003: External Model APIs for Initial Inference

## Status

Accepted

## Context

The target homelab has sufficient resources for PostgreSQL, ingestion, and an API service, but local LLM inference would consume substantially more memory and would benefit from dedicated GPU hardware.

## Decision

Use external APIs for embeddings and answer generation in the initial implementation. Keep retrieval, metadata, indexing, and orchestration local.

## Consequences

### Positive

- Keeps homelab resource requirements small.
- Avoids a hardware upgrade solely for model inference.
- Allows the project to focus first on retrieval quality and system design.

### Tradeoffs

- Retrieved context may leave the local environment.
- API usage can incur variable cost.
- Model availability and behavior depend on an external provider.

## Follow-up

Add configurable exclusions and context inspection before sending retrieved content to external services. Local inference may be evaluated later as hardware and model requirements change.
