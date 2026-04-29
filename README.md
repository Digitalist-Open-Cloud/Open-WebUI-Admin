# Open WebUI Admin

CLI tool for managing Open WebUI instances.

Very much a work in progress, and everyone is welcome to contribute.

Idea around this module is to use the existing API to simplify common tasks, checks etc.
So you need to able to use the API and have an API key.

## Commands Overview

| Command | Description |
|---------|------------|
| `models list` | List all available models (standard + custom) |
| `models list -v` | List models with provider/connection info |
| `models custom list` | List custom/preset models with base_model_id |
| `models custom list --name <model>` | Show full JSON for a specific custom model |
| `models check --name <model>` | Check if model is valid |
| `models check --name <model> -v` | Check with provider/URL info |
| `models verify --name <model>` | Verify single model works |
| `models verify --all` | Verify all models |
| `models verify --all -v` | Verify all with provider/URL info |
| `models verify --debug` | Verify with debug output |
| `models custom verify --all` | Verify all custom models |
| `models custom verify --name <model>` | Verify a specific custom model |
| `models custom verify -v` | Verify custom with provider info |
| `models custom verify --debug` | Verify custom with debug output |
| `models config` | Get models configuration |
| `connections verify` | Verify external connections |
| `config get --name openai\|ollama` | Get OpenAI or Ollama configuration |
| `config get --json` | Output config as JSON |
| `config export` | Export all configuration |
| `users get --all` | List all users |
| `users get --all --json` | List all users in JSON format |
| `users get --include-email <regex>` | Include users matching email pattern |
| `users get --exclude-email <regex>` | Exclude users matching email pattern |
| `images list` | List image models |
| `audio models` | List audio models |
| `audio voices` | List available voices |
| `banners get` | Get banners |
| `banners set --type <type> --content <text>` | Set a banner |
| `banners set --dismissible` | Set a dismissible banner |
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
open-webui-admin models custom list
# Output: model_id (base: base_model_id)
# Example: dada (base: gpt-4o)
```

Show full details for a specific custom model:

```bash
open-webui-admin models custom list --name dada
# Output: Full JSON for the model
```

Check if a model is valid:

```bash
open-webui-admin models check --name gpt-4o
```

Check with provider/URL info:

```bash
open-webui-admin models check --name gpt-4o -v
```

Get models configuration:

```bash
open-webui-admin models config
# Output: Full JSON models configuration
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

Verify all with provider/URL info:

```bash
open-webui-admin models verify --all -v
# Output:
# [OK] gpt-5 | https://api.openai.com/v1
# [FAIL] anthropic.claude-opus-4-6 | https://api.anthropic.com/v1 | authentication_error
```

Verify all custom models:

```bash
open-webui-admin models custom verify --all
# Output:
# Verifying 10 custom models...
# [OK] dada
# [FAIL] test-model | error_message
# ...
# 10 custom models verified
```

Verify custom with provider info:

```bash
open-webui-admin models custom verify --all -v
```

Verify custom with debug output:

```bash
open-webui-admin models custom verify --name dada --debug
```

Verify a specific custom model:

```bash
open-webui-admin models custom verify --name dada
# Output: Model 'dada' is working
```

### connections

Verify external connections (OpenAI, Ollama):

```bash
open-webui-admin connections verify
```

### config

Get OpenAI configuration:

```bash
open-webui-admin config get --name openai
```

Get OpenAI configuration as JSON:

```bash
open-webui-admin config get --name openai --json
```

Get Ollama configuration:

```bash
open-webui-admin config get --name ollama
```

Get Ollama configuration as JSON:

```bash
open-webui-admin config get --name ollama --json
```

Export all configuration:

```bash
open-webui-admin config export
# Output: Full JSON configuration
```

### users

Get all users:

```bash
open-webui-admin users get --all
# Output: user_id | name | email | role
```

Get all users in JSON format:

```bash
open-webui-admin users get --all --json
```

Include users matching email pattern (can be used multiple times):

```bash
open-webui-admin users get --all --include-email "@example.com"
open-webui-admin users get --all --include-email "@admin.com" --include-email "@test.com"
```

Exclude users matching email pattern (can be used multiple times):

```bash
open-webui-admin users get --all --exclude-email "@spam.com"
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

Set a banner (required: --type, --content):

```bash
open-webui-admin banners set --type Warning --title "System Update" --content "Maintenance scheduled"
```

Set a non-dismissible banner:

```bash
open-webui-admin banners set --type Warning --title "Alert" --content "Critical update" --dismissible
```

Clear all banners:

```bash
open-webui-admin banners clear
```

Options for `--type`: `Info`, `Warning`, `Error`, `Success`

Options for `--dismissible`: Flag (default: True)

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

### models custom list
```
model_id (base: base_model_id)
model_id (no base model)
```

### users get --all
```
user_id | name | email | role
```

## Error Messages

- `authentication_error` - Invalid API key
- `not_found` - Model not found (404)
- `not_chat_model` - Model doesn't support chat completions endpoint
- `server_error` - Upstream provider error (500)
- `timeout` - Request timed out

## Project Structure

```
open_webui_admin/
├── cli.py          # Main entry point, registers command groups
├── client.py       # HTTP client factory (get_client)
├── models.py       # Models commands (list, custom, check, verify)
├── banners.py      # Banners commands (get, clear, set)
├── images.py       # Images commands (list)
├── audio.py        # Audio commands (models, voices)
├── config.py       # Config commands (get, export)
├── connections.py  # Connections commands (verify)
└── users.py       # Users commands (get)
```

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
