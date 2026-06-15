import click
from .client import get_client
from .output import print_table, print_json


@click.group("images")
def images():
    """Manage images."""
    pass


@images.command("list")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--simple", "simple_output", is_flag=True, help="Simple output (no table)")
def images_list(json_output, simple_output):
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
    if not models:
        if json_output:
            print_json([])
        else:
            click.echo("(none)")
        return
    rows = []
    for model in models:
        if isinstance(model, dict):
            rows.append({"id": model.get("id", model)})
        else:
            rows.append({"id": str(model)})
    print_table(
        rows,
        [("ID", "id", 30)],
        json_output=json_output,
        simple_output=simple_output,
    )
