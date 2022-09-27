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


@cli.command(help='Create client vault state.')
def create() -> None:
    click.secho('- Create client vault state', fg='green')
    create_state()


@cli.command(help='Load client state from vault.')
def load() -> None:
    click.secho('- Load client state from vault', fg='green')
    load_state()


@cli.command(help='Save client state.')
def save() -> None:
    click.secho('- Save client vault state', fg='green')
    state = load_state()
    tfstate_content = state.tfstate()
    create_tfstate(state, tfstate_content)


if __name__ == '__main__':
    exit(cli())
