import os

import click
import hvac
from hvac.exceptions import InvalidPath

from agileupstate.client import Client
from agileupstate.state import State
from agileupstate.terminal import print_cross_message, print_check_message


def address():
    return os.environ['VAULT_ADDR']


def is_ready() -> bool:
    client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )
    if client.sys.is_sealed():
        return print_cross_message(f'Vault is sealed: {address()}', leave=True)
    else:
        if client.is_authenticated():
            print_check_message(f'Vault client authenticated to: {address()}')
            try:
                client.secrets.kv.v2.create_or_update_secret(
                    path='siab/smoke-test',
                    secret=dict(test='this is a vault engine smoke test'),
                )
                list_response = client.secrets.kv.v2.list_secrets(path='siab')
                print('The following paths are available under "siab" prefix: {keys}'.format(
                    keys=','.join(list_response['data']['keys']),
                ))
                return print_check_message(f'Vault client secrets backend validated: {address()}')
            except InvalidPath:
                return print_cross_message(f'Could not find KV v2 siab path in: {address()}', leave=True)

        else:
            return print_cross_message(f'Vault client failed to authenticate to: {address()}', leave=True)


def create_state() -> None:
    client = Client()
    state = State(client)
    state.write()

    client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )
    state_path = 'siab/' \
                 + state.client.id + '-' \
                 + state.client.cloud + '-' \
                 + state.client.location + '-' \
                 + state.client.context
    client.secrets.kv.v2.create_or_update_secret(
        path=state_path,
        secret=state.data()
    )
    click.secho(f'- Created state data in vault {state_path} and file {state.file()}', fg='blue')
