import time
import uuid
import click
from .client import get_client
from .output import print_table, print_success, print_error


@click.group("banners")
def banners():
    """Manage banners."""
    pass


@banners.command("get")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--simple", "simple_output", is_flag=True, help="Simple output (no table)")
def banners_get(json_output, simple_output):
    """Get banners."""
    with get_client() as client:
        response = client.get("/api/v1/configs/banners")
        response.raise_for_status()
        data = response.json()
    if not data:
        if json_output:
            print_json([])
        else:
            click.echo("No banners")
        return
    if json_output:
        print_json(data)
    elif simple_output:
        for banner in data:
            click.echo(f"[{banner.get('type')}] {banner.get('title')}: {banner.get('content')}")
    else:
        rows = [{"type": b.get("type", "?"), "title": b.get("title", "?"), "content": b.get("content", "?")} for b in data]
        print_table(
            rows,
            [("TYPE", "type", 10), ("TITLE", "title", 20), ("CONTENT", "content", 50)],
            json_output=False,
            simple_output=False,
        )


@banners.command("clear")
def banners_clear():
    """Delete all banners."""
    with get_client() as client:
        response = client.post(
            "/api/v1/configs/banners",
            json={"banners": []},
        )
        response.raise_for_status()
    print_success("All banners deleted successfully")


@banners.command("set")
@click.option("--type", required=True, type=click.Choice(["Info", "Warning", "Error", "Success"]), help="Banner type")
@click.option("--title", help="Banner title")
@click.option("--content", required=True, help="Banner content")
@click.option("--dismissible", is_flag=True, default=True, help="Banner is dismissible")
def banners_set(type, title, content, dismissible):
    """Set banners."""
    with get_client() as client:
        response = client.post(
            "/api/v1/configs/banners",
            json={"banners": [{"id": str(uuid.uuid4()), "type": type, "title": title, "content": content, "dismissible": dismissible, "timestamp": int(time.time())}]},
        )
        response.raise_for_status()
    print_success("Banner set successfully")
