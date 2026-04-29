# Open WebUI Admin

CLI tool for managing Open WebUI instances.

## Commands Overview

| Command | Description |
|---------|------------|
| `models list` | List all available models (standard + custom) |
| `models list -v` | List models with provider/connection info |
| `models custom` | List custom/preset models |
| `models check --name <model>` | Check if model is valid |
| `models verify --name <model>` | Verify single model works |
| `models verify --all` | Verify all models |
| `connections verify` | Verify external connections |
| `config get` | Get configuration |
| `images list` | List image models |
| `audio models` | List audio models |
| `audio voices` | List available voices |
| `banners get` | Get banners |
| `banners set` | Set a banner |
| `banners clear` | Clear all banners |

## Installation

```bash
pip install open-webui-admin
```

Or install from source:

```bash
poetry install
poetry build
pip install dist/open_webui_admin-*.whl
```

## Configuration

Set environment variables:
- `OPENWEBUI_URL` - Base URL of Open WebUI instance (e.g., `https://cloud.open-webui.example.com`)
- `OPENWEBUI_TOKEN` - Authentication token (from Account settings)

## Commands

### models

List all available models (standard + custom):

```bash
open-webui-admin models list
```

List with verbose output (shows provider and connection info):

```bash
open-webui-admin models list -v
# Output: model_id | provider | connection_type | urlIdx | url
# Example: gpt-5 | openai | external | 1 | https://api.openai.com/v1
```

List custom/preset models only:

```bash
open-webui-admin models custom
```

Check if a model is valid:

```bash
open-webui-admin models check --name gpt-4o
```

Verify a single model works:

```bash
open-webui-admin models verify --name gpt-4o
# Output: Model 'gpt-4o' is working
#        Model 'anthropic.claude-opus-4-6' is NOT working: authentication_error
```

Verify with debug output (shows full API response):

```bash
open-webui-admin models verify --name gpt-4o --debug
```

Verify all available models:

```bash
open-webui-admin models verify --all
# Output:
# Verifying 134 models...
# [OK] gpt-5
# [FAIL] anthropic.claude-opus-4-6 | authentication_error
# ...
# 58 models verified
```

Verify all with verbose output (shows provider info):

```bash
open-webui-admin models verify --all -v
```

### connections

Verify external connections (OpenAI, Ollama):

```bash
open-webui-admin connections verify
```

### config

Get full config:

```bash
open-webui-admin config get
```

Get specific config section:

```bash
open-webui-admin config get models
```

### images

List available image models:

```bash
open-webui-admin images list
```

### audio

List available audio models:

```bash
open-webui-admin audio models
```

List available voices:

```bash
open-webui-admin audio voices
```

### banners

Get current banners:

```bash
open-webui-admin banners get
```

Set a banner:

```bash
open-webui-admin banners set --type Warning --title "System Update" --content "Maintenance scheduled"
```

Clear all banners:

```bash
open-webui-admin banners clear
```

Options for `--type`: `Info`, `Warning`, `Error`, `Success`

## Output Formats

### models list -v
```
model_id | provider | connection_type | urlIdx | url
```
- `provider`: Inferred from model name or URL (e.g., `openai`, `anthropic`, `pipeline`, `ollama`)
- `connection_type`: `external` or local
- `urlIdx`: Index into configured API endpoints (see `/openai/config`)
- `url`: The actual API endpoint URL

### models verify --all -v
```
[OK] model_name
[FAIL] model_name | error_message
[ERROR] model_name | status_code
```

### Error Messages
- `authentication_error` - Invalid API key
- `not_found` - Model not found (404)
- `not_chat_model` - Model doesn't support chat completions endpoint
- `server_error` - Upstream provider error (500)
- `timeout` - Request timed out

## Development

Install for development:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov=open_webui_admin --cov-report=term-missing
```

Run CLI directly:

```bash
poetry run open-webui-admin --help
```

Build package:

```bash
poetry build
```