# Config Commands

Manage configuration settings for your Open WebUI instance.

## Commands

| Command | Description |
|---------|-------------|
| `config get --name openai` | Get OpenAI configuration |
| `config get --name openai --json` | Get OpenAI configuration as JSON |
| `config get --name ollama` | Get Ollama configuration |
| `config get --name ollama --json` | Get Ollama configuration as JSON |
| `config export` | Export all configuration |

## Get OpenAI Configuration

Retrieve the OpenAI API configuration:

```bash
open-webui-admin config get --name openai
```

Output includes:
- API base URLs
- API keys (masked)
- Model list
- Connection settings

### JSON Output

Get the full configuration as JSON:

```bash
open-webui-admin config get --name openai --json
```

Output:
```json
{
  "OPENAI_API_BASE_URLS": ["https://api.openai.com/v1"],
  "OPENAI_API_KEYS": ["sk-..."],
  ...
}
```

## Get Ollama Configuration

Retrieve the Ollama configuration:

```bash
open-webui-admin config get --name ollama
```

Output includes:
- Ollama base URL
- Available models
- Connection settings

### JSON Output

Get the full configuration as JSON:

```bash
open-webui-admin config get --name ollama --json
```

## Export All Configuration

Export the complete configuration as JSON:

```bash
open-webui-admin config export
```

Output:
```json
{
  "OPENAI_API_BASE_URLS": ["https://api.openai.com/v1"],
  "OLLAMA_BASE_URL": "http://localhost:11434",
  ...
}
```

This is useful for:
- Backup purposes
- Migrating configurations
- Debugging configuration issues

## Note

The `config get` command requires the `--name` parameter with either `openai` or `ollama`.
