import os
import tempfile

from app import db
from app.chunking import chunk_text


def _fresh_conn():
    path = os.path.join(tempfile.mkdtemp(), "test.sqlite3")
    db.init_db(path)
    return db.connect(path)


def test_store_source_and_read_back_citation():
    conn = _fresh_conn()
    project = db.create_project(conn, "Tech Club")
    chunks = chunk_text("line one\nline two\n\nline four", max_chars=20)
    source = db.add_source(conn, project["id"], "notes.md", "markdown", "team", 0, chunks)

    assert source["chunk_count"] == len(chunks) >= 1
    stored = db.list_chunks(conn, source["id"])
    row = db.get_chunk_with_source(conn, stored[0]["id"])
    assert row["filename"] == "notes.md"
    assert (row["start_line"], row["end_line"]) == (chunks[0].start_line, chunks[0].end_line)


def test_citation_label_formats():
    assert db.citation_label("n.md", 4, 4) == "n.md, line 4"
    assert db.citation_label("n.md", 14, 18) == "n.md, lines 14\u201318"


def test_bad_access_level_is_rejected():
    conn = _fresh_conn()
    project = db.create_project(conn, "P")
    try:
        db.add_source(conn, project["id"], "x.md", "markdown", "everyone", 0, [])
    except Exception:
        return
    raise AssertionError("expected the database to reject an unknown access level")


def test_deleting_a_project_removes_its_sources_and_chunks():
    conn = _fresh_conn()
    project = db.create_project(conn, "P")
    db.add_source(conn, project["id"], "x.md", "markdown", "team", 0, chunk_text("hello"))
    conn.execute("DELETE FROM projects WHERE id = ?", (project["id"],))
    conn.commit()
    assert conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0] == 0
