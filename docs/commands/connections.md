# Connections Commands

Manage and verify external connections in your Open WebUI instance.

## Commands

| Command | Description |
|---------|-------------|
| `connections verify` | Verify OpenAI and Ollama connections |

## Verify Connections

Verify that external connections (OpenAI, Ollama) are properly configured and accessible:

```bash
open-webui-admin connections verify
```

This command checks:
- OpenAI API connectivity
- Ollama local instance connectivity
- Authentication validity

### Example Output

```
=== OpenAI Connections ===
[OK] https://api.openai.com/v1
[FAIL] https://api.anthropic.com/v1 - 401

=== Ollama Connections ===
[OK] http://localhost:11434
```

## Troubleshooting

If a connection fails, check:
1. The `OPENWEBUI_URL` and `OPENWEBUI_TOKEN` are correct
2. The external service (OpenAI, Ollama) is running and accessible
3. API keys are valid and have proper permissions
4. Network connectivity to the external service
