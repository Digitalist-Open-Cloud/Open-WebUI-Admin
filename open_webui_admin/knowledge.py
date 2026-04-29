import os
import click
from .client import get_client
from .output import print_table, print_kv, print_success, print_error, die


@click.group("knowledge")
def knowledge():
    """Manage knowledge bases."""
    pass


@knowledge.command("list")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--simple", "simple_output", is_flag=True, help="Simple output (no table)")
def knowledge_list(json_output, simple_output):
    """List all knowledge bases."""
    with get_client() as client:
        response = client.get("/api/v1/knowledge/")
        response.raise_for_status()
        data = response.json()
    kbs = data if isinstance(data, list) else data.get("items", [])
    if not kbs:
        click.echo("(none)" if not json_output else json.dumps([]))
        return
    rows = [{"id": kb.get("id", "?"), "name": kb.get("name", "?")} for kb in kbs]
    print_table(
        rows,
        [("ID", "id", 36), ("NAME", "name", 30)],
        json_output=json_output,
        simple_output=simple_output,
    )


@knowledge.command("show")
@click.argument("id")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def knowledge_show(id, json_output):
    """Show details of a knowledge base."""
    with get_client() as client:
        response = client.get(f"/api/v1/knowledge/{id}")
        if response.status_code == 404:
            print_error(f"Knowledge base '{id}' not found")
            raise SystemExit(1)
        response.raise_for_status()
        kb = response.json()
    if json_output:
        print_json(kb)
        return
    grants = kb.get("access_grants") or []
    print_kv([
        ("ID", kb.get("id", "?")),
        ("Name", kb.get("name", "?")),
        ("Description", kb.get("description", "(none)")),
        ("Grants", str(len(grants))),
    ])


@knowledge.command("files")
@click.argument("id")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--simple", "simple_output", is_flag=True, help="Simple output (no table)")
def knowledge_files(id, json_output, simple_output):
    """List files in a knowledge base."""
    with get_client() as client:
        response = client.get(f"/api/v1/knowledge/{id}/files")
        if response.status_code == 404:
            print_error(f"Knowledge base '{id}' not found")
            raise SystemExit(1)
        response.raise_for_status()
        data = response.json()
    items = data.get("items", [])
    if not items:
        click.echo("(none)" if not json_output else json.dumps([]))
        return
    rows = [{"id": f.get("id", "?"), "name": (f.get("meta") or {}).get("name") or f.get("filename", "?")} for f in items]
    print_table(
        rows,
        [("FILE_ID", "id", 36), ("NAME", "name", 30)],
        json_output=json_output,
        simple_output=simple_output,
    )


@knowledge.command("create")
@click.option("--name", required=True, help="Knowledge base name")
@click.option("--description", default="", help="Knowledge base description")
def knowledge_create(name, description):
    """Create a new knowledge base."""
    with get_client() as client:
        response = client.post("/api/v1/knowledge/create", json={"name": name, "description": description})
        response.raise_for_status()
        data = response.json()
    print_success(f"Created: {data.get('id')}")


@knowledge.command("delete")
@click.argument("id")
def knowledge_delete(id):
    """Delete a knowledge base."""
    with get_client() as client:
        response = client.delete(f"/api/v1/knowledge/{id}/delete")
        response.raise_for_status()
    print_success(f"Deleted: {id}")


@knowledge.command("add-file")
@click.argument("id")
@click.argument("file_id")
def knowledge_add_file(id, file_id):
    """Add a file to a knowledge base."""
    with get_client() as client:
        response = client.post(f"/api/v1/knowledge/{id}/file/add", json={"file_id": file_id})
        response.raise_for_status()
    print_success(f"Added {file_id} to {id}")


@knowledge.command("remove-file")
@click.argument("id")
@click.argument("file_id")
def knowledge_remove_file(id, file_id):
    """Remove a file from a knowledge base (destroys the file)."""
    with get_client() as client:
        response = client.post(f"/api/v1/knowledge/{id}/file/remove", json={"file_id": file_id})
        response.raise_for_status()
    print_success(f"Removed {file_id} from {id} (file destroyed)")


@knowledge.command("add-folder")
@click.argument("id")
@click.argument("folder")
@click.option("--recursive", "-r", is_flag=True, help="Upload files recursively")
@click.option("--pattern", default="*", help="File pattern to match (e.g., *.pdf)")
def knowledge_add_folder(id, folder, recursive, pattern):
    """Upload all files from a folder to a knowledge base."""
    import mimetypes
    import glob

    if not os.path.isdir(folder):
        print_error(f"'{folder}' is not a valid directory")
        raise SystemExit(1)

    # Verify the knowledge base exists first
    with get_client() as client:
        response = client.get(f"/api/v1/knowledge/{id}")
        if response.status_code == 404:
            print_error(f"Knowledge base '{id}' not found")
            raise SystemExit(1)

    # Get list of files
    if recursive:
        files = glob.glob(os.path.join(folder, "**", pattern), recursive=True)
    else:
        files = glob.glob(os.path.join(folder, pattern))

    # Filter to only files (not directories)
    files = [f for f in files if os.path.isfile(f)]

    if not files:
        click.echo(f"No files found in '{folder}'")
        return

    click.echo(f"Found {len(files)} file(s) to upload...")

    uploaded = []
    failed = []

    with get_client() as client:
        for filepath in sorted(files):
            filename = os.path.basename(filepath)
            click.echo(f"  Uploading {filename}...", nl=False)

            try:
                mime_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
                with open(filepath, "rb") as f:
                    data = f.read()

                response = client.post("/api/v1/files/", files={"file": (filename, data, mime_type)})
                response.raise_for_status()
                file_id = response.json().get("id")

                client.post(f"/api/v1/knowledge/{id}/file/add", json={"file_id": file_id})

                click.echo(" done")
                uploaded.append((filename, file_id))

            except Exception as e:
                click.echo(f" failed: {e}")
                failed.append((filename, str(e)))

    click.echo(f"\nSummary: {len(uploaded)} uploaded, {len(failed)} failed")

    if uploaded:
        click.echo("\nUploaded files:")
        for filename, file_id in uploaded:
            click.echo(f"  {filename} -> {file_id}")

    if failed:
        click.echo("\nFailed files:")
        for filename, error in failed:
            click.echo(f"  {filename}: {error}")
