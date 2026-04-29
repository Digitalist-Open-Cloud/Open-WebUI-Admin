# Configuration

## Environment Variables

Open WebUI Admin requires two environment variables to connect to your Open WebUI instance:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENWEBUI_URL` | Base URL of Open WebUI instance | `https://open-webui.example.com` |
| `OPENWEBUI_TOKEN` | Authentication token | `sadad4354JIUzI1NiIsfff6IkpXVCJ9...` |

## Setting Environment Variables

### Linux/macOS

```bash
export OPENWEBUI_URL="https://your-openwebui.example.com"
export OPENWEBUI_TOKEN="your-token-here"
```

### Windows (PowerShell)

```powershell
$env:OPENWEBUI_URL="https://your-openwebui.example.com"
$env:OPENWEBUI_TOKEN="your-token-here"
```

### Using .env file

You can also create a `.env` file in your working directory:

```bash
OPENWEBUI_URL=https://your-openwebui.example.com
OPENWEBUI_TOKEN=your-token-here
```

## Getting Your Token

1. Log in to your Open WebUI instance
2. Go to **Account Settings**
3. Look for **API Key** or **Token** section
4. Copy the token and set it as `OPENWEBUI_TOKEN`

## Verifying Configuration

Test your configuration by listing models:

```bash
open-webui-admin models list
```
