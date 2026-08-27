# Linux Container Deployment

The homelab deployment uses a dedicated Debian 13 Linux container for the RAG backend.

## Current resources

```text
vCPU: 2
RAM: 2 GB
Swap: 512 MB
Root disk: 32 GB
GPU: none
```

## Current responsibilities

- PostgreSQL 17
- pgvector 0.8.0
- Dedicated `knowledge_rag` database
- Restricted application database role
- Future Python ingestion process
- Future FastAPI service

The initial container does not run a local language model. Embedding and generation workloads use external APIs so the deployment remains appropriate for modest homelab hardware.

## Current state

Completed:

- Debian 13 container deployed
- Static private LAN addressing assigned
- PostgreSQL installed and running
- pgvector extension installed and enabled
- Application database and role created
- Remote PostgreSQL access restricted through `pg_hba.conf`
- Authenticated connectivity from the development workstation validated

Not started:

- Proxmox backup policy and restore validation
- Checkmk host onboarding and service monitoring
- Application code deployment
- Production vault mount or read-only access
- Scheduled ingestion

## Data separation

The private Obsidian vault is stored separately on ZFS-backed homelab storage and synchronized through Syncthing. The RAG container should eventually consume a read-only view of that replica where practical.

The vector database is derived state and should be rebuildable from the Markdown source.

## Security posture

- Keep the source vault separate from the public project repository.
- Do not store application credentials in Git.
- Restrict PostgreSQL network access to explicitly trusted clients.
- Do not expose PostgreSQL directly to the public internet.
- Avoid logging note bodies or retrieved private context during normal operation.
- Add privacy policy checks before production indexing or external model use.

Deployment-specific hostnames, addresses, credentials, and infrastructure identifiers belong in private operational documentation rather than this repository.
