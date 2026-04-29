import click
import json
import re
from .client import get_client


@click.group("users")
def users():
    """Manage users."""
    pass


@users.command("get")
@click.option("--all", "all_users", is_flag=True, help="Get all users")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--include-email", multiple=True, help="Include users with email matching regex pattern (can be used multiple times)")
@click.option("--exclude-email", multiple=True, help="Exclude users with email matching regex pattern (can be used multiple times)")
def users_get(all_users, json_output, include_email, exclude_email):
    """Get users."""
    with get_client() as client:
        response = client.get("/api/v1/users/all")
        response.raise_for_status()
        data = response.json()

        users = data.get("users", [])

        if include_email:
            include_patterns = [re.compile(p) for p in include_email]
            users = [u for u in users if any(p.search(u.get("email", "")) for p in include_patterns)]

        if exclude_email:
            exclude_patterns = [re.compile(p) for p in exclude_email]
            users = [u for u in users if not any(p.search(u.get("email", "")) for p in exclude_patterns)]

        if json_output:
            click.echo(json.dumps({"users": users, "count": len(users)}, indent=2))
        else:
            if users:
                for user in users:
                    user_id = user.get("id", "")
                    name = user.get("name", "")
                    email = user.get("email", "")
                    role = user.get("role", "")
                    click.echo(f"{user_id} | {name} | {email} | {role}")
                click.echo(f"\nTotal: {len(users)} users")
            else:
                click.echo("No users found")
