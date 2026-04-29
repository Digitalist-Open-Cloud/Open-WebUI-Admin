import click
from .client import get_client


@click.group("images")
def images():
    """Manage images."""
    pass


@images.command("list")
def images_list():
    """List available image models."""
    with get_client() as client:
        response = client.get("/api/v1/images/models")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            models = data.get("data", data.get("models", []))
        elif isinstance(data, list):
            models = data
        else:
            models = [data]
        for model in models:
            if isinstance(model, dict):
                click.echo(model.get("id", model))
            else:
                click.echo(model)
