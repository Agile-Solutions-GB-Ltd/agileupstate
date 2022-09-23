import os

import hvac

from agileupstate.terminal import print_cross_message, print_check_message


def address():
    return os.environ['VAULT_ADDR']


def is_ready() -> bool:
    client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )
    if client.sys.is_sealed():
        return print_cross_message(f'Vault is sealed: {address()}')
    else:
        if client.is_authenticated():
            return print_check_message(f'Vault client authenticated to: {address()}')
        else:
            return print_cross_message(f'Vault client failed to authenticate to: {address()}')
