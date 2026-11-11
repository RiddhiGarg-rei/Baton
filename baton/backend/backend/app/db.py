"""Step 3: the database (SQLite, using Python's built-in sqlite3).

Three tables, each pointing to the one before it:
    projects -> sources (an uploaded file) -> chunks (a piece of that file)

Each source carries an access level now, even though it is not enforced yet.
Enforcing it (roles and filtering) is a later step.
"""
import sqlite3
from typing import Iterable

from .chunking import Chunk

ACCESS_LEVELS = ("public", "team", "lead_only", "restricted")

SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sources (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    filename     TEXT NOT NULL,
    kind         TEXT NOT NULL,
    access_level TEXT NOT NULL
                 CHECK (access_level IN ('public', 'team', 'lead_only', 'restricted')),
    redactions   INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chunks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id   INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    start_line  INTEGER NOT NULL,
    end_line    INTEGER NOT NULL,
    text        TEXT NOT NULL,
    UNIQUE (source_id, chunk_index)
);
"""


def connect(path: str) -> sqlite3.Connection:
    # check_same_thread=False because FastAPI may use different worker
    # threads within one request. Each request still gets its own connection.
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: str) -> None:
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def _one(row: sqlite3.Row | None) -> dict | None:
    return dict(row) if row else None


# ---- projects -------------------------------------------------------------

def create_project(conn: sqlite3.Connection, name: str) -> dict:
    cur = conn.execute("INSERT INTO projects (name) VALUES (?)", (name,))
    conn.commit()
    return get_project(conn, cur.lastrowid)  # type: ignore[arg-type, return-value]


def get_project(conn: sqlite3.Connection, project_id: int) -> dict | None:
    return _one(conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone())


# ---- sources --------------------------------------------------------------

def add_source(
    conn: sqlite3.Connection,
    project_id: int,
    filename: str,
    kind: str,
    access_level: str,
    redactions: int,
    chunks: Iterable[Chunk],
) -> dict:
    """Store a source and all of its chunks in one transaction."""
    try:
        cur = conn.execute(
            "INSERT INTO sources (project_id, filename, kind, access_level, redactions) "
            "VALUES (?, ?, ?, ?, ?)",
            (project_id, filename, kind, access_level, redactions),
        )
        source_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO chunks (source_id, chunk_index, start_line, end_line, text) "
            "VALUES (?, ?, ?, ?, ?)",
            [(source_id, c.index, c.start_line, c.end_line, c.text) for c in chunks],
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return get_source(conn, source_id)  # type: ignore[arg-type, return-value]


_SOURCE_SELECT = (
    "SELECT s.*, (SELECT COUNT(*) FROM chunks c WHERE c.source_id = s.id) AS chunk_count "
    "FROM sources s"
)


def get_source(conn: sqlite3.Connection, source_id: int) -> dict | None:
    return _one(conn.execute(f"{_SOURCE_SELECT} WHERE s.id = ?", (source_id,)).fetchone())


def list_sources(conn: sqlite3.Connection, project_id: int) -> list[dict]:
    rows = conn.execute(f"{_SOURCE_SELECT} WHERE s.project_id = ? ORDER BY s.id", (project_id,))
    return [dict(r) for r in rows]


# ---- chunks and citations -------------------------------------------------

def list_chunks(conn: sqlite3.Connection, source_id: int) -> list[dict]:
    rows = conn.execute(
        "SELECT id, source_id, chunk_index, start_line, end_line, text "
        "FROM chunks WHERE source_id = ? ORDER BY chunk_index",
        (source_id,),
    )
    return [dict(r) for r in rows]


def get_chunk_with_source(conn: sqlite3.Connection, chunk_id: int) -> dict | None:
    row = conn.execute(
        "SELECT c.id AS chunk_id, c.text, c.start_line, c.end_line, "
        "       s.id AS source_id, s.filename, s.access_level "
        "FROM chunks c JOIN sources s ON s.id = c.source_id WHERE c.id = ?",
        (chunk_id,),
    ).fetchone()
    return _one(row)


def citation_label(filename: str, start_line: int, end_line: int) -> str:
    """Human-readable citation, e.g. 'notes.md, lines 14-18'."""
    if start_line == end_line:
        return f"{filename}, line {start_line}"
    return f"{filename}, lines {start_line}\u2013{end_line}"
