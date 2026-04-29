import os
import httpx
import click

OPENWEBUI_URL = os.environ.get("OPENWEBUI_URL", "")
TOKEN = os.environ.get("OPENWEBUI_TOKEN", "")


def get_client() -> httpx.Client:
    if not OPENWEBUI_URL or not TOKEN:
        raise click.ClickException("OPENWEBUI_URL and OPENWEBUI_TOKEN must be set")
    return httpx.Client(
        base_url=OPENWEBUI_URL,
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=60.0,
    )
