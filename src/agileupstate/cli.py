import click
import pkg_resources

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(help='CLI to manage pipeline states.')
def cli() -> int:
    pass


@cli.command(help='Display the current version.')
def version() -> None:
    click.echo(f"AgileUp State Version: {pkg_resources.get_distribution('agileupstate').version}")


@cli.command(help='Check client configuration.')
def check() -> None:
    click.secho('- Checking client configuration', fg='green')


@cli.command(help='Create client state.')
def create() -> None:
    click.secho('- Create client state', fg='green')


@cli.command(help='Update client state.')
def update() -> None:
    click.secho('- Update client state', fg='green')


@cli.command(help='Save client state.')
def save() -> None:
    click.secho('- Save client state', fg='green')


@cli.command(help='Load client state.')
def fetch() -> None:
    click.secho('- Load client state', fg='green')


if __name__ == '__main__':
    exit(cli())
