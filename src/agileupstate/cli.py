import click
import pkg_resources

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(help='Pipeline support cli.')
def cli() -> int:
    pass


@cli.command(help='Display the current version.')
def version() -> None:
    click.echo(f"Version: {pkg_resources.get_distribution('agileup').version}")


@cli.command(help='Check client configuration.')
def check() -> None:
    click.secho('- Checking client configuration', fg='green')


@cli.command(help='Update client state.')
def update() -> None:
    click.secho('- Update client state', fg='green')


@cli.command(help='Save client state.')
def save() -> None:
    click.secho('- Save client state', fg='green')


@cli.command(help='Fetch client state.')
def fetch() -> None:
    click.secho('- Fetch client state', fg='green')


if __name__ == '__main__':
    exit(cli())
