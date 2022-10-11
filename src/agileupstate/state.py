import json
from pathlib import Path

import click
import yaml

from agileupstate.client import Client
from agileupstate.terminal import print_cross_message


class State:

    def __init__(self, state_file='siab-state.yml', state_export_file='siab-state-export.sh'):
        self.client = Client()
        self.state_file = state_file
        self.state_export_file = state_export_file
        self.values_path = self.client.values_path
        self.state_name = self.client.id + '-' + self.client.cloud + '-' + self.client.location1 + '-' + self.client.context
        self.state_name_underscore = self.client.id + '_' + self.client.cloud + '_' + self.client.location1 + '_' + self.client.context

        self.vault_state_path = 'siab-state/' \
                                + self.client.id + '-' \
                                + self.client.cloud + '-' \
                                + self.client.location1 + '-' \
                                + self.client.context

        self.vault_tfstate_path = 'siab-tfstate/' \
                                  + self.client.id + '-' \
                                  + self.client.cloud + '-' \
                                  + self.client.location1 + '-' \
                                  + self.client.context

        self.siab_state_data = {'siab-id': self.client.id,
                                'siab-cloud': self.client.cloud,
                                'siab-location1': self.client.location1,
                                'siab-location2': self.client.location2,
                                'siab-context': self.client.context,
                                'siab-values-path': self.client.values_path,
                                }

    def validate(self, data: dict):
        self.client.validate(data)

    def update(self, data: dict):
        self.client.update(data)

    @staticmethod
    def read_tfstate(file='terraform.tfstate') -> dict:
        file_path = Path(file)
        if file_path.is_file():
            with open(file, 'r') as tfstate_file:
                tfstate_content = json.loads(tfstate_file.read())
            return tfstate_content
        else:
            print_cross_message(f'Could not read from state file {file}!', leave=True)

    @staticmethod
    def write_tfstate(tfstate_content, file='terraform.tfstate') -> None:
        click.secho(f'- Writing {file}', fg='blue')
        with open(file, 'w') as tfstate_file:
            json.dump(tfstate_content, tfstate_file)

    def write(self) -> None:
        file = Path(self.state_file)
        click.secho(f'- Writing {file}', fg='blue')
        with open(file, 'w') as f:
            yaml.dump(self.siab_state_data, f, sort_keys=False, default_flow_style=False)

    def write_exports(self, state_values_filename) -> None:
        file = Path(self.state_export_file)
        state_values = self.read(state_values_filename)
        line1 = f'export TF_VAR_siab_name={self.state_name}'
        line2 = f'export TF_VAR_siab_name_underscore={self.state_name_underscore}'
        click.secho(f'- Writing {file}', fg='blue')
        with open(file, 'w') as f:
            for key, value in state_values['connection'].items():
                f.write('export SIAB_{}={}\n'.format(key, value))
            for key, value in state_values['cloud'].items():
                f.write('export TF_VAR_{}={}\n'.format(key, value))
            f.write(line1 + '\n')
            f.write(line2 + '\n')

    @staticmethod
    def read(filename) -> dict:
        file_path = Path(filename)
        if file_path.is_file():
            click.secho(f'- Reading {file_path}', fg='blue')
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            print_cross_message(f'Could not read from state file {file_path}!', leave=True)
