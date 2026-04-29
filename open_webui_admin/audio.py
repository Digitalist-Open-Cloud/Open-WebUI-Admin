import click
from .client import get_client


@click.group("audio")
def audio():
    """Manage audio."""
    pass


@audio.command("models")
def audio_models():
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
        for model in models:
            if isinstance(model, dict):
                click.echo(model.get("id", model))
            else:
                click.echo(model)


@audio.command("voices")
def audio_voices():
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
        for voice in voices:
            if isinstance(voice, dict):
                click.echo(voice.get("id", voice))
            else:
                click.echo(voice)
