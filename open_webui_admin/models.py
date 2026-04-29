import json
import click
import httpx
from .client import get_client


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
                    error_obj = result.get("error")
                    if isinstance(error_obj, dict):
                        error_msg = error_obj.get("message", "Unknown error")
                    elif error_obj:
                        error_msg = str(error_obj)
                    else:
                        error_msg = "Unknown error"
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
                if isinstance(error_data, dict):
                    error_obj = error_data.get("error")
                    if isinstance(error_obj, dict):
                        error_msg = error_obj.get("message", error_data.get("message", error_text))
                    elif error_obj:
                        error_msg = str(error_obj)
                    else:
                        error_msg = error_data.get("message", error_text)
                else:
                    error_msg = str(error_data)[:150]
            except (json.JSONDecodeError, ValueError):
                error_msg = error_text
            return None, f"FAIL:{error_msg[:150]}"
    except httpx.ReadTimeout:
        return None, "FAIL:Timeout"
    except (httpx.HTTPStatusError, httpx.ConnectError) as e:
        return None, f"FAIL:{str(e)[:100]}"
    return None, "FAIL"


def get_provider(model_id, url_display):
    if model_id.startswith("anthropic."):
        return "anthropic"
    if model_id.startswith("claude-"):
        return "anthropic"
    if model_id.startswith("replicate_") or model_id.startswith("replicate-"):
        return "replicate"
    if model_id.startswith("recraft") or model_id.startswith("ideogram"):
        return "recraft"
    if model_id.startswith("flux") or model_id.startswith("nano-banana") or model_id.startswith("seedream"):
        return "replicate"
    if model_id.startswith("llama") or model_id.startswith("mistral"):
        return "ollama"
    if model_id.startswith("gemini"):
        return "google"
    if model_id.startswith("deepseek"):
        return "deepseek"
    if "open-webui-pipelines" in url_display:
        return "pipeline"
    if "api.openai.com" in url_display:
        return "openai"
    if "anthropic" in url_display:
        return "anthropic"
    if "replicate" in url_display:
        return "replicate"
    if "ollama" in url_display:
        return "ollama"
    if "_" in model_id:
        return model_id.split("_")[0]
    return ""


@click.group("models")
def models():
    """Manage models."""
    pass


@models.command("list")
@click.option("--verbose", "-v", is_flag=True, help="Show provider info")
def models_list(verbose):
    """List all available models."""
    with get_client() as client:
        response = client.get("/openai/models")
        response.raise_for_status()
        data = response.json()

        custom_response = client.get("/api/v1/models")
        custom_data = custom_response.json() if custom_response.status_code == 200 else {"data": []}
        custom_models = [m for m in custom_data.get("data", []) if m.get("preset")]

        all_models = data.get("data", []) + custom_models

        if verbose:
            config_response = client.get("/openai/config")
            if config_response.status_code == 200:
                config = config_response.json()
                urls = config.get("OPENAI_API_BASE_URLS", [])
            else:
                urls = []
            for model in sorted(all_models, key=lambda m: m.get("id", "")):
                model_id = model.get("id", "")
                owned_by = model.get("owned_by", "")
                connection_type = model.get("connection_type", "")
                url_idx = model.get("urlIdx", "")
                url_idx_val = int(url_idx) if url_idx else 0
                url_display = urls[url_idx_val] if url_idx_val < len(urls) else ""
                provider = get_provider(model_id, url_display)
                click.echo(f"{model_id} | {provider} | {connection_type} | {url_idx} | {url_display}")
        else:
            for m in sorted([model.get("id", "") for model in all_models]):
                click.echo(m)


@models.group("custom")
def custom():
    """Manage custom models."""
    pass


@custom.command("list")
@click.option("--name", help="Show details for a specific custom model")
def custom_list(name):
    """List custom models."""
    with get_client() as client:
        response = client.get("/api/v1/models/list")
        response.raise_for_status()
        data = response.json()
        custom_models = data.get("items", [])
        if name:
            model = next((m for m in custom_models if m.get("id") == name), None)
            if model:
                click.echo(json.dumps(model, indent=2))
            else:
                click.echo(f"Model '{name}' not found")
                raise SystemExit(1)
        elif custom_models:
            for m in sorted(custom_models, key=lambda x: x.get("id", "")):
                model_id = m.get("id", "")
                base_model_id = m.get("base_model_id", "")
                if base_model_id:
                    click.echo(f"{model_id} (base: {base_model_id})")
                else:
                    click.echo(model_id)
        else:
            click.echo("No custom models")


@custom.command("verify")
@click.option("--name", help="Custom model name to verify")
@click.option("--all", "all_models", is_flag=True, help="Verify all custom models")
@click.option("--verbose", "-v", is_flag=True, help="Show provider info")
@click.option("--debug", is_flag=True, help="Debug output")
def custom_verify(name, all_models, verbose, debug):
    """Verify custom models work by sending test requests."""
    with get_client() as client:
        response = client.get("/api/v1/models/list")
        response.raise_for_status()
        data = response.json()
        custom_models = [m.get("id", "") for m in data.get("items", [])]

        if all_models:
            count = len(custom_models)
            click.echo(f"Verifying {count} custom models...\n")
            results = {}
            for model in custom_models:
                try:
                    endpoint, status = verify_model(client, model, debug)
                    if status == "chat":
                        if verbose:
                            click.echo(f"[OK] {model}")
                        else:
                            click.echo(f"[OK] {model}")
                        results[model] = endpoint
                    elif status.startswith("FAIL:"):
                        failed_msg = status[5:]
                        click.echo(f"[FAIL] {model} | {failed_msg}")
                        results[model] = failed_msg
                except httpx.HTTPStatusError as e:
                    click.echo(f"[ERROR] {model} | {e.response.status_code}")
                    results[model] = f"ERROR-{e.response.status_code}"
                except httpx.ConnectError:
                    click.echo(f"[ERROR] {model} | connection")
                    results[model] = "ERROR"
            click.echo(f"\n{count} custom models verified")
        elif name:
            endpoint, status = verify_model(client, name, debug)
            if status == "chat":
                click.echo(f"Model '{name}' is working")
            elif status.startswith("FAIL:"):
                click.echo(f"Model '{name}' is NOT working: {status[5:]}")
        else:
            click.echo("Use --name <model> or --all")


