# Development

Information for developers contributing to Open WebUI Admin.

## Project Structure

```
open_webui_admin/
├── cli.py          # Main entry point, registers command groups
├── client.py       # HTTP client factory (get_client)
├── models.py       # Models commands (list, custom, check, verify, config)
├── banners.py      # Banners commands (get, clear, set)
├── images.py       # Images commands (list)
├── audio.py        # Audio commands (models, voices)
├── config.py       # Config commands (get, export)
├── connections.py  # Connections commands (verify)
└── users.py        # Users commands (get)
```

## Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/anomalyco/openwebui-models.git
cd openwebui-models

# Install with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Running Tests

Run all tests:

```bash
poetry run pytest
```

Run specific test file:

```bash
poetry run pytest tests/test_models.py -v
```

Run specific test:

```bash
poetry run pytest tests/test_models.py::TestModelsCustom::test_models_custom -v
```

Run tests with coverage:

```bash
poetry run pytest --cov=open_webui_admin --cov-report=term-missing
```

## Running CLI Directly

```bash
poetry run open-webui-admin --help
```

## Key Patterns

### HTTP Client Usage

All commands use `get_client()` from `client.py`:

```python
from .client import get_client

with get_client() as client:
    response = client.get("/api/v1/endpoint")
    response.raise_for_status()
    data = response.json()
```

### Testing with Mocked Client

Tests must mock `get_client` in the module where it's used:

```python
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

with patch("open_webui_admin.MODULE.get_client") as mock_get_client:
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_get_client.return_value.__exit__ = MagicMock(return_value=False)
```

### Adding New Commands

1. Add command to appropriate module (or create new module)
2. Import and register in `cli.py` using `cli.add_command(group)`
3. Add tests to corresponding `tests/test_MODULE.py`

## API Endpoints Used

- `/api/v1/models/list` - List custom models with full details
- `/openai/models` - List all models
- `/openai/config` - OpenAI configuration
- `/ollama/config` - Ollama configuration
- `/api/v1/configs/export` - Export all config
- `/api/v1/configs/banners` - Manage banners
- `/api/v1/images/models` - List image models
- `/api/v1/audio/models` - List audio models
- `/api/v1/audio/voices` - List voices
- `/openai/chat/completions` - Verify model (POST)
- `/api/v1/users/` - Get all users, paginated

## Dependencies

Managed with Poetry (`pyproject.toml`):
- `httpx` - HTTP client
- `click` - CLI framework
- `pytest` - Testing (dev)
- `pytest-mock` - Mocking support (dev)
- `pytest-cov` - Coverage reporting (dev)

## Building the Package

```bash
poetry build
```

This creates:
- `dist/open_webui_admin-*.whl`
- `dist/open_webui_admin-*.tar.gz`
