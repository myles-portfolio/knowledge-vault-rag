from knowledge_rag.ingest.chunker import chunk_markdown


def test_chunk_markdown_preserves_heading_context() -> None:
    content = "# Monitoring\n\nOverview text.\n\n## Alerts\n\nAlert details."

    chunks = chunk_markdown(content, max_chars=500)

    assert len(chunks) == 2
    assert chunks[0].heading_path == "Monitoring"
    assert chunks[1].heading_path == "Alerts"
    assert "Alert details." in chunks[1].content
