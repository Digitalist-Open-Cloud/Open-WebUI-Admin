import time
import uuid
import click
from .client import get_client


@click.group("banners")
def banners():
    """Manage banners."""
    pass


@banners.command("get")
def banners_get():
    """Get banners."""
    with get_client() as client:
        response = client.get("/api/v1/configs/banners")
        response.raise_for_status()
        data = response.json()
        if not data:
            click.echo("No banners")
        else:
            for banner in data:
                click.echo(f"[{banner.get('type')}] {banner.get('title')}: {banner.get('content')}")


@banners.command("clear")
def banners_clear():
    """Delete all banners."""
    with get_client() as client:
        response = client.post(
            "/api/v1/configs/banners",
            json={"banners": []},
        )
        response.raise_for_status()
        click.echo("All banners deleted successfully")


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
        click.echo("Banner set successfully")
