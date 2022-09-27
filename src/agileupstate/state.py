import json
from pathlib import Path

import click
import yaml

from agileupstate.client import Client
from agileupstate.terminal import print_cross_message


class State:

    def __init__(self, client: Client, state_file='siab-state.yml'):
        self.client = client
        self.state_file = state_file
        self.vault_state_path = 'siab-state/' \
                                + self.client.id + '-' \
                                + self.client.cloud + '-' \
                                + self.client.location + '-' \
                                + self.client.context
        self.vault_tfstate_path = 'tfsiab-state/' \
                                  + self.client.id + '-' \
                                  + self.client.cloud + '-' \
                                  + self.client.location + '-' \
                                  + self.client.context

        self.client_state_data = {'client-id': self.client.id,
                                  'client-cloud': self.client.cloud,
                                  'client-location': self.client.location,
                                  'client-context': self.client.context,
                                  }

    @staticmethod
    def tfstate(file='terraform.tfstate') -> dict:
        with open(file, 'r') as tfstate_file:
            tfstate_content = json.loads(tfstate_file.read())
        return tfstate_content

    def write(self) -> None:
        file = Path(self.state_file)
        click.secho(f'- Writing {file}', fg='blue')
        with open(file, 'w') as f:
            yaml.dump(self.client_state_data, f, sort_keys=False, default_flow_style=False)

    def read(self) -> dict:
        file = Path(self.state_file)
        if file.is_file():
            click.secho(f'- Reading {file}', fg='blue')
            with open(file, 'r') as f:
                return yaml.safe_load(f)
        else:
            print_cross_message(f'Could not read from state file {file}!', leave=True)
