# Open WebUI Admin

CLI tool for managing Open WebUI instances.

## Overview

Open WebUI Admin provides a command-line interface to manage and validate Open WebUI configurations, including models, users, connections, and more.

## Quick Start

```bash
# Install the tool
pip install open-webui-admin

# Set environment variables
export OPENWEBUI_URL="https://your-openwebui.example.com"
export OPENWEBUI_TOKEN="your-token"

# List available models
open-webui-admin models list
```

## Commands

| Command | Description |
|---------|-------------|
| `models list` | List all available models (standard + custom) |
| `models list -v` | List models with provider/connection info |
| `models custom list` | List custom/preset models |
| `models custom list --name <model>` | Show full JSON for a specific custom model |
| `models check --name <model>` | Check if a model is valid |
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

## Getting Help

For detailed documentation on each command, see the [Commands](commands/models.md) section.
