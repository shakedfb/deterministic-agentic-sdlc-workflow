-- Additional databases for the agentic SDLC platform (Temporal creates its own)
CREATE DATABASE agentic_sdlc;
CREATE USER agentic WITH PASSWORD 'agentic';
GRANT ALL PRIVILEGES ON DATABASE agentic_sdlc TO agentic;

\c agentic_sdlc;
GRANT ALL ON SCHEMA public TO agentic;

CREATE TABLE IF NOT EXISTS langgraph_checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    type TEXT,
    checkpoint JSONB NOT NULL,
    metadata_ JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

CREATE INDEX idx_checkpoints_thread ON langgraph_checkpoints(thread_id);
CREATE INDEX idx_checkpoints_created ON langgraph_checkpoints(created_at);
