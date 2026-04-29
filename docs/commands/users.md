# Users Commands

Manage users in your Open WebUI instance.

## Commands

| Command | Description |
|---------|-------------|
| `users get --all` | List all users |
| `users get --all --json` | List all users in JSON format |
| `users get --include-email <regex>` | Include users matching email pattern |
| `users get --exclude-email <regex>` | Exclude users matching email pattern |

## List All Users

Get all users in table format:

```bash
open-webui-admin users get --all
```

Output:
```
user_id | name | email | role
12345 | John Doe | john@example.com | admin
67890 | Jane Smith | jane@example.com | user
```

## List All Users (JSON)

Get all users in JSON format for programmatic use:

```bash
open-webui-admin users get --all --json
```

Output:
```json
[
  {
    "id": "12345",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
  },
  ...
]
```

## Filter Users by Email

### Include Email Pattern

Include only users whose email matches a regex pattern (can be used multiple times):

```bash
open-webui-admin users get --all --include-email "@example.com"
open-webui-admin users get --all --include-email "@admin.com" --include-email "@test.com"
```

### Exclude Email Pattern

Exclude users whose email matches a regex pattern (can be used multiple times):

```bash
open-webui-admin users get --all --exclude-email "@spam.com"
open-webui-admin users get --all --exclude-email "@old-domain.com" --exclude-email "@temp.com"
```

### Combine Include and Exclude

```bash
open-webui-admin users get --all --include-email "@example.com" --exclude-email "@test.example.com"
```

## User Roles

| Role | Description |
|------|-------------|
| `admin` | Full administrative access |
| `user` | Standard user access |
| `pending` | User awaiting approval |

## Note

The `users get` command requires the `--all` flag to retrieve all users. User listing is paginated internally.
