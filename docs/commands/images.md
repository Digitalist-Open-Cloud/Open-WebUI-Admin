# Images Commands

Manage image models in your Open WebUI instance.

## Commands

| Command | Description |
|---------|-------------|
| `images list` | List available image models |

## List Image Models

List all available image generation models:

```bash
open-webui-admin images list
```

Output:
```
dall-e-3
stable-diffusion-xl
flux-pro
midjourney-v6
```

## Supported Image Models

Image models are typically provided by:
- OpenAI (DALL-E series)
- Replicate (Stable Diffusion, FLUX, etc.)
- Custom pipelines

## Note

Image models are listed from the `/api/v1/images/models` endpoint. The availability depends on your Open WebUI configuration and enabled connections.
