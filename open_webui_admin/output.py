import json
import sys
from typing import Optional

import click


def print_table(
    rows: list[dict],
    cols: list[tuple[str, str, int]],
    json_output: bool = False,
    simple_output: bool = False,
):
    """Print aligned table with optional JSON or simple output.

    cols: [(header, key, min_width), ...]
    """
    if json_output:
        click.echo(json.dumps(rows, indent=2, default=str))
        return

    if not rows:
        click.echo("(none)")
        return

    if simple_output:
        # Simple output: just print the values, one per line
        for row in rows:
            values = [str(row.get(k, "")) for _, k, _ in cols]
            click.echo("  ".join(values))
        return

    # Colored table output
    green = "\033[92m"
    cyan = "\033[96m"
    reset = "\033[0m"
    dim = "\033[2m"

    widths = [
        max(mw, len(h), max((len(str(r.get(k, ""))) for r in rows), default=0))
        for h, k, mw in cols
    ]

    # Header
    header = "  ".join(f"{cyan}{h:<{w}}{reset}" for (h, _, _), w in zip(cols, widths))
    click.echo(header)
    # Separator
    sep = "  ".join(f"{dim}{'-' * w}{reset}" for w in widths)
    click.echo(sep)
    # Rows
    for row in rows:
        line = "  ".join(f"{green}{str(row.get(k, '')):<{w}}{reset}" for (_, k, _), w in zip(cols, widths))
        click.echo(line)


def print_kv(
    pairs: list[tuple[str, str]],
    json_output: bool = False,
    simple_output: bool = False,
):
    """Print key-value pairs with optional JSON or simple output."""
    if json_output:
        click.echo(json.dumps(dict(pairs), indent=2, default=str))
        return

    if simple_output:
        for k, v in pairs:
            click.echo(f"{v}")
        return

    green = "\033[92m"
    cyan = "\033[96m"
    reset = "\033[0m"

    if not pairs:
        return
    w = max(len(k) for k, _ in pairs)
    for k, v in pairs:
        click.echo(f"{cyan}{k:<{w}}{reset}  {green}{v}{reset}")


def print_json(data):
    """Print data as JSON."""
    click.echo(json.dumps(data, indent=2, default=str))


def print_success(msg: str):
    """Print success message in green."""
    click.echo(f"\033[92m{msg}\033[0m")


def print_error(msg: str):
    """Print error message in red."""
    click.echo(f"\033[91m{msg}\033[0m", err=True)


def print_warning(msg: str):
    """Print warning message in yellow."""
    click.echo(f"\033[93m{msg}\033[0m")


def die(msg: str, code: int = 1):
    """Print error and exit."""
    print_error(msg)
    sys.exit(code)
