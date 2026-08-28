from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory

import psycopg

from knowledge_rag.config import settings
from knowledge_rag.ingest.persistence import persist_note


def create_test_tables(conn: psycopg.Connection) -> None:
    conn.execute(
        """
        CREATE TEMP TABLE documents (
            document_id BIGSERIAL PRIMARY KEY,
            document_uuid UUID NOT NULL UNIQUE,
            source_path TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            note_type TEXT,
            created_date DATE,
            status TEXT,
            metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
            content_hash TEXT NOT NULL,
            indexed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )

    conn.execute(
        """
        CREATE TEMP TABLE document_chunks (
            chunk_id BIGSERIAL PRIMARY KEY,
            document_id BIGINT NOT NULL,
            chunk_index INTEGER NOT NULL,
            heading_path TEXT,
            content TEXT NOT NULL,
            UNIQUE (document_id, chunk_index)
        );
        """
    )


def test_persist_note_inserts_skips_and_updates() -> None:
    test_root = Path(".test-temp")
    test_root.mkdir(exist_ok=True)

    sample_note = Path(
        "examples/sample-vault/20 Learning/Azure RBAC.md"
    )

    with TemporaryDirectory(dir=test_root) as temp_dir:
        vault_path = Path(temp_dir)
        note_dir = vault_path / "20 Learning"
        note_dir.mkdir()

        note_path = note_dir / "Azure RBAC.md"
        copy2(sample_note, note_path)

        with psycopg.connect(settings.database_url) as conn:
            create_test_tables(conn)

            first_result = persist_note(
                conn,
                vault_path,
                note_path,
            )

            second_result = persist_note(
                conn,
                vault_path,
                note_path,
            )

            document_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM documents;
                """
            ).fetchone()

            original_chunk_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM document_chunks;
                """
            ).fetchone()

            note_path.write_text(
                note_path.read_text(encoding="utf-8")
                + "\n\n"
                + "## Persistence Test\n\n"
                + "Changed content for automated testing.\n",
                encoding="utf-8",
            )

            third_result = persist_note(
                conn,
                vault_path,
                note_path,
            )

            updated_document_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM documents;
                """
            ).fetchone()

            updated_chunks = conn.execute(
                """
                SELECT heading_path, content
                FROM document_chunks
                ORDER BY chunk_index;
                """
            ).fetchall()

            assert first_result is True
            assert second_result is False
            assert third_result is True

            assert document_count is not None
            assert document_count[0] == 1

            assert original_chunk_count is not None
            assert original_chunk_count[0] > 0

            assert updated_document_count is not None
            assert updated_document_count[0] == 1

            assert any(
                heading == "Persistence Test"
                and "Changed content for automated testing." in content
                for heading, content in updated_chunks
            )