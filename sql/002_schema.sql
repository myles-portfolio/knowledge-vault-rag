CREATE TABLE IF NOT EXISTS documents (
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

CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    heading_path TEXT,
    content TEXT NOT NULL,
    token_estimate INTEGER,
    embedding VECTOR(1536),
    UNIQUE (document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_documents_type
ON documents(note_type);

CREATE INDEX IF NOT EXISTS idx_documents_metadata
ON documents USING GIN(metadata);