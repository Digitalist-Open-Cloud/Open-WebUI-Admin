import click
from .client import get_client
from .output import print_table, print_json


@click.group("audio")
def audio():
    """Manage audio."""
    pass


@audio.command("models")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--simple", "simple_output", is_flag=True, help="Simple output (no table)")
def audio_models(json_output, simple_output):
    """List available audio models."""
    with get_client() as client:
        response = client.get("/api/v1/audio/models")
        response.raise_for_status()
        data = response.json()
    if isinstance(data, dict):
        models = data.get("models", data.get("data", []))
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


@audio.command("voices")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--simple", "simple_output", is_flag=True, help="Simple output (no table)")
def audio_voices(json_output, simple_output):
    """List available voices."""
    with get_client() as client:
        response = client.get("/api/v1/audio/voices")
        response.raise_for_status()
        data = response.json()
    if isinstance(data, dict):
        voices = data.get("voices", data.get("data", []))
    elif isinstance(data, list):
        voices = data
    else:
        voices = [data]
    if not voices:
        if json_output:
            print_json([])
        else:
            click.echo("(none)")
        return
    rows = []
    for voice in voices:
        if isinstance(voice, dict):
            rows.append({"id": voice.get("id", voice)})
        else:
            rows.append({"id": str(voice)})
    print_table(
        rows,
        [("ID", "id", 30)],
        json_output=json_output,
        simple_output=simple_output,
    )
