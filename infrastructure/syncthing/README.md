# Syncthing Integration

Syncthing replicates the private Obsidian vault from the editing workstation to homelab storage. This repository does not contain real device IDs, addresses, credentials, or the private vault.

## Recommended pattern

- Workstation copy: normal editing source
- Homelab copy: synchronized replica
- Homelab receiver: staggered file versioning enabled
- RAG service: read from the homelab replica, preferably read-only

## Recovery

Sync is not a backup by itself because deletions and bad edits can propagate. Receiver-side file versioning provides a recovery layer, while private Git history provides an independent history mechanism for text notes.

## Public documentation rule

Use placeholders in examples. Never commit real Syncthing device IDs, private addresses, GUI credentials, or screenshots containing them.
