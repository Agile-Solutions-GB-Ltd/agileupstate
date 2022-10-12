import os

import click
import winrm

from agileupstate.state import State
from agileupstate.terminal import print_cross_message, print_check_message

PRIVATE_KEY_PEM = 'vm-rsa-private-key.pem'
INVENTORY = 'inventory.ini'


def opener(path, flags):
    return os.open(path, flags, 0o600)


def reset_linux(state: State) -> None:
    if os.path.isfile(INVENTORY):
        os.remove(INVENTORY)
    with open(INVENTORY, 'w') as f:
        f.write('[' + state.state_name_underscore + ']\n')


def reset_windows(state: State) -> None:
    if os.path.isfile(INVENTORY):
        os.remove(INVENTORY)
    with open(INVENTORY, 'w') as f:
        f.write('[' + state.state_name_underscore + ']\n')


def switch_domain_if_present(dns: str) -> str:
    try:
        override = os.environ['SIAB_DOMAIN']
        click.secho(f'- Overriding domain to {override}', fg='yellow')
        return dns.split('.')[0] + '.' + override
    except KeyError:
        return dns


def windows_bottom(state: State, username, password, pki) -> None:
    ca_trust_path, cert_pem, cert_key_pem = pki
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


def create_windows_inventory(state: State, tfstate_content, pki) -> None:
    try:
        ips = tfstate_content['outputs']['public_ip_address']['value']
        dnss = tfstate_content['outputs']['public_ip_dns_name']['value']
        admin_username = tfstate_content['outputs']['admin_username']['value']
        admin_password = tfstate_content['outputs']['admin_password']['value']
        if ips is None:
            print_cross_message('Expected public_ip_address in terraform output!', leave=True)
        if dnss is None:
            print_cross_message('Expected public_ip_dns_name in terraform output!', leave=True)
        if admin_username is None:
            print_cross_message('Expected admin_username in terraform output!', leave=True)
        if admin_password is None:
            print_cross_message('Expected admin_password in terraform output!', leave=True)
        print_check_message(f'Creating Windows inventory for {dnss}')
        reset_windows(state)
        for dns in dnss:
            with open(INVENTORY, 'a') as f:
                f.write(switch_domain_if_present(dns) + '\n')
        windows_bottom(state, admin_username, admin_password, pki)
        click.secho(f'- Writing inventory file {INVENTORY}', fg='blue')
    except KeyError as e:
        print_cross_message(f'Missing key {e}!', leave=True)


def create_linux_inventory(state: State, tfstate_content) -> None:
    try:
        ips = tfstate_content['outputs']['public_ip_address']['value']
        dnss = tfstate_content['outputs']['public_ip_dns_name']['value']
        admin_username = tfstate_content['outputs']['admin_username']['value']
        admin_password = tfstate_content['outputs']['admin_password']['value']
        if ips is None:
            print_cross_message('Expected public_ip_address in terraform output!', leave=True)
        if dnss is None:
            print_cross_message('Expected public_ip_dns_name in terraform output!', leave=True)
        if admin_username is None:
            print_cross_message('Expected admin_username in terraform output!', leave=True)
        if admin_password is None:
            print_cross_message('Expected admin_password in terraform output!', leave=True)
        print_check_message(f'Creating Windows inventory for {dnss}')
        reset_linux(state)
        for dns in dnss:
            with open(INVENTORY, 'a') as f:
                f.write(switch_domain_if_present(dns) + f' ansible_ssh_private_key_file={PRIVATE_KEY_PEM}\n')
        click.secho(f'- Writing inventory file {INVENTORY}', fg='blue')
    except KeyError as e:
        print_cross_message(f'Missing key {e}!', leave=True)


def ping_windows(auth) -> None:
    session = winrm.Session('https://ags-w-arm1.meltingturret.io:5986',
                            ca_trust_path='chain.meltingturret.io.pem',
                            cert_pem='devops@meltingturret.io.pem',
                            cert_key_pem='devops@meltingturret.io.key',
                            transport='certificate', auth=auth)
    response = session.run_cmd('ipconfig', ['/all'])
    print(response.std_out)
