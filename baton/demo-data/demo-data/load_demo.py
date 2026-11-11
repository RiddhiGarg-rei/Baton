"""Upload every demo file to a running Baton backend, using the access levels in manifest.json.

Usage:
    python load_demo.py --dry-run          # just list what would be uploaded
    python load_demo.py                    # needs the backend running and httpx installed
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    sources = manifest["sources"]

    if args.dry_run:
        for s in sources:
            print(f"would upload {s['path']} as {s['upload_name']} ({s['access_level']})")
        return

    import httpx  # installed with the backend requirements

    with httpx.Client(base_url=args.base_url, timeout=30) as client:
        resp = client.post("/projects", json={"name": manifest["project"]["name"]})
        resp.raise_for_status()
        project_id = resp.json()["id"]
        print(f"Created project {project_id}")
        for s in sources:
            path = HERE / s["path"]
            with path.open("rb") as f:
                resp = client.post(
                    f"/projects/{project_id}/sources",
                    files={"file": (s["upload_name"], f)},
                    data={"access_level": s["access_level"]},
                )
            if resp.status_code != 201:
                print(f"FAILED {s['path']}: {resp.status_code} {resp.text}")
                continue
            body = resp.json()
            print(f"{s['upload_name']}: {body['chunk_count']} chunks, {body['redactions']} redactions")


if __name__ == "__main__":
    main()
