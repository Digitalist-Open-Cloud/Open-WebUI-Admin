import json
import os
import click
import httpx

from . import __version__

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


def verify_model(client, model, debug=False):
    endpoint = "/openai/chat/completions"
    payload = {"model": model, "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 5}
    try:
        response = client.post(endpoint, json=payload, timeout=60.0)
        if response.status_code == 200:
            try:
                content = response.text
                if content.startswith("data:"):
                    if debug:
                        click.echo(f"DEBUG: {endpoint} returned streaming: {content[:500]}")
                    has_error = '"error"' in content or '"error":' in content or 'Error:' in content
                    has_content = False
                    for line in content.split("\n"):
                        if line.startswith("data:") and '"content"' in line:
                            has_content = True
                            break
                    if has_error:
                        msg = "API Error"
                        for line in content.split("\n"):
                            if line.startswith("data:") and "content" in line:
                                import re
                                match = re.search(r'"content":\s*"([^"]*(?:\\.[^"]*)*)"', line)
                                if match:
                                    raw_msg = match.group(1).replace('\\"', '"').replace('\\n', '\n')
                                    if "invalid x-api-key" in raw_msg:
                                        msg = "invalid x-api-key"
                                    elif "401" in raw_msg:
                                        msg = "authentication_error"
                                    else:
                                        msgs = re.findall(r'"message":"([^"]+)"', raw_msg)
                                        msg = msgs[0] if msgs else raw_msg[:100]
                        return None, f"FAIL:{msg}"
                    return endpoint, "chat"
                result = json.loads(content)
                if debug:
                    click.echo(f"DEBUG: {endpoint} returned: {content[:500]}")
                if result.get("error"):
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    return None, f"FAIL:{error_msg[:150]}"
                chat_content = result.get("choices", [])
                message = result.get("message", {})
                if chat_content or message:
                    return endpoint, "chat"
            except json.JSONDecodeError:
                return None, "FAIL:Invalid response"
        else:
            error_text = response.text[:200]
            if debug:
                click.echo(f"DEBUG: {endpoint} returned {response.status_code}: {error_text}")
            try:
                error_data = json.loads(response.text)
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
            except json.JSONDecodeError:
                error_msg = error_text
            return None, f"FAIL:{error_msg[:150]}"
    except httpx.ReadTimeout:
        return None, "FAIL:Timeout"
    except (httpx.HTTPStatusError, httpx.ConnectError) as e:
        return None, f"FAIL:{str(e)[:100]}"
    return None, "FAIL"


@click.group()
@click.version_option(version=__version__)
def cli():
    """Open WebUI validation tool."""
    pass


@cli.group("models")
def models():
    """Manage models."""
    pass


@models.command("list")
def models_list():
    """List all available models."""
    with get_client() as client:
        response = client.get("/openai/models")
        response.raise_for_status()
        data = response.json()
        for m in sorted([model.get("id", "") for model in data.get("data", [])]):
            click.echo(m)


@models.command("custom")
def models_custom():
    """List custom models."""
    with get_client() as client:
        response = client.get("/api/v1/models")
        response.raise_for_status()
        data = response.json()
        custom_models = [m.get("id", "") for m in data.get("data", []) if m.get("preset")]
        if custom_models:
            for m in sorted(custom_models):
                click.echo(m)
        else:
            click.echo("No custom models")


@models.command("check")
@click.option("--name", required=True, help="Model name to check")
def models_check(name):
    """Check if a model is valid."""
    with get_client() as client:
        response = client.get("/openai/models")
        response.raise_for_status()
        data = response.json()
        available_models = {m.get("id", "").replace(":latest", "") for m in data.get("data", [])}
        name = name.replace(":latest", "")
        if name in available_models:
            click.echo(f"Model '{name}' is valid")
        else:
            click.echo(f"Model '{name}' is NOT valid")
            raise SystemExit(1)


@models.command("verify")
@click.option("--name", help="Model name to verify")
@click.option("--all", is_flag=True, help="Verify all available models")
@click.option("--debug", is_flag=True, help="Debug output")
def models_verify(name, all, debug):
    """Verify a model works by sending a test request."""
    with get_client() as client:
        if all:
            models_response = client.get("/openai/models")
            models_response.raise_for_status()
            models_data = models_response.json()
            available_models = [m.get("id", "") for m in models_data.get("data", [])]
            custom_response = client.get("/api/v1/models")
            if custom_response.status_code == 200:
                custom_data = custom_response.json()
                custom_models = [m.get("id", "") for m in custom_data.get("data", []) if m.get("preset")]
                available_models.extend(custom_models)
            count = len(available_models)
            click.echo(f"Verifying {count} models...\n")
            results = {}
            for model in available_models:
                try:
                    endpoint, status = verify_model(client, model, debug)
                    if status == "chat":
                        click.echo(f"[OK:{endpoint}] {model}")
                        results[model] = endpoint
                    elif status.startswith("FAIL:"):
                        failed_msg = status[5:]
                        click.echo(f"[FAIL:{failed_msg}] {model}")
                        results[model] = failed_msg
                except httpx.HTTPStatusError as e:
                    click.echo(f"[FAIL-{e.response.status_code}] {model}")
                    results[model] = f"FAIL-{e.response.status_code}"
                except httpx.ConnectError:
                    click.echo(f"[ERROR] {model}")
                    results[model] = "ERROR"
            click.echo(f"\n{count} models verified")
        elif name:
            endpoint, status = verify_model(client, name, debug)
            if status == "chat":
                if debug:
                    click.echo(f"DEBUG: Model is working via {endpoint}")
                click.echo(f"Model '{name}' is working via {endpoint}")
            elif status.startswith("FAIL:"):
                click.echo(f"Model '{name}' is NOT working: {status[5:]}")
        else:
            click.echo("Use --name <model> or --all")


@models.command("config")
def models_config():
    """Get models config."""
    with get_client() as client:
        response = client.get("/api/v1/configs/models")
        response.raise_for_status()
        click.echo(response.json())


@cli.group("banners")
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


@cli.group("images")
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


@cli.group("audio")
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


@banners.command("set")
@click.option("--type", required=True, type=click.Choice(["Info", "Warning", "Error", "Success"]), help="Banner type")
@click.option("--title", help="Banner title")
@click.option("--content", required=True, help="Banner content")
@click.option("--dismissible", is_flag=True, default=True, help="Banner is dismissible")
def banners_set(type, title, content, dismissible):
    """Set banners."""
    import time
    import uuid
    with get_client() as client:
        response = client.post(
            "/api/v1/configs/banners",
            json={"banners": [{"id": str(uuid.uuid4()), "type": type, "title": title, "content": content, "dismissible": dismissible, "timestamp": int(time.time())}]},
        )
        response.raise_for_status()
        click.echo("Banner set successfully")


@cli.group("config")
def config():
    """Manage config."""
    pass


@config.command("get")
def config_get():
    """Get current config."""
    with get_client() as client:
        response = client.get("/openai/config")
        response.raise_for_status()
        click.echo(response.json())


@cli.group("connections")
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


if __name__ == "__main__":
    cli()