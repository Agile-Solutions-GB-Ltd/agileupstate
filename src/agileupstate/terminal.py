
import click
from fabric.operations import local

from src.agileup import EXITCODE
from src.agileup.strings import indent


def print_check_message(text) -> None:
    click.echo(b'\xE2\x9C\x94' + f' {text}'.encode())


def print_cross_message(text, leave=False) -> None:
    click.echo(b'\xE2\x9D\x8C' + f' {text}'.encode())
    if leave:
        exit(EXITCODE)


def run_command(exec_path, exec_command) -> str:
    return local(f'cd {exec_path} && {exec_command}', capture=True)


def terraform_init(config) -> None:
    exec_path = config['exec_path']
    exec_command = f"{config['terraform']} init -input=false"
    output = run_command(exec_path, exec_command)
    for line in output.splitlines():
        if 'initial' in line.lower() and 'rerun' not in line:
            click.echo(indent(line))


def terraform_plan(config) -> None:
    exec_path = config['exec_path']
    exec_command = f"{config['terraform']} plan -input=false -out={config['iac']}.tfplan"
    output = run_command(exec_path, exec_command)
    for line in output.splitlines():
        if 'No changes.' in line or 'Changes to Outputs:' in line:
            click.echo(indent(line))


def terraform_apply(config) -> None:
    exec_path = config['exec_path']
    exec_command = f"{config['terraform']} apply -input=false {config['iac']}.tfplan"
    output = run_command(exec_path, exec_command)
    for line in output.splitlines():
        if 'Apply complete!' in line:
            click.echo(indent(line))


def terraform_destroy(config) -> None:
    exec_path = config['exec_path']
    exec_command = f"{config['terraform']} destroy -auto-approve"
    output = run_command(exec_path, exec_command)
    for line in output.splitlines():
        if 'Destroy complete!' in line:
            click.echo(indent(line))
