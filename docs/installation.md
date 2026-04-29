# Installation

## Prerequisites

- Python 3.12 or higher
- pip or Poetry

## Install from PyPI

```bash
pip install open-webui-admin
```

## Install from Source

```bash
git clone https://github.com/anomalyco/openwebui-models.git
cd openwebui-models
poetry install
poetry build
pip install dist/open_webui_admin-*.whl
```

## Verify Installation

```bash
open-webui-admin --help
```

Output:

```shell
Usage: open-webui-admin [OPTIONS] COMMAND [ARGS]...

  Open WebUI validation tool.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  audio      Manage audio.
  banners    Manage banners.
  config     Manage config.
  connections
              Manage connections.
  images     Manage images.
  models     Manage models.
  users      Manage users.
```
