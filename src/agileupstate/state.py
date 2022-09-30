import json
from pathlib import Path

import click
import yaml

from agileupstate.client import Client
from agileupstate.terminal import print_cross_message


class State:

    def __init__(self, client: Client, state_file='siab-state.yml', state_name_file='siab-state-names.sh'):
        self.client = client
        self.state_file = state_file
        self.state_name_file = state_name_file
        self.state_name = self.client.id + '-' + self.client.cloud + '-' + self.client.location + '-' \
            + self.client.context
        self.state_name_underscore = self.client.id + '_' + self.client.cloud + '_' + self.client.location + '_' \
            + self.client.context

        self.vault_state_path = 'siab-state/' \
                                + self.client.id + '-' \
                                + self.client.cloud + '-' \
                                + self.client.location + '-' \
                                + self.client.context
        self.vault_tfstate_path = 'siab-tfstate/' \
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
    def read_tfstate(file='terraform.tfstate') -> dict:
        with open(file, 'r') as tfstate_file:
            tfstate_content = json.loads(tfstate_file.read())
        return tfstate_content

    @staticmethod
    def write_tfstate(tfstate_content, file='terraform.tfstate') -> None:
        with open(file, 'w') as tfstate_file:
            json.dump(tfstate_content, tfstate_file)

    def write(self) -> None:
        file = Path(self.state_file)
        click.secho(f'- Writing {file}', fg='blue')
        with open(file, 'w') as f:
            yaml.dump(self.client_state_data, f, sort_keys=False, default_flow_style=False)

    def write_names(self) -> None:
        name1 = f'export TF_VAR_siab_name={self.state_name}'
        name2 = f'export TF_VAR_siab_name_underscore={self.state_name_underscore}'
        file = Path(self.state_name_file)
        click.secho(f'- Writing {file}', fg='blue')
        with open(file, 'w') as f:
            f.write(name1 + '\n')
            f.write(name2 + '\n')

    def read(self) -> dict:
        file = Path(self.state_file)
        if file.is_file():
            click.secho(f'- Reading {file}', fg='blue')
            with open(file, 'r') as f:
                return yaml.safe_load(f)
        else:
            print_cross_message(f'Could not read from state file {file}!', leave=True)
