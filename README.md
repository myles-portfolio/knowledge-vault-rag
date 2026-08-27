# Knowledge Vault RAG

A public, sanitized implementation of a private-first personal knowledge assistant built around an Obsidian vault.

The private vault remains the authoritative source of truth. This repository contains only the software, architecture, infrastructure documentation, and synthetic sample content required to develop and demonstrate the system safely in public.

## Goals

- Preserve personal knowledge as human-readable Markdown.
- Use Obsidian for authoring, linking, and navigation.
- Synchronize a read-only copy of the vault to homelab infrastructure.
- Parse Markdown and structured frontmatter into a rebuildable search index.
- Store embeddings and metadata in PostgreSQL with pgvector.
- Expose retrieval and answer generation through a small FastAPI service.
- Return source references with generated answers.
- Keep private notes, credentials, internal documentation, and identifying infrastructure details out of the public repository.

## High-level architecture

```text
Obsidian on workstation
        |
        +--> private Git repository for vault history
        |
        +--> Syncthing
               |
               v
        Homelab vault replica
               |
               v
        Markdown ingestion
               |
               v
        PostgreSQL + pgvector
               |
               v
        Retrieval API
               |
               v
        External embedding and LLM APIs
```

## Design principles

1. The Markdown vault is canonical. The vector index is disposable and rebuildable.
2. Private knowledge never belongs in this public repository.
3. Retrieval should be inspectable. Answers should identify their source notes.
4. The first implementation favors understandable components over heavy AI frameworks.
5. Infrastructure should remain lightweight enough for modest homelab hardware.
6. Sanitized sample data should make the public project reproducible without exposing the real vault.

## Planned stack

| Layer | Technology |
| --- | --- |
| Knowledge authoring | Obsidian and Markdown |
| Synchronization | Syncthing |
| Application | Python |
| API | FastAPI |
| Database | PostgreSQL |
| Vector search | pgvector |
| Embeddings | External API |
| Generation | External LLM API |
| Packaging | Docker Compose |
| Deployment target | Lightweight Linux container |

## Repository layout

```text
.
├── docs/
├── examples/sample-vault/
├── infrastructure/
├── scripts/
├── sql/
├── src/knowledge_rag/
├── tests/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── pyproject.toml
```

## Roadmap

- [x] Phase 0: Private vault, Git history, Syncthing replica, and recovery testing
- [ ] Phase 1: Public repository and sanitized architecture documentation
- [ ] Phase 2: Markdown loading and frontmatter parsing
- [ ] Phase 3: Chunking and document identity
- [ ] Phase 4: PostgreSQL and pgvector persistence
- [ ] Phase 5: Embedding pipeline and semantic retrieval
- [ ] Phase 6: FastAPI query service
- [ ] Phase 7: Grounded answer generation with citations
- [ ] Phase 8: Hybrid lexical and vector search
- [ ] Phase 9: Retrieval evaluation and regression tests
- [ ] Phase 10: Simple web interface and operational hardening

## Privacy boundary

The real vault is intentionally excluded from this project. Never commit real journal entries, private bookmarks, employer documentation, credentials, internal hostnames, IP addresses, API keys, tokens, or private source paths.

Use `examples/sample-vault/` for synthetic or deliberately sanitized demonstration content.

## Status

Early architecture and scaffolding. Implementation is intentionally incremental so each layer can be understood, tested, and replaced independently.
