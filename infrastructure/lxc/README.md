# Linux Container Deployment

The intended homelab deployment is a small Linux container dedicated to the RAG backend.

## Starting resources

```text
vCPU: 2
RAM: 2 GB
Root disk: 24 to 32 GB
GPU: none
```

## Responsibilities

- Run PostgreSQL with pgvector
- Run the Python ingestion process
- Run the FastAPI service
- Read a mounted or otherwise available private vault replica

## Non-responsibilities

The initial container does not run a local language model. Embedding and generation workloads use external APIs so the deployment remains appropriate for modest homelab hardware.

## Security posture

The RAG process should not require write access to the source vault. Deployment-specific addresses, mount paths, credentials, and hostnames belong in private operational documentation.
