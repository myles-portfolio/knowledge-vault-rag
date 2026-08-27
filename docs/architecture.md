# Architecture

## Purpose

Knowledge Vault RAG is designed as a private-first personal knowledge system. Obsidian and Markdown remain the authoritative knowledge layer. The RAG components index a synchronized replica and can be rebuilt without changing the source vault.

## Logical flow

```text
Workstation
  Obsidian
    |
    | local Markdown
    v
Private Knowledge Vault
    |
    +--> private Git history
    |
    +--> Syncthing
            |
            v
Homelab replica
    |
    v
Markdown loader
    |
    v
Frontmatter parser
    |
    v
Chunker
    |
    v
Embedding client
    |
    v
PostgreSQL + pgvector
    |
    v
Retriever
    |
    v
FastAPI
    |
    v
External LLM
```

## Trust boundaries

### Private source boundary

The real vault contains personal data and is never committed to this repository. The homelab replica is treated as private data.

### Public development boundary

This repository contains only code, sanitized configuration examples, synthetic notes, and non-identifying architecture documentation.

### External model boundary

Only the minimum retrieved context required for a query should be sent to external embedding or generation APIs. Later phases should add configurable exclusion rules for sensitive note types and paths.

## Initial deployment model

The production-oriented target is a lightweight Linux container hosting PostgreSQL, pgvector, the ingestion process, and FastAPI. Model inference remains external to avoid local GPU and memory requirements.

## Source of truth

The vector database is a derived index. If it is lost or corrupted, it should be possible to recreate it entirely from the vault replica.
