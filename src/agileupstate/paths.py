from os.path import join


def operator_path(config) -> str:
    return join(config['iac_path'], config['provisioner_data']['architecture']['agileup-operator'])


def stack_path(iac, iac_path) -> str:
    return join(iac_path, 'src', 'cloud', 'terraform', 'aws', 'stacks', iac)
