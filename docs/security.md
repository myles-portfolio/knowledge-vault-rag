# Security and Privacy Boundary

## Public repository rule

Assume every committed file is permanently public.

Do not commit:

- Personal journal entries or private notes
- Employer or customer documentation
- Credentials, tokens, API keys, cookies, or certificates
- Private IP addresses, internal DNS names, or identifying hostnames
- Real Syncthing device IDs
- Personal browser exports or bookmark collections
- Private repository URLs
- Database dumps from the real system
- The real Obsidian vault or its Syncthing version store

## Development data

Use only `examples/sample-vault/` for tests, screenshots, demonstrations, and reproducible examples. Sample notes should be synthetic or deliberately sanitized.

## Secrets

Runtime secrets belong in `.env`, a secret manager, or deployment-specific protected configuration. `.env.example` documents variable names only.

## RAG-specific controls

Future implementation should support:

1. Path-level and note-type exclusion from indexing.
2. Metadata filters before retrieval.
3. Source citations in every generated answer.
4. Logging that avoids note bodies by default.
5. A clear boundary between local retrieval and context sent to external models.
6. Rebuildable indexes so database backups are not the sole copy of knowledge.

## Principle

The assistant is allowed to derive from the vault. It is never the authoritative owner of the vault.
