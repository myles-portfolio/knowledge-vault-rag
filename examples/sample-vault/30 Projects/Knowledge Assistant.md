---
type: project
topic:
  - rag
  - knowledge-management
created: "2026-08-26"
status: active
project: "Knowledge Assistant"
---

# Knowledge Assistant

## Objective

Build a private-first assistant that can retrieve and synthesize information from a personal Markdown knowledge base while preserving source traceability.

## Current State

The sample architecture uses Obsidian for authoring, Syncthing for replication, PostgreSQL with pgvector for derived retrieval state, and a small Python API layer.

## Decisions

The source vault remains canonical. The vector index is disposable. Public development uses synthetic notes only.

## Next Actions

Implement document identity, persistence, embeddings, and semantic retrieval.

## Related

[[Monitoring Concepts]]
[[Azure RBAC]]
