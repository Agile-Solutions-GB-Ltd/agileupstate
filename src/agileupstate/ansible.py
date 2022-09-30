import os

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


def windows_bottom(state: State, username, password):
    with open(INVENTORY, 'a') as f:
        f.write('[' + f'{state.state_name_underscore}:vars' + ']\n')
        f.write('[' + f'ansible_user={username}' + ']\n')
        f.write('[' + f'ansible_password={password}' + ']\n')
        f.write('[' + 'ansible_connection=winrm' + ']\n')
        f.write('[' + 'ansible_port=5986' + ']\n')
        f.write('[' + 'ansible_winrm_server_cert_validation=ignore' + ']\n')
        f.write('[' + 'ansible_winrm_server_cert_validation=ignore' + ']\n')


def create_inventory(state: State, tfstate_content):
    ips = tfstate_content['outputs']['public_ip_address']['value']
    if ips is None:
        print_cross_message('Expected public_ip_address is output!', leave=True)

    try:
        key = tfstate_content['outputs']['vm-rsa-private-key']['value']
        print_check_message(f'Creating Linux inventory for {ips}')
        os.umask(0)
        with open(PRIVATE_KEY_PEM, 'w', opener=opener) as f:
            f.write(key)

        reset_linux(state)
        for ip in ips:
            with open(INVENTORY, 'a') as f:
                f.write(ip + f' ansible_ssh_private_key_file={PRIVATE_KEY_PEM}\n')
        print_check_message(f'Written inventory file {INVENTORY}')

    except KeyError:
        print_check_message(f'Creating Windows inventory for {ips}')
        admin_username = tfstate_content['outputs']['admin_username']['value']
        admin_password = tfstate_content['outputs']['admin_password']['value']
        reset_windows(state)
        for ip in ips:
            with open(INVENTORY, 'a') as f:
                f.write(ip + '\n')
        windows_bottom(state, admin_username, admin_password)
