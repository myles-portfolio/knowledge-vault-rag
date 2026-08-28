from knowledge_rag.config import settings
from knowledge_rag.db import get_connection
from knowledge_rag.ingest.markdown import discover_markdown_files
from knowledge_rag.ingest.persistence import persist_note


def main() -> None:
    vault_path = settings.vault_path

    with get_connection() as conn:
        for note_path in discover_markdown_files(vault_path):
            changed = persist_note(conn, vault_path, note_path)

            status = "indexed" if changed else "unchanged"
            relative_path = note_path.relative_to(vault_path)

            print(f"{status}: {relative_path}")


if __name__ == "__main__":
    main()