from pathlib import Path
from typing import List, Dict, Any

import click
import yaml

from agileupstate.terminal import print_cross_message


class State:

    def __init__(self, client, state_file='siab-state.yml'):
        self.client = client
        self.state_file = state_file

    def file(self):
        return self.state_file

    def data(self) -> dict[str, Any]:
        return {'client-id': self.client.id,
                'client-cloud': self.client.cloud,
                'client-location': self.client.location,
                'client-context': self.client.context,
                }

    def write(self) -> None:
        file = Path(self.state_file)
        with open(file, 'w') as f:
            yaml.dump(self.data(), f, sort_keys=False, default_flow_style=False)

    def read(self) -> dict:
        file = Path(self.state_file)
        if file.is_file():
            click.echo(f'- Reading {file}')
            with open(file, 'r') as f:
                return yaml.safe_load(f)
        else:
            print_cross_message(f'Could not read from state file {file}!', leave=True)
