import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import create_app  # noqa: E402

NOTES = (
    "# Notes\n\nDecision: keep the form in the club workspace.\n"
    "Contact: sponsor.desk@example.com\n"
    "api_key = sk-ABCDEFGHIJKLMNOPQRSTUV\n"
)


@pytest.fixture()
def client(tmp_path):
    return TestClient(create_app(str(tmp_path / "api.sqlite3")))


def _project(client):
    return client.post("/projects", json={"name": "Tech Club"}).json()["id"]


def _upload(client, pid, name="notes.md", content=NOTES, level="team"):
    return client.post(
        f"/projects/{pid}/sources",
        files={"file": (name, content.encode(), "text/markdown")},
        data={"access_level": level},
    )


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_upload_redacts_chunks_and_gives_citation(client):
    pid = _project(client)
    resp = _upload(client, pid)
    assert resp.status_code == 201
    body = resp.json()
    assert body["redactions"] == 2 and body["chunk_count"] >= 1

    chunks = client.get(f"/sources/{body['id']}/chunks").json()
    all_text = " ".join(c["text"] for c in chunks)
    assert "sponsor.desk@example.com" not in all_text
    assert "sk-ABCDEFGHIJKLMNOPQRSTUV" not in all_text

    cite = client.get(f"/chunks/{chunks[0]['id']}").json()["citation"]
    assert cite["filename"] == "notes.md"
    assert cite["label"].startswith("notes.md, line")


def test_rejects_bad_uploads(client):
    pid = _project(client)
    assert _upload(client, pid, name="evil.exe").status_code == 415
    assert _upload(client, pid, content="   \n").status_code == 422
    assert _upload(client, pid, level="everyone").status_code == 422
    assert _upload(client, 999).status_code == 404


def test_missing_things_return_404(client):
    assert client.get("/projects/1").status_code == 404
    assert client.get("/chunks/1").status_code == 404
    assert client.get("/sources/1/chunks").status_code == 404


def test_blank_project_name_is_rejected(client):
    assert client.post("/projects", json={"name": "   "}).status_code == 422
