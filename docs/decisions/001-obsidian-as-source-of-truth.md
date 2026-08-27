# ADR 001: Obsidian Markdown as the Source of Truth

## Status

Accepted

## Context

The system needs to remain useful without the RAG service, preserve human-readable knowledge, support linking and metadata, and avoid locking personal information into a proprietary AI datastore.

## Decision

Use an Obsidian vault composed of ordinary Markdown files as the canonical knowledge source. The RAG database is derived state only.

## Consequences

### Positive

- Notes remain directly readable and editable.
- The knowledge base survives replacement of the AI stack.
- Git can provide text history.
- Structured frontmatter can support filtering and ingestion.

### Tradeoffs

- The ingestion pipeline must understand Markdown and frontmatter.
- Attachments need separate handling.
- Obsidian-specific links may require normalization later.
