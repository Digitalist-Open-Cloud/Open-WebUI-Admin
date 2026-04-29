import click
import mimetypes
from .client import get_client
from .output import print_table, print_kv, print_success, die


@click.group("files")
def files():
    """Manage files."""
    pass


@files.command("list")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--simple", "simple_output", is_flag=True, help="Simple output (no table)")
def files_list(json_output, simple_output):
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
        click.echo("(none)" if not json_output else json.dumps([]))
        return
    rows = []
    for f in files:
        name = (f.get("meta") or {}).get("name") or f.get("filename", "?")
        size = (f.get("meta") or {}).get("size", "?")
        rows.append({"id": f.get("id", "?"), "name": name, "size": size})
    print_table(
        rows,
        [("ID", "id", 36), ("NAME", "name", 30), ("SIZE", "size", 10)],
        json_output=json_output,
        simple_output=simple_output,
    )


@files.command("show")
@click.argument("id")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def files_show(id, json_output):
    """Show file details."""
    with get_client() as client:
        response = client.get(f"/api/v1/files/{id}")
        if response.status_code == 404:
            die(f"File '{id}' not found")
        response.raise_for_status()
        f = response.json()
    if isinstance(f, list):
        f = f[0] if f else {}
    meta = f.get("meta") or {}
    if json_output:
        print_json(f)
        return
    print_kv([
        ("ID", f.get("id", "?")),
        ("Name", meta.get("name") or f.get("filename", "?")),
        ("Size", f"{meta.get('size', '?')} bytes"),
        ("Type", meta.get("content_type", "?")),
    ])


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
    print_success(f"Uploaded: {filename} -> {data.get('id')}")


@files.command("delete")
@click.argument("id")
def files_delete(id):
    """Delete a file."""
    with get_client() as client:
        response = client.delete(f"/api/v1/files/{id}")
        response.raise_for_status()
    print_success(f"Deleted: {id}")
