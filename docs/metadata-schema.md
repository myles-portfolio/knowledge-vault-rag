# Vault Metadata Schema

The ingestion contract intentionally mirrors a small set of Obsidian properties rather than requiring a rigid taxonomy.

Unknown properties are preserved so the vault schema can evolve without requiring a database migration for every new property.

## Common properties

| Property    | Type            | Purpose                                                                                |
| ----------- | --------------- | -------------------------------------------------------------------------------------- |
| `type`      | string          | Classifies the note, such as `study`, `technical`, `bookmark`, `project`, or `journal` |
| `topic`     | list of strings | Broad subjects used for filtering and discovery                                        |
| `created`   | date string     | Original capture date in `YYYY-MM-DD` form                                             |
| `status`    | string          | Lightweight lifecycle such as `active`, `reference`, or `archived`                     |
| `source`    | string          | Optional URL, book, course, or other source reference                                  |
| `ai_access` | string          | Controls whether note content may be indexed locally or sent to external AI providers  |

## AI access policy

`ai_access` supports three values.

### `allowed`

The note may:

- enter the local searchable index
- be sent to an approved external embedding provider
- be included in context sent to an approved external generation model

Example:

```yaml
ai_access: allowed
```

### `local-only`

The note may enter the local searchable index but its content must remain within the local environment.

It must not be sent to external embedding or generation APIs.

Example:

```yaml
ai_access: local-only
```

### `exclude`

The note must not enter the searchable index.

Example:

```yaml
ai_access: exclude
```

## Default behavior

If `ai_access` is missing, malformed, or contains an unsupported value, the effective policy is:

```yaml
ai_access: local-only
```

This ensures that external disclosure requires explicit authorization.

## Configuration-level exclusions

The application also supports exclusions based on:

- vault-relative paths
- note types

These controls operate independently of frontmatter.

A configured exclusion takes precedence over `ai_access: allowed`.

## Type-specific properties

Technical notes may add `system` and `environment`.

Study notes may add `course`.

Meeting notes may add `participants`.

Project notes may add `project`.

Unknown properties should be preserved in the JSON metadata column rather than discarded.

## Ingestion behavior

1. Parse YAML frontmatter from each Markdown note.
2. Evaluate configured path exclusions.
3. Evaluate configured note-type exclusions.
4. Resolve the effective `ai_access` policy.
5. Reject notes whose effective policy prohibits indexing.
6. Preserve all frontmatter in `documents.metadata`.
7. Promote commonly queried fields into dedicated relational columns.
8. Persist the effective `ai_access` value as a dedicated database field.
9. Derive the display title from the first level-one Markdown heading, falling back to the filename.
10. Preserve the vault-relative source path for citations and traceability.

## Retrieval behavior

Local retrieval may return both:

- `allowed`
- `local-only`

Before content is sent to an external generation model, retrieved chunks must pass an additional policy check.

Only `allowed` content may be included in external generation context.

The same policy boundary applies before content is submitted to an external embedding provider.
