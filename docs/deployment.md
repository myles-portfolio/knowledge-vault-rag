# Deployment Model

## Current target

The production-oriented deployment is a lightweight Linux container in the homelab. It will read from a synchronized replica of the private Obsidian vault rather than from the workstation directly.

Suggested starting allocation:

- 2 vCPU
- 2 GB RAM
- 24 to 32 GB root disk
- No GPU requirement

## Service responsibilities

The container is expected to host:

- PostgreSQL with pgvector
- Python ingestion code
- FastAPI retrieval service
- Scheduled or event-driven re-indexing

The LLM and embedding model remain external services during the initial implementation.

## Data mounts

The vault replica should be mounted read-only into the RAG service whenever practical. The application should never need write access to the canonical vault to answer questions.

Example conceptual layout:

```text
/mnt/knowledge-vault      # private synchronized Markdown replica
/opt/knowledge-vault-rag # application code
/var/lib/postgresql       # derived database state
```

Actual hostnames, private addresses, Syncthing device IDs, and private paths should remain in local deployment documentation rather than this public repository.

## Development

For public development, use `examples/sample-vault/` as `VAULT_PATH` and run PostgreSQL through Docker Compose.

```bash
cp .env.example .env
docker compose up -d
python -m pip install -e ".[dev]"
python scripts/inspect_vault.py
uvicorn knowledge_rag.api.main:app --reload
```

The `/health` endpoint can then be used to confirm the API process is running.
