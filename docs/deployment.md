# Deployment Model

## Active homelab deployment

The RAG backend now runs in a dedicated Debian 13 Linux container on the homelab virtualization platform.

Current allocation:

- 2 vCPU
- 2 GB RAM
- 512 MB swap
- 32 GB root disk
- No GPU

The container currently hosts:

- PostgreSQL 17
- pgvector 0.8.0
- The `knowledge_rag` application database and restricted application role
- The future Python ingestion service
- The future FastAPI retrieval service

Embedding and language-model inference remain external services during the initial implementation.

## Development workstation

The public repository is cloned to the development workstation. A Python virtual environment is used locally for tests and application development.

Authenticated PostgreSQL connectivity from the workstation to the homelab database has been validated over the private LAN.

The local `.env` contains the private database connection string and is excluded from Git. Credentials and private network addressing must never be committed.

## Vault data path

The canonical Obsidian vault remains on the workstation. Syncthing replicates it to ZFS-backed homelab storage with staggered file versioning.

The real vault is intentionally not indexed yet. Until persistence and privacy controls are validated, development uses only:

```text
examples/sample-vault/
```

The future production ingestion service should consume the homelab replica and should use read-only access wherever practical.

## Database networking

PostgreSQL is configured to listen on its private LAN interface in addition to localhost. Authentication is controlled through `pg_hba.conf` with SCRAM authentication.

Deployment-specific addresses and credentials are intentionally omitted from this public repository.

For tighter access control, production rules should prefer specific trusted clients rather than broad network ranges.

## Portable development option

`docker-compose.yml` remains in the repository as a portable option for contributors or future isolated development environments. It is not required by the active homelab deployment.

## Operational follow-up

Before production vault indexing, complete these infrastructure tasks:

1. Configure scheduled backup protection for the RAG container and database state.
2. Perform and document a restore validation.
3. Add the RAG container to Checkmk.
4. Discover and monitor host resources, PostgreSQL health, and the future API service.
5. Validate alerting behavior.

## Next software milestone

Persist parsed documents and chunks from the synthetic sample vault into PostgreSQL while preserving stable document identity, metadata, content hashes, and vault-relative source paths.
