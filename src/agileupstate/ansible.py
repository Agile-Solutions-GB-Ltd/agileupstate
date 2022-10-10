import os

import click
import winrm

from agileupstate.state import State
from agileupstate.terminal import print_cross_message, print_check_message

PRIVATE_KEY_PEM = 'vm-rsa-private-key.pem'
INVENTORY = 'inventory.txt'


def opener(path, flags):
    return os.open(path, flags, 0o600)


def reset_linux(state: State):
    if os.path.isfile(INVENTORY):
        os.remove(INVENTORY)
    with open(INVENTORY, 'w') as f:
        f.write('[' + state.state_name_underscore + ']\n')


def reset_windows(state: State):
    if os.path.isfile(INVENTORY):
        os.remove(INVENTORY)
    with open(INVENTORY, 'w') as f:
        f.write('[' + state.state_name_underscore + ']\n')


def windows_bottom(state: State, username, password, client):
    ca_trust_path, cert_pem, cert_key_pem = client
    with open(INVENTORY, 'a') as f:
        f.write('[' + f'{state.state_name_underscore}:vars' + ']\n')
        f.write(f'ansible_user={username}' + '\n')
        f.write(f'ansible_password={password}' + '\n')
        f.write('ansible_connection=winrm' + '\n')
        f.write('ansible_port=5986' + '\n')
        f.write(f'ansible_winrm_ca_trust_path={ca_trust_path}' + '\n')
        f.write(f'ansible_winrm_cert_pem={cert_pem}' + '\n')
        f.write(f'ansible_winrm_cert_key_pem={cert_key_pem}' + '\n')
        f.write('ansible_winrm_transport=certificate' + '\n')


def create_inventory(state: State, tfstate_content, client=None):
    ips = tfstate_content['outputs']['public_ip_address']['value']
    if ips is None:
        print_cross_message('Expected public_ip_address is output!', leave=True)

    try:
        key = tfstate_content['outputs']['vm-rsa-private-key']['value']
        print_check_message(f'Creating Linux inventory for {ips}')
        os.umask(0)
        click.secho(f'- Writing {PRIVATE_KEY_PEM}', fg='blue')
        with open(PRIVATE_KEY_PEM, 'w', opener=opener) as f:
            f.write(key)

        reset_linux(state)
        for ip in ips:
            with open(INVENTORY, 'a') as f:
                f.write(ip + f' ansible_ssh_private_key_file={PRIVATE_KEY_PEM}\n')
        click.secho(f'- Writing inventory file {INVENTORY}', fg='blue')

    except KeyError:
        print_check_message(f'Creating Windows inventory for {ips}')
        admin_username = tfstate_content['outputs']['admin_username']['value']
        admin_password = tfstate_content['outputs']['admin_password']['value']
        reset_windows(state)
        for ip in ips:
            with open(INVENTORY, 'a') as f:
                f.write(ip + '\n')
        windows_bottom(state, admin_username, admin_password, client)
        click.secho(f'- Writing inventory file {INVENTORY}', fg='blue')


def ping_windows(auth):
    session = winrm.Session('https://ags-w-arm1.meltingturret.io:5986',
                            ca_trust_path='chain.meltingturret.io.pem',
                            cert_pem='devops@meltingturret.io.pem',
                            cert_key_pem='devops@meltingturret.io.key',
                            transport='certificate', auth=auth)
    response = session.run_cmd('ipconfig', ['/all'])
    print(response.std_out)
