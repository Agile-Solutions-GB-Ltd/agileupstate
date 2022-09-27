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
        except KeyError:
            print_cross_message('SIAB_ID must be set!', leave=True)
        try:
            self.cloud = os.environ['SIAB_CLOUD']
        except KeyError:
            print_cross_message('SIAB_CLOUD must be set!', leave=True)
        try:
            self.location = os.environ['SIAB_LOCATION']
        except KeyError:
            print_cross_message('SIAB_LOCATION must be set!', leave=True)
        try:
            self.context = os.environ['SIAB_CONTEXT']
        except KeyError:
            print_cross_message('SIAB_CONTEXT must be set!', leave=True)

        try:
            os.environ['VAULT_ADDR']
        except KeyError:
            print_cross_message('VAULT_ADDR must be set!', leave=True)
        try:
            os.environ['VAULT_TOKEN']
        except KeyError:
            print_cross_message('VAULT_TOKEN must be set!', leave=True)

        self.display()

    def display(self) -> None:
        if self.updated:
            message = f'- Updated client ({self.id} {self.cloud} {self.location} {self.context}) {self.version}'
            click.secho(message, fg='yellow')
        else:
            message = f'- Running client ({self.id} {self.cloud} {self.location} {self.context}) {self.version}'
            click.secho(message, fg='blue')

    def validate(self, data: dict) -> None:
        if self.id != data['client-id']:
            print_cross_message(f'Client out of sync error {self.id}!', leave=True)
        if self.cloud != data['client-cloud']:
            print_cross_message(f'Client out of sync error {self.cloud}!', leave=True)
        if self.location != data['client-location']:
            print_cross_message(f'Client out of sync error {self.location}!', leave=True)
        if self.context != data['client-context']:
            print_cross_message(f'Client out of sync error {self.context}!', leave=True)
        self.display()

    def update(self, data: dict) -> None:
        self.id = data['client-id']
        self.cloud = data['client-cloud']
        self.location = data['client-location']
        self.context = data['client-context']
        self.updated = True
        self.display()
