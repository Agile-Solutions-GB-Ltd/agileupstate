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

    def __init__(self):
        self.version = get_version_string()
        try:
            self.id = os.environ['SIAB_ID']
        except KeyError:
            print_cross_message(f'SIAB_ID must be set!', leave=True)
        try:
            self.cloud = os.environ['SIAB_CLOUD']
        except KeyError:
            print_cross_message(f'SIAB_CLOUD must be set!', leave=True)
        try:
            self.location = os.environ['SIAB_LOCATION']
        except KeyError:
            print_cross_message(f'SIAB_LOCATION must be set!', leave=True)
        try:
            self.context = os.environ['SIAB_CONTEXT']
        except KeyError:
            print_cross_message(f'SIAB_CONTEXT must be set!', leave=True)

        if supported_os():
            print_check_message(f'Client machine supported {platform}')
        else:
            print_cross_message(f'Client machine not supported {platform}!', leave=True)

        self.display()

    def display(self) -> str:
        message = f'- Running ({self.id} {self.cloud} {self.location} {self.context}) {self.version}'
        click.secho(message, fg='blue')
        return message
