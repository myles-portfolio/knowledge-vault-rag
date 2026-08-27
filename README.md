# Knowledge Vault RAG

A public, sanitized implementation of a private-first personal knowledge assistant built around an Obsidian vault.

The private vault remains the authoritative source of truth. This repository contains only the software, architecture, infrastructure documentation, and synthetic sample content required to develop and demonstrate the system safely in public.

## Goals

- Preserve personal knowledge as human-readable Markdown.
- Use Obsidian for authoring, linking, and navigation.
- Synchronize a protected replica of the vault to homelab infrastructure.
- Parse Markdown and structured frontmatter into a rebuildable search index.
- Store embeddings and metadata in PostgreSQL with pgvector.
- Expose retrieval and answer generation through a small FastAPI service.
- Return source references with generated answers.
- Keep private notes, credentials, internal documentation, and identifying infrastructure details out of the public repository.

## High-level architecture

```text
Workstation
├── Obsidian
│   └── Private Markdown vault
├── Private Git repository
└── Python development environment
        |
        +--> Syncthing
        |      |
        |      v
        |   Homelab vault replica
        |
        +--------------------------+
                                   |
                                   v
                         Dedicated RAG container
                         ├── PostgreSQL 17
                         ├── pgvector
                         ├── Markdown ingestion
                         └── FastAPI service
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
7. Development and production data remain separated. Public development uses only synthetic sample content until ingestion and privacy controls are validated.

## Current stack

| Layer | Technology | Status |
| --- | --- | --- |
| Knowledge authoring | Obsidian and Markdown | Operational |
| Vault version history | Private Git repository | Operational |
| Vault synchronization | Syncthing | Operational |
| Homelab vault storage | ZFS-backed storage | Operational |
| Application | Python | Scaffolded |
| API | FastAPI | Health endpoint scaffolded |
| Database | PostgreSQL 17 | Operational in homelab |
| Vector search | pgvector 0.8.0 | Enabled |
| Embeddings | External API | Planned |
| Generation | External LLM API | Planned |
| Production runtime | Dedicated Debian 13 LXC | Operational |

## Development model

Application development occurs from a workstation checkout of this public repository. The Python environment connects over the private LAN to the PostgreSQL instance hosted by the dedicated RAG container.

The real private vault is not used for development ingestion yet. Development continues against:

```text
examples/sample-vault/
```

This keeps parser, chunking, database persistence, and privacy behavior testable before any real personal data is indexed.

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

Docker Compose remains available as a portable development option, but the active homelab implementation uses PostgreSQL directly on the dedicated Linux container.

## Roadmap

- [x] Phase 0: Private Obsidian vault and initial metadata templates
- [x] Phase 1: Private Git history and synchronized homelab vault replica
- [x] Phase 2: Public repository and sanitized architecture documentation
- [x] Phase 3: Markdown loading, frontmatter parsing, and heading-aware chunking scaffold
- [x] Phase 4: Dedicated Debian RAG container deployed
- [x] Phase 5: PostgreSQL 17 and pgvector 0.8.0 installed and connectivity validated
- [ ] Phase 6: Persist parsed sample documents and chunks in PostgreSQL
- [ ] Phase 7: Privacy-aware indexing and retrieval policies
- [ ] Phase 8: Embedding pipeline and semantic retrieval
- [ ] Phase 9: FastAPI query service
- [ ] Phase 10: Grounded answer generation with citations
- [ ] Phase 11: Hybrid lexical and vector search
- [ ] Phase 12: Retrieval evaluation and regression tests
- [ ] Phase 13: Production vault indexing
- [ ] Phase 14: Web interface and operational hardening

## Infrastructure follow-up

The RAG container is operational, but two infrastructure controls remain open before the service is considered production-ready:

- Configure and validate backups for the RAG container and database state.
- Add the RAG container to Checkmk monitoring and validate service discovery and alerting.

## Privacy boundary

The real vault is intentionally excluded from this project. Never commit real journal entries, private bookmarks, employer documentation, credentials, internal hostnames, IP addresses, API keys, tokens, or private source paths.

Use `examples/sample-vault/` for synthetic or deliberately sanitized demonstration content.

The production system is expected to add explicit policy controls so notes can be excluded from indexing or restricted from being sent to external model APIs.

## Status

The infrastructure foundation is now operational. A private Obsidian vault is synchronized to protected homelab storage, the dedicated Debian RAG container is running, PostgreSQL 17 and pgvector 0.8.0 are available, and authenticated database connectivity from the development workstation has been validated.

The next software milestone is database persistence for parsed documents and chunks using only the synthetic sample vault.
