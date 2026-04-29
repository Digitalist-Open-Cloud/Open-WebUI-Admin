import json
import click
from .client import get_client


@click.group("config")
def config():
    """Manage config."""
    pass


@config.command("get")
@click.option("--name", type=click.Choice(["openai", "ollama"]), help="Config name (openai, ollama)")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def config_get(name, json_output):
    """Get current config."""
    with get_client() as client:
        if name == "openai":
            response = client.get("/openai/config")
            response.raise_for_status()
            data = response.json()

            if json_output:
                click.echo(json.dumps(data, indent=2))
            else:
                urls = data.get("OPENAI_API_BASE_URLS", [])
                keys = data.get("OPENAI_API_KEYS", [])

                click.echo("=== OpenAI Connections ===")
                for i, url in enumerate(urls):
                    key_display = keys[i] if i < len(keys) and keys[i] else "(none)"
                    click.echo(f"[{i}] {url}")
                    click.echo(f"    Key: {key_display}")

                click.echo("\n=== Ollama Connections ===")
                ollama_response = client.get("/ollama/config")
                if ollama_response.status_code == 200:
                    ollama_config = ollama_response.json()
                    ollama_urls = ollama_config.get("OLLAMA_BASE_URLS", [])
                    for i, url in enumerate(ollama_urls):
                        click.echo(f"[{i}] {url}")
                else:
                    click.echo("  (none)")
        elif name == "ollama":
            response = client.get("/ollama/config")
            response.raise_for_status()
            data = response.json()

            if json_output:
                click.echo(json.dumps(data, indent=2))
            else:
                click.echo("=== Ollama Config ===")
                click.echo(json.dumps(data, indent=2))
@config.command("export")
def config_export():
    """Export all config in json"""
    with get_client() as client:
        response = client.get("/api/v1/configs/export")
        response.raise_for_status()
        data = response.json()
        click.echo(json.dumps(data, indent=2))
