from knowledge_rag.config import settings
from knowledge_rag.ingest.chunker import chunk_markdown
from knowledge_rag.ingest.markdown import discover_markdown_files, load_markdown


def main() -> None:
    files = discover_markdown_files(settings.vault_path)
    print(f"Vault: {settings.vault_path}")
    print(f"Markdown files: {len(files)}")

    for path in files:
        document = load_markdown(path)
        chunks = chunk_markdown(document.content)
        relative = path.relative_to(settings.vault_path)
        print(f"{relative}: {len(chunks)} chunk(s), type={document.metadata.get('type')}")


if __name__ == "__main__":
    main()
