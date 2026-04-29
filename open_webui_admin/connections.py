import click
from .client import get_client


@click.group("connections")
def connections():
    """Manage connections."""
    pass


@connections.command("verify")
def connections_verify():
    """Verify all external connections."""
    with get_client() as client:
        config_response = client.get("/openai/config")
        config_response.raise_for_status()
        openai_config = config_response.json()

        ollama_config_response = client.get("/ollama/config")
        ollama_config_response.raise_for_status()
        ollama_config = ollama_config_response.json()

        click.echo("=== OpenAI Connections ===")
        openai_urls = openai_config.get("OPENAI_API_BASE_URLS", [])
        openai_keys = openai_config.get("OPENAI_API_KEYS", [])
        for i, url in enumerate(openai_urls):
            key = openai_keys[i] if i < len(openai_keys) else ""
            try:
                verify_response = client.post(
                    "/openai/verify",
                    json={"url": url, "key": key},
                )
                if verify_response.status_code == 200:
                    click.echo(f"[OK] {url}")
                else:
                    click.echo(f"[FAIL] {url} - {verify_response.status_code}")
            except Exception as e:
                click.echo(f"[FAIL] {url} - {e}")

        click.echo("=== Ollama Connections ===")
        ollama_enabled = ollama_config.get("ENABLE_OLLAMA_API", True)
        ollama_urls = ollama_config.get("OLLAMA_BASE_URLS", [])
        if not ollama_enabled:
            click.echo("Ollama API is disabled")
        elif not ollama_urls:
            click.echo("No Ollama connections configured")
        else:
            for url in ollama_urls:
                if url == "http://localhost:11434":
                    continue
                try:
                    verify_response = client.post(
                        "/ollama/verify",
                        json={"url": url, "keep_alive": "1m"},
                    )
                    if verify_response.status_code in (200, 201):
                        click.echo(f"[OK] {url}")
                    else:
                        click.echo(f"[FAIL] {url} - {verify_response.status_code}")
                except Exception as e:
                    click.echo(f"[FAIL] {url} - {e}")
