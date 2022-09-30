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


def create_state() -> State:
    client = Client()
    state = State(client)
    hvac_client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )
    hvac_client.secrets.kv.v2.create_or_update_secret(
        path=state.vault_state_path,
        secret=state.client_state_data
    )
    click.secho(f'- Created state data in vault {state.vault_state_path}', fg='blue')
    state.write()
    state.write_names()
    return state


def load_state() -> State:
    client = Client()
    state = State(client)
    hvac_client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )
    try:
        response = hvac_client.secrets.kv.read_secret_version(path=state.vault_state_path)
        click.secho(f'- Loaded state data from vault {state.vault_state_path}', fg='blue')
        click.secho('- Created time: {created_time} Version: {version} '.format(
            created_time=response['data']['metadata']['created_time'],
            version=response['data']['metadata']['version'],
        ), fg='blue')
        client.validate(response['data']['data'])
        client.update(response['data']['data'])
        state.write()
        state.write_names()
        return state
    except InvalidPath:
        print_cross_message(f'Could not find {state.vault_state_path} path in: {address()}', leave=True)


def create_tfstate(state: State, tfstate_content: dict) -> None:
    hvac_client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )
    hvac_client.secrets.kv.v2.create_or_update_secret(
        path=state.vault_tfstate_path,
        secret=tfstate_content
    )
    click.secho(f'- Created tfstate data in vault {state.vault_tfstate_path}', fg='blue')


def load_tfstate() -> dict:
    client = Client()
    state = State(client)
    hvac_client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )
    response = hvac_client.secrets.kv.read_secret_version(path=state.vault_tfstate_path)
    click.secho(f'- Loaded state data from vault {state.vault_tfstate_path}', fg='blue')
    click.secho('- Created time: {created_time} Version: {version} '.format(
        created_time=response['data']['metadata']['created_time'],
        version=response['data']['metadata']['version'],
    ), fg='blue')
    return response['data']['data']
