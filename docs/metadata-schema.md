# Vault Metadata Schema

The initial ingestion contract intentionally mirrors a small set of Obsidian properties rather than requiring a rigid taxonomy.

## Common properties

| Property | Type | Purpose |
| --- | --- | --- |
| `type` | string | Classifies the note, such as `study`, `technical`, `bookmark`, `project`, or `journal` |
| `topic` | list of strings | Broad subjects used for filtering and discovery |
| `created` | date string | Original capture date in `YYYY-MM-DD` form |
| `status` | string | Lightweight lifecycle such as `active`, `reference`, or `archived` |
| `source` | string | Optional URL, book, course, or other source reference |

## Type-specific properties

Technical notes may add `system` and `environment`. Study notes may add `course`. Meeting notes may add `participants`. Project notes may add `project`.

Unknown properties should be preserved in the JSON metadata column rather than discarded. This allows the vault schema to evolve without requiring a database migration for every new Obsidian property.

## Ingestion behavior

1. Parse YAML frontmatter from each Markdown note.
2. Preserve all frontmatter in `documents.metadata`.
3. Promote a small set of commonly queried fields into dedicated relational columns.
4. Derive the display title from the first level-one Markdown heading, falling back to the filename.
5. Preserve the vault-relative source path for citations and traceability.

## Privacy metadata

A future schema revision should add an explicit sensitivity or indexing policy field. Until that feature exists, sensitive paths should be excluded from ingestion through configuration rather than relying on the model to decide what is safe to send externally.
