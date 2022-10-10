# agileupstate

Python 3.8+ project to manage AgileUP pipeline states with the following features:

* Linux and Windows compatible project.
* Defines state model.
* Saves and fetches states from vault.
* Exports private key for Linux SSH connections.
* Exports client PKI data for Windows WinRM connections.
* Exports cloud init zip file for mTLS connection data to Windows WinRM hosts.
* Exports ansible inventories for both Linux(SSH) and Windows(WinRM) connections.
* Provides simple connectivity tests.

## Prerequisites

This project uses poetry is a tool for dependency management and packaging in Python. It allows you to declare the 
libraries your project depends on, it will manage (install/update) them for you. 

Use the installer rather than pip [installing-with-the-official-installer](https://python-poetry.org/docs/master/#installing-with-the-official-installer).

```sh
poetry self add poetry-bumpversion
```

```sh
poetry -V
Poetry (version 1.2.0)
```

### Windows Path

Install poetry from powershell in admin mode.

```shell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

The path will be `C:\Users\<YOURUSER>\AppData\Roaming\Python\Scripts\poetry.exe` which you will need to add to your system path.

### Windows GitBash

When using gitbash you can setup an alias for the poetry command:

```shell
alias poetry="\"C:\Users\<YOURUSER>\AppData\Roaming\Python\Scripts\poetry.exe\""
```

## Getting Started

```sh
poetry update
```

```sh
poetry install
```

## Development

This project uses the [hvac](https://github.com/hvac/hvac) python module and to develop locally you can run vault
as a docker service as detailed here [local docker vault](https://hub.docker.com/_/vault). For local development vault 
setup follow the [VAULT](VAULT.md) guide for information.

Check your connection with the following command, note in development mode vault should not be sealed.

```shell
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='8d02106e-b1cd-4fa5-911b-5b4e669ad07a'

poetry run agileupstate check
```

## States

* The state values are exported to `siab-state.yml`.
* The dynamic state names used by terraform are exported to file `siab-state-names.sh` and should be sourced in the pipelines for correct use.
* The tarraform state file is exported as `terraform.tfstate`.

## Cloud Init

```shell
poetry run agileupstate cloud-init --server-path=siab-pfx/ags-w-arm1.meltingturret.io.pfx --client-path=siab-pfx/devops@meltingturret.io.pfx
```

## Ansible Inventory

The ansible `inventory.txt` file is generated from the state data and the format automatically supports both SSH and 
WinRM connections. It is assumed that terraform does not output `['vm-rsa-private-key']` for Windows hosts which is used to determine 
the difference ebtween SSH or WinRM type inventory.txt file, example of WinRM file:

Example SSH `inventory.txt`
```ini
[001_arm_uksouth_dev]
20.77.124.22 ansible_ssh_private_key_file=vm-rsa-private-key.pem
```

Example WinRM `inventory.txt`
```ini
[001_arm_uksouth_dev]
20.108.1.34
[001_arm_uksouth_dev:vars]
ansible_user=azureuser
ansible_password=heTgDg!J4buAv5kc
ansible_connection=winrm
ansible_port=5986
ansible_winrm_ca_trust_path=chain.meltingturret.io.pem
ansible_winrm_cert_pem=devops@meltingturret.io.pem
ansible_winrm_cert_key_pem=devops@meltingturret.io.key
ansible_winrm_transport=certificate
```

## Run
```sh
poetry run agileupstate
```

## Lint
```sh
poetry run flake8
```

## Test
```sh
poetry run pytest
```

## Publish

* By default we are using [PYPI packages](https://packaging.python.org/en/latest/tutorials/installing-packages/). 
* Create yourself an access token for PYPI and then follow the instructions.

```sh
export PYPI_USERNAME=__token__ 
export PYPI_PASSWORD=<Your API Token>
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Agile-Solutions-GB-Ltd/agileup/tags). 

## Releasing

We are using [poetry-bumpversion](https://github.com/monim67/poetry-bumpversion) to manage release versions.

```sh
poetry version patch
```

## Dependency

Once the release has been created it is now available for you to use in other python projects via:

```sh
pip install agileupstate
```

And also for poetry projects via:

```sh
poetry add agileupstate
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details



