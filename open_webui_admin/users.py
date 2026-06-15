import click
import json
import re
from .client import get_client
from .output import print_table, print_json


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
            print_json({"users": users, "count": len(users)})
        else:
            if users:
                rows = [{"id": u.get("id", ""), "name": u.get("name", ""), "email": u.get("email", ""), "role": u.get("role", "")} for u in users]
                print_table(
                    rows,
                    [("USER_ID", "id", 36), ("NAME", "name", 20), ("EMAIL", "email", 30), ("ROLE", "role", 5)],
                    json_output=False,
                    simple_output=False,
                )
                click.echo(f"\nTotal: {len(users)} users")
            else:
                click.echo("No users found")
