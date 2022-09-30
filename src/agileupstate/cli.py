import click

from agileupstate.ansible import create_inventory
from agileupstate.client import get_version_string
from agileupstate.terminal import print_check_message, print_cross_message
from agileupstate.vault import address, is_ready, create_state, load_state, create_tfstate, load_tfstate

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


@cli.command(help='Create client vault states.')
def create() -> None:
    click.secho('- Create client vault states', fg='green')
    create_state()


@cli.command(help='Save client states to vault.')
def save() -> None:
    click.secho('- Save client states to vault', fg='green')
    state = load_state()
    tfstate_content = state.read_tfstate()
    create_tfstate(state, tfstate_content)


@cli.command(help='Load client states from vault.')
def load() -> None:
    click.secho('- Load client states from vault', fg='green')
    state = load_state()
    tfstate_content = load_tfstate()
    state.write_tfstate(tfstate_content)


@cli.command(help='Create ansible inventory from vault tfstate.')
def inventory() -> None:
    click.secho('- Creating ansible inventory from vault tfstate', fg='green')
    state = load_state()
    tfstate_content = state.read_tfstate()
    create_inventory(state, tfstate_content)


if __name__ == '__main__':
    exit(cli())
