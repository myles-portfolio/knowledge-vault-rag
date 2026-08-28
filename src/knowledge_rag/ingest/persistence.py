from pathlib import Path

from psycopg import Connection
from psycopg.types.json import Jsonb

from knowledge_rag.ingest.chunker import chunk_markdown
from knowledge_rag.ingest.identity import content_hash, document_identity
from knowledge_rag.ingest.markdown import load_markdown


def persist_note(
    conn: Connection,
    vault_path: Path,
    note_path: Path,
) -> bool:
    document = load_markdown(note_path)

    source_path = note_path.resolve().relative_to(vault_path.resolve()).as_posix()
    document_uuid = document_identity(vault_path, note_path)
    digest = content_hash(document.content)

    existing = conn.execute(
        """
        SELECT document_id, content_hash
        FROM documents
        WHERE source_path = %s;
        """,
        (source_path,),
    ).fetchone()

    if existing is not None and existing[1] == digest:
        return False

    metadata = document.metadata

    row = conn.execute(
        """
        INSERT INTO documents (
            document_uuid,
            source_path,
            title,
            note_type,
            created_date,
            status,
            metadata,
            content_hash,
            indexed_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (source_path)
        DO UPDATE SET
            title = EXCLUDED.title,
            note_type = EXCLUDED.note_type,
            created_date = EXCLUDED.created_date,
            status = EXCLUDED.status,
            metadata = EXCLUDED.metadata,
            content_hash = EXCLUDED.content_hash,
            indexed_at = NOW()
        RETURNING document_id;
        """,
        (
            document_uuid,
            source_path,
            document.title,
            metadata.get("type"),
            metadata.get("created"),
            metadata.get("status"),
            Jsonb(metadata),
            digest,
        ),
    ).fetchone()

    if row is None:
        raise RuntimeError(f"Failed to persist document: {source_path}")

    document_id = row[0]

    conn.execute(
        """
        DELETE FROM document_chunks
        WHERE document_id = %s;
        """,
        (document_id,),
    )

    chunks = chunk_markdown(document.content)

    for chunk in chunks:
        conn.execute(
            """
            INSERT INTO document_chunks (
                document_id,
                chunk_index,
                heading_path,
                content
            )
            VALUES (%s, %s, %s, %s);
            """,
            (
                document_id,
                chunk.index,
                chunk.heading_path,
                chunk.content,
            ),
        )

    return True