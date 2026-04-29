# Banners Commands

Manage banners in your Open WebUI instance.

## Commands

| Command | Description |
|---------|-------------|
| `banners get` | Get current banners |
| `banners set` | Set a banner |
| `banners set --dismissible` | Set a dismissible banner |
| `banners clear` | Clear all banners |

## Get Banners

Retrieve current banners:

```bash
open-webui-admin banners get
```

Output:
```json
[
  {
    "type": "Warning",
    "title": "System Update",
    "content": "Maintenance scheduled for Sunday 2AM-4AM"
  }
]
```

## Set Banner

Set a new banner with title and content:

```bash
open-webui-admin banners set --type Warning --title "System Update" --content "Maintenance scheduled"
```

Options:
- `--type` (required): Banner type - `Info`, `Warning`, `Error`, `Success`
- `--title`: Banner title text
- `--content` (required): Banner message content
- `--dismissible` (flag, default: True): Whether the banner can be dismissed by users

### Set Non-Dismissible Banner

```bash
open-webui-admin banners set --type Error --title "Critical" --content "System down" --dismissible
```

### Banner Types

| Type | Description |
|------|-------------|
| `Info` | Informational banner (blue) |
| `Warning` | Warning banner (yellow/orange) |
| `Error` | Error banner (red) |
| `Success` | Success banner (green) |

## Clear Banners

Remove all banners:

```bash
open-webui-admin banners clear
```

Output:
```
Banners cleared
```

## Banner Properties

| Property | Description |
|----------|-------------|
| `type` | Banner type (Info, Warning, Error, Success) |
| `title` | Banner title text |
| `content` | Banner message content |

## Use Cases

- Announce scheduled maintenance
- Display system warnings
- Show important notifications to all users
- Celebrate successful updates (Success type)
