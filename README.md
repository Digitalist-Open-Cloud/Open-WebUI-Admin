# Open WebUI Admin

CLI tool for managing Open WebUI instances.

## Installation

```bash
pip install open-webui-admin
```

## Configuration

Set environment variables:
- `OPENWEBUI_URL` - Base URL of Open WebUI instance
- `OPENWEBUI_TOKEN` - Authentication token

## Commands

### models

List all available models:
```bash
open-webui-admin models list
```

Check if a model is valid:
```bash
open-webui-admin models check --name gpt-4o
```

Verify a model is working:
```bash
open-webui-admin models verify --name gpt-4o
```

Verify all available models:
```bash
open-webui-admin models verify --all
```

Get models config:
```bash
open-webui-admin models config
```

### config

Get config:
```bash
open-webui-admin config get
```

### connections

Verify connections:
```bash
open-webui-admin connections verify
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

Get banners:
```bash
open-webui-admin banners get
```

Set banner:
```bash
open-webui-admin banners set --type Warning --title "Test" --content "Message"
```

Clear all banners:
```bash
open-webui-admin banners clear
```

Options for `--type`: `Info`, `Warning`, `Error`, `Success`

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