@models.command("check")
@click.option("--name", required=True, help="Model name to check")
@click.option("--verbose", "-v", is_flag=True, help="Show provider info")
def models_check(name, verbose):
    """Check if a model is valid."""
    with get_client() as client:
        response = client.get("/openai/models")
        response.raise_for_status()
        data = response.json()
        available_models = {m.get("id", ""): m for m in data.get("data", [])}

        custom_response = client.get("/api/v1/models")
        if custom_response.status_code == 200:
            custom_data = custom_response.json()
            for m in custom_data.get("data", []):
                if m.get("preset"):
                    available_models[m.get("id", "")] = m

        name = name.replace(":latest", "")
        if name in available_models:
            model_data = available_models[name]
            click.echo(f"Model '{name}' is valid")
            if verbose:
                url_idx = model_data.get("urlIdx", "")
                config_response = client.get("/openai/config")
                if config_response.status_code == 200:
                    config = config_response.json()
                    urls = config.get("OPENAI_API_BASE_URLS", [])
                else:
                    urls = []
                url_display = urls[int(url_idx)] if url_idx and int(url_idx) < len(urls) else ""
                provider = get_provider(name, url_display)
                click.echo(f"  Provider: {provider}")
                click.echo(f"  URL: {url_display}")
        else:
            click.echo(f"Model '{name}' is NOT valid")
            raise SystemExit(1)


@models.command("verify")
@click.option("--name", help="Model name to verify")
@click.option("--all", "all_models", is_flag=True, help="Verify all available models")
@click.option("--verbose", "-v", is_flag=True, help="Show provider info")
@click.option("--debug", is_flag=True, help="Debug output")
def models_verify(name, all_models, verbose, debug):
    """Verify a model works by sending a test request."""
    with get_client() as client:
        if all_models:
            models_response = client.get("/openai/models")
            models_response.raise_for_status()
            models_data = models_response.json()
            available_models = [m.get("id", "") for m in models_data.get("data", [])]
            custom_response = client.get("/api/v1/models")
            if custom_response.status_code == 200:
                custom_data = custom_response.json()
                custom_models = [m.get("id", "") for m in custom_data.get("data", []) if m.get("preset")]
                available_models.extend(custom_models)

            model_urls = {m.get("id", ""): m.get("urlIdx", "") for m in models_data.get("data", [])}

            if verbose:
                config_response = client.get("/openai/config")
                if config_response.status_code == 200:
                    config = config_response.json()
                    urls = config.get("OPENAI_API_BASE_URLS", [])
                else:
                    urls = []
            else:
                urls = []

            count = len(available_models)
            click.echo(f"Verifying {count} models...\n")
            results = {}
            for model in available_models:
                try:
                    endpoint, status = verify_model(client, model, debug)
                    url_idx = model_urls.get(model, "")
                    try:
                        url_idx_int = int(url_idx) if url_idx else 0
                    except ValueError:
                        url_idx_int = 0
                    url_display = urls[url_idx_int] if url_idx_int < len(urls) else "(default)" if verbose else ""
                    if status == "chat":
                        if verbose:
                            click.echo(f"[OK] {model} | {url_display}")
                        else:
                            click.echo(f"[OK] {model}")
                        results[model] = endpoint
                    elif status.startswith("FAIL:"):
                        failed_msg = status[5:]
                        if verbose:
                            click.echo(f"[FAIL] {model} | {url_display} | {failed_msg}")
                        else:
                            click.echo(f"[FAIL] {model} | {failed_msg}")
                        results[model] = failed_msg
                except httpx.HTTPStatusError as e:
                    click.echo(f"[ERROR] {model} | {e.response.status_code}")
                    results[model] = f"ERROR-{e.response.status_code}"
                except httpx.ConnectError:
                    click.echo(f"[ERROR] {model} | connection")
                    results[model] = "ERROR"
            click.echo(f"\n{count} models verified")
        elif name:
            endpoint, status = verify_model(client, name, debug)
            if status == "chat":
                if verbose:
                    config_response = client.get("/openai/config")
                    if config_response.status_code == 200:
                        config = config_response.json()
                        urls = config.get("OPENAI_API_BASE_URLS", [])
                    else:
                        urls = []
                    model_response = client.get("/openai/models")
                    if model_response.status_code == 200:
                        model_data = model_response.json()
                        url_idx = next((m.get("urlIdx", "") for m in model_data.get("data", []) if m.get("id") == name), "")
                        try:
                            url_idx_int = int(url_idx) if url_idx else 0
                        except ValueError:
                            url_idx_int = 0
                        url_display = urls[url_idx_int] if url_idx_int < len(urls) else "(default)"
                        click.echo(f"Model '{name}' is working | {url_display}")
                    else:
                        click.echo(f"Model '{name}' is working")
                else:
                    click.echo(f"Model '{name}' is working")
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
