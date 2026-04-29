import click
import mimetypes
from .client import get_client


@click.group("files")
def files():
    """Manage files."""
    pass


@files.command("list")
def files_list():
    """List all files."""
    with get_client() as client:
        response = client.get("/api/v1/files/")
        response.raise_for_status()
        data = response.json()
    # Handle different response formats
    if isinstance(data, dict):
        files = data.get("items", data.get("data", []))
    elif isinstance(data, list):
        files = data
    else:
        files = []
    if not files:
        click.echo("No files")
        return
    for f in files:
        name = (f.get("meta") or {}).get("name") or f.get("filename", "?")
        size = (f.get("meta") or {}).get("size", "?")
        click.echo(f"{f.get('id', '?')}  {name}  ({size} bytes)")


@files.command("show")
@click.argument("id")
def files_show(id):
    """Show file details."""
    with get_client() as client:
        response = client.get(f"/api/v1/files/{id}")
        if response.status_code == 404:
            click.echo(f"File '{id}' not found")
            raise SystemExit(1)
        response.raise_for_status()
        f = response.json()
    # Handle both dict and list responses
    if isinstance(f, list):
        f = f[0] if f else {}
    meta = f.get("meta") or {}
    click.echo(f"ID: {f.get('id', '?')}")
    click.echo(f"Name: {meta.get('name') or f.get('filename', '?')}")
    click.echo(f"Size: {meta.get('size', '?')} bytes")
    click.echo(f"Type: {meta.get('content_type', '?')}")


@files.command("upload")
@click.argument("path")
@click.option("--mime-type", default="", help="MIME type (auto-detected if not provided)")
def files_upload(path, mime_type):
    """Upload a file."""
    if not mime_type:
        mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    filename = path.rsplit("/", 1)[-1]
    with open(path, "rb") as f:
        data = f.read()
    with get_client() as client:
        response = client.post("/api/v1/files/", files={"file": (filename, data, mime_type)})
        response.raise_for_status()
        data = response.json()
    click.echo(f"Uploaded: {filename} -> {data.get('id')}")


@files.command("delete")
@click.argument("id")
def files_delete(id):
    """Delete a file."""
    with get_client() as client:
        response = client.delete(f"/api/v1/files/{id}")
        response.raise_for_status()
    click.echo(f"Deleted: {id}")
