import click
from . import __version__
from .models import models
from .banners import banners
from .images import images
from .audio import audio
from .config import config
from .connections import connections
from .users import users
from .knowledge import knowledge
from .files import files


@click.group()
@click.version_option(version=__version__)
def cli():
    """Open WebUI validation tool."""
    pass


cli.add_command(models)
cli.add_command(banners)
cli.add_command(images)
cli.add_command(audio)
cli.add_command(config)
cli.add_command(connections)
cli.add_command(users)
cli.add_command(knowledge)
cli.add_command(files)


if __name__ == "__main__":
    cli()
