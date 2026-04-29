# Models Commands

Manage models in your Open WebUI instance.

## Commands Overview

| Command | Description |
|---------|-------------|
| `models list` | List all available models |
| `models list -v` | List models with provider/connection info |
| `models custom list` | List custom/preset models |
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

## List Models

List all available models (standard + custom):

```bash
open-webui-admin models list
```

### Verbose Output

List with provider and connection info:

```bash
open-webui-admin models list -v
```

Output format:
```
model_id | provider | connection_type | urlIdx | url
```

Example:
```
gpt-5 | openai | external | 1 | https://api.openai.com/v1
claude-3 | anthropic | external | 2 | https://api.anthropic.com/v1
llama3 | ollama | local | 0 |
```

### Provider Detection

The `provider` field is inferred from:
- Model name prefix (e.g., `anthropic.`, `claude-`, `gemini`, `deepseek`)
- URL display (e.g., `api.openai.com` → `openai`)
- Special patterns (e.g., `replicate_`, `flux`, `llama`, `mistral`)

## Custom Models

### List Custom Models

List custom/preset models with base_model_id:

```bash
open-webui-admin models custom list
```

Output:
```
dada (base: gpt-4o)
my-custom-model (base: claude-3)
```

### Show Specific Custom Model

Show full JSON for a specific custom model:

```bash
open-webui-admin models custom list --name dada
```

## Check Model Validity

Check if a model is valid (exists in the instance):

```bash
open-webui-admin models check --name gpt-4o
```

Verbose output includes provider and URL:
```bash
open-webui-admin models check --name gpt-4o -v
```

## Models Configuration

Get the models configuration:

```bash
open-webui-admin models config
```

Output:
```json
{
  "models": [...],
  ...
}
```

## Verify Models

Verification sends a test request to the model's chat completions endpoint.

### Verify Single Model

```bash
open-webui-admin models verify --name gpt-4o
```

Output:
```
Model 'gpt-4o' is working
```

If the model fails:
```
Model 'anthropic.claude-opus-4-6' is NOT working: authentication_error
```

### Debug Output

Show full API response for debugging:

```bash
open-webui-admin models verify --name gpt-4o --debug
```

### Verify All Models

```bash
open-webui-admin models verify --all
```

Output:
```
Verifying 134 models...

[OK] gpt-5
[FAIL] anthropic.claude-opus-4-6 | authentication_error
[ERROR] test-model | 500
...

134 models verified
```

With verbose flag (shows provider/URL info):
```bash
open-webui-admin models verify --all -v
```

Output:
```
[OK] gpt-5 | https://api.openai.com/v1
[FAIL] anthropic.claude-opus-4-6 | https://api.anthropic.com/v1 | authentication_error
```

With debug flag (shows full API response):
```bash
open-webui-admin models verify --all --debug
```

### Verify All Custom Models

```bash
open-webui-admin models custom verify --all
```

With verbose flag:
```bash
open-webui-admin models custom verify --all -v
```

With debug flag:
```bash
open-webui-admin models custom verify --all --debug
```

### Verify Specific Custom Model

```bash
open-webui-admin models custom verify --name dada
```

With debug flag:
```bash
open-webui-admin models custom verify --name dada --debug
```

## Output Formats

### models list -v
```
model_id | provider | connection_type | urlIdx | url
```
- `provider`: Inferred from model name or URL
- `connection_type`: `external` or `local`
- `urlIdx`: Index into configured API endpoints
- `url`: The actual API endpoint URL

### models verify --all
```
[OK] model_name
[FAIL] model_name | error_message
[ERROR] model_name | status_code
```

## Error Messages

| Error | Description |
|-------|-------------|
| `authentication_error` | Invalid API key |
| `invalid x-api-key` | API key is invalid |
| `not_found` | Model not found (404) |
| `not_chat_model` | Model doesn't support chat completions |
| `server_error` | Upstream provider error (500) |
| `timeout` | Request timed out |
| `connection` | Connection error |
