# Audio Commands

Manage audio models and voices in your Open WebUI instance.

## Commands

| Command | Description |
|---------|-------------|
| `audio models` | List audio models |
| `audio voices` | List available voices |

## List Audio Models

List all available audio transcription/models:

```bash
open-webui-admin audio models
```

Output:
```
whisper-1
whisper-large-v3
```

## List Available Voices

List all available text-to-speech voices:

```bash
open-webui-admin audio voices
```

Output:
```
alloy
echo
fable
onyx
nova
shimmer
```

## Supported Audio Features

- **Transcription**: Speech-to-text using Whisper models
- **Text-to-Speech**: Convert text to spoken audio with various voices

## Note

Audio models and voices are listed from the `/api/v1/audio/models` and `/api/v1/audio/voices` endpoints. Availability depends on your Open WebUI configuration and enabled connections (typically OpenAI).
