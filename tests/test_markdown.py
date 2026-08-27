from pathlib import Path

from knowledge_rag.ingest.markdown import load_markdown


def test_load_markdown_parses_frontmatter(tmp_path: Path) -> None:
    note = tmp_path / "Example.md"
    note.write_text(
        "---\ntype: study\ntopic:\n  - azure\n---\n\n# Example Note\n\nBody text.\n",
        encoding="utf-8",
    )

    document = load_markdown(note)

    assert document.title == "Example Note"
    assert document.metadata["type"] == "study"
    assert document.metadata["topic"] == ["azure"]
    assert "Body text." in document.content
