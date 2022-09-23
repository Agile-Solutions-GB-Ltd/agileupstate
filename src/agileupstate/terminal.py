
import click

from agileupstate import EXITCODE


def print_check_message(text) -> bool:
    click.echo(b'\xE2\x9C\x94' + f' {text}'.encode())
    return True


def print_cross_message(text, leave=False) -> bool:
    click.echo(b'\xE2\x9D\x8C' + f' {text}'.encode())
    if leave:
        exit(EXITCODE)
    else:
        return True
