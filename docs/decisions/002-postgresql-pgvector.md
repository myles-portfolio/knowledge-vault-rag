# ADR 002: PostgreSQL with pgvector

## Status

Accepted

## Context

The system needs durable metadata storage, semantic vector retrieval, filtering, and a path toward hybrid lexical and vector search without introducing an additional specialized database early in the project.

## Decision

Use PostgreSQL for document metadata and chunk storage, with pgvector for embeddings and vector similarity search.

## Consequences

### Positive

- Relational metadata and vectors live together.
- Standard SQL remains available for inspection and filtering.
- The project can later combine PostgreSQL full-text search with vector retrieval.
- The database remains understandable and portable.

### Tradeoffs

- Embedding dimensions must match the selected model.
- Index tuning will matter as the vault grows.
- The schema must be migrated if embedding strategy changes materially.
