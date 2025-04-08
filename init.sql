-- EXTENSION PGVECTOR, menambahkan pgvector di postgresql.
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabel chat_history
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_input TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel chatbot_data
CREATE TABLE chatbot_data (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    embedding_vector VECTOR(1024),  -- Sesuai dengan pgvector
    additional_info JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON chatbot_data USING ivfflat (embedding_vector vector_cosine_ops) WITH (lists = 100);