import os
from sys import platform

import click
import pkg_resources

from agileupstate.terminal import print_check_message, print_cross_message


def get_version_string() -> str:
    return f"AgileUp State Version: {pkg_resources.get_distribution('agileupstate').version}"


def supported_os() -> bool:
    if platform == 'linux' or platform == 'linux2':
        return True
    elif platform == 'darwin':
        return True
    elif platform == 'win32':
        return False


class Client:

    def __init__(self, updated=False):
        self.version = get_version_string()
        self.updated = updated

        if supported_os():
            print_check_message(f'Client machine supported {platform}')
        else:
            print_cross_message(f'Client machine not supported {platform}!', leave=True)

        try:
            self.id = os.environ['SIAB_ID']
            self.cloud = os.environ['SIAB_CLOUD']
            self.location1 = os.environ['SIAB_LOCATION1']
            self.location2 = os.environ['SIAB_LOCATION2']
            self.context = os.environ['SIAB_CONTEXT']
            self.values_path = os.environ['SIAB_VALUES_PATH']
            self.vault_addr = os.environ['VAULT_ADDR']
            self.vault_token = os.environ['VAULT_TOKEN']
            self.display()
        except KeyError as e:
            print_cross_message(f'Missing key {e}!', leave=True)

    def display(self) -> None:
        if self.updated:
            message = f'- Updated client ({self.id} {self.cloud} {self.location1} {self.context}) {self.version}'
            click.secho(message, fg='yellow')
        else:
            message = f'- Running client ({self.id} {self.cloud} {self.location1} {self.context}) {self.version}'
            click.secho(message, fg='blue')

    def vault_addr(self) -> str:
        return self.vault_addr

    def vault_token(self) -> str:
        return self.vault_token

    def values_path(self) -> str:
        return self.values_path

    def validate(self, data: dict) -> None:
        try:
            if self.id != data['siab-id']:
                print_cross_message(f'Client out of sync error {self.id}!', leave=True)
            if self.cloud != data['siab-cloud']:
                print_cross_message(f'Client out of sync error {self.cloud}!', leave=True)
            if self.location1 != data['siab-location1']:
                print_cross_message(f'Client out of sync error {self.location1}!', leave=True)
            if self.location2 != data['siab-location2']:
                print_cross_message(f'Client out of sync error {self.location2}!', leave=True)
            if self.context != data['siab-context']:
                print_cross_message(f'Client out of sync error {self.context}!', leave=True)
            if self.values_path != data['siab-values-path']:
                print_cross_message(f'Client out of sync error {self.values_path}!', leave=True)
            self.display()
        except KeyError as e:
            print_cross_message(f'Missing key {e}!', leave=True)

    def update(self, data) -> None:
        self.id = data['siab-id']
        self.cloud = data['siab-cloud']
        self.location1 = data['siab-location1']
        self.location2 = data['siab-location2']
        self.context = data['siab-context']
        self.values_path = data['siab-values-path']
        self.updated = True
        self.display()
