import click

from agileupstate.client import get_version_string
from agileupstate.terminal import print_check_message, print_cross_message
from agileupstate.vault import address, is_ready, create_state, load_state, create_tfstate

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(help='CLI to manage pipeline states.')
def cli() -> int:
    pass


@cli.command(help='Display the current version.')
def version() -> None:
    click.echo(get_version_string())


@cli.command(help='Check client configuration.')
def check() -> None:
    click.secho('Checking client configuration.', fg='green')
    if is_ready():
        print_check_message('Vault backend is available')
    else:
        print_cross_message(f'Vault backend failed from: {address()}', leave=True)


@cli.command(help='Create client state and vault path.')
def create() -> None:
    click.secho('- Create client state', fg='green')
    create_state()


@cli.command(help='Update client state.')
@click.option('--config-type', required=True, type=click.Choice(['TERRAFORM', 'ANSIBLE'], case_sensitive=True),
              help='Choose required configuration framework')
def update(config_type) -> None:
    click.secho(f'- Update client state for config {config_type}', fg='green')
    state = load_state()
    tfstate_content = state.tfstate(file='resources/tests/terraform.tfstate')
    create_tfstate(state, tfstate_content)


@cli.command(help='Save client state.')
def save() -> None:
    click.secho('- Save client state', fg='green')


@cli.command(help='Load client state.')
def fetch() -> None:
    click.secho('- Load client state', fg='green')


if __name__ == '__main__':
    exit(cli())
