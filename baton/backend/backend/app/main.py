"""Steps 1, 2 and 4: the web API.

Run it with:  uvicorn app.main:app --reload
Then open:    http://127.0.0.1:8000/docs   (interactive page to try every route)
"""
import os
import sqlite3
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel, ConfigDict, Field

from . import db
from .chunking import chunk_text
from .redaction import redact

MAX_UPLOAD_BYTES = 1_000_000  # 1 MB is plenty for notes and chat exports
ALLOWED_TYPES = {".txt": "text", ".md": "markdown", ".csv": "csv"}

AccessLevel = Literal["public", "team", "lead_only", "restricted"]


class ProjectCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=100)


def get_conn(request: Request):
    """Give each request its own database connection, and always close it."""
    conn = db.connect(request.app.state.db_path)
    try:
        yield conn
    finally:
        conn.close()


Conn = Annotated[sqlite3.Connection, Depends(get_conn)]


def create_app(db_path: str | None = None) -> FastAPI:
    path = db_path or os.environ.get("BATON_DB", "baton.sqlite3")
    db.init_db(path)

    app = FastAPI(title="Baton API", version="0.1.0")
    app.state.db_path = path

    # ---- Step 1: health check -------------------------------------------
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # ---- projects ---------------------------------------------------------
    @app.post("/projects", status_code=201)
    def create_project(body: ProjectCreate, conn: Conn):
        return db.create_project(conn, body.name)

    @app.get("/projects/{project_id}")
    def read_project(project_id: int, conn: Conn):
        project = db.get_project(conn, project_id)
        if project is None:
            raise HTTPException(404, "Project not found")
        return project

    # ---- Step 2 + 3: upload, redact, chunk, store -------------------------
    @app.post("/projects/{project_id}/sources", status_code=201)
    async def upload_source(
        project_id: int,
        conn: Conn,
        file: UploadFile = File(...),
        access_level: AccessLevel = Form("team"),
    ):
        if db.get_project(conn, project_id) is None:
            raise HTTPException(404, "Project not found")

        filename = Path(file.filename or "").name
        kind = ALLOWED_TYPES.get(Path(filename).suffix.lower())
        if not filename or kind is None:
            raise HTTPException(415, f"Unsupported file type. Use: {', '.join(ALLOWED_TYPES)}")

        raw = await file.read(MAX_UPLOAD_BYTES + 1)
        if len(raw) > MAX_UPLOAD_BYTES:
            raise HTTPException(413, "File is larger than 1 MB")
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise HTTPException(400, "File must be UTF-8 text")
        if not text.strip():
            raise HTTPException(422, "File has no text")

        # Redact BEFORE storing, so sensitive details never reach the database.
        redacted = redact(text)
        chunks = chunk_text(redacted.text)
        source = db.add_source(
            conn, project_id, filename, kind, access_level, redacted.total, chunks
        )
        return {**source, "redaction_counts": redacted.counts}

    @app.get("/projects/{project_id}/sources")
    def list_sources(project_id: int, conn: Conn):
        if db.get_project(conn, project_id) is None:
            raise HTTPException(404, "Project not found")
        return db.list_sources(conn, project_id)

    @app.get("/sources/{source_id}/chunks")
    def list_chunks(source_id: int, conn: Conn):
        if db.get_source(conn, source_id) is None:
            raise HTTPException(404, "Source not found")
        return db.list_chunks(conn, source_id)

    # ---- Step 4: citations ------------------------------------------------
    @app.get("/chunks/{chunk_id}")
    def read_chunk(chunk_id: int, conn: Conn):
        row = db.get_chunk_with_source(conn, chunk_id)
        if row is None:
            raise HTTPException(404, "Chunk not found")
        # NOTE: access_level is returned but NOT enforced yet. Roles and
        # filtering come in a later step; do not expose this API publicly
        # with real data until then.
        return {
            "chunk_id": row["chunk_id"],
            "text": row["text"],
            "access_level": row["access_level"],
            "citation": {
                "source_id": row["source_id"],
                "filename": row["filename"],
                "start_line": row["start_line"],
                "end_line": row["end_line"],
                "label": db.citation_label(row["filename"], row["start_line"], row["end_line"]),
            },
        }

    return app


app = create_app()
