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

## Required Environment State Variables

| Variable         | Description                                                     |
|------------------|-----------------------------------------------------------------|
| SIAB_ID          | Unique environment ID.                                          |
| SIAB_CLOUD       | Cloud vendor API mnemonic.                                      |
| SIAB_LOCATION1   | Cloud vendor defined cloud location, uksouth, etc.              |
| SIAB_LOCATION2   | Cloud vendor defined cloud location, UK South, etc.             |
| SIAB_CONTEXT     | Environment context, e.g. dev. test, prod.                      |
| SIAB_VALUES_PATH | Vault path to common environment values to be exported.         |
| SIAB_DOMAIN      | Optional public domain that overrides cloud provided DNS names. |

`SIAB_LOCATION`: Azure has a different location string between "accounts" and "resources" and only `uksouth` is useful
to the automation, but we must also provide `UK South` for resource groups.

`SIAB_VALUES_PATH`: Rather than load variables into the delivery platform environment, there can be many, a better option
is to define a YML file that contains all the required common variables for a specific environment and have the user upload
that to vault. This application can then download the YML data file and convert it into an exports file that can be sourced 
by the pipelines. These environment values that are exported can then be used by this project and other utilities such as
terraform, ansible and powershell.

`SIAB_DOMAIN`: Cloud DNS services might in some cases provide a DNS domain that is not the same as the public internet
domain required by the project, for example server1.uksouth.cloudapp.azure.com might optionally be server1.meltingturret.io.

`username/password`: These values are common across the environment, for example Ubuntu Azure images use a `username=azureuser`,
and so it simplifies configuration if the same credentials are used for Linux and Windows environments running in Azure for 
administration access, client administration access as well as PFX certificate files used on Windows for WinRM certificate 
authentication. For AWS `ubuntu` is the username for Ubuntu images the same approach can be taken there.

**Required environment inputs:**

> These values should be setup in your CD platforms environment variables.

```shell
export SIAB_ID=001
export SIAB_CLOUD=arm
export SIAB_LOCATION1=uksouth
export SIAB_LOCATION2="UK South"
export SIAB_CONTEXT=dev
export SIAB_VALUES_PATH=siab-state/001-arm-uksouth-dev/siab-values/siab-values.yml
```

**Required values inputs (stored in vault path `SIAB_VALUES_PATH`):**

```yaml
connection:
  url: https://server1.meltingturret.io:5986
  username: azureuser
  password: mypassword
  ca_trust_path: siab-client/chain.meltingturret.io.pem
  cert_pem: siab-client/azureuser@meltingturret.io.pem
  cert_key_pem: siab-client/azureuser@meltingturret.io.key
cloud:
  group_owner: Paul Gilligan
  group_department: DevOps
  group_location: UK South
```

## Required Supporting Data

Some data is generated only once and thus can be uploaded to vault manually. 

**Uploading values file:**

```shell
base64 ./siab-values.yml | vault kv put secret/siab-state/001-arm-uksouth-dev/siab-values/siab-values.yml file=-
```

**Uploading pfx files:**

```shell
base64 ./server1.meltingturret.io.pfx | vault kv put secret/siab-pfx/server1.meltingturret.io.pfx file=-
base64 ./azureuser@meltingturret.io.pfx | vault kv put secret/siab-pfx/azureuser@meltingturret.io.pfx file=-
```

**Uploading pki files:**

```shell
base64 ./chain.meltingturret.io.pem | vault kv put secret/siab-client/chain.meltingturret.io.pem file=-
base64 ./azureuser@meltingturret.io.key | vault kv put secret/siab-client/azureuser@meltingturret.io.key file=-
base64 ./azureuser@meltingturret.io.pem | vault kv put secret/siab-client/azureuser@meltingturret.io.pem file=-
```

## Exports

The `yml` file from `SIAB_VALUES_PATH` is exported to the file `siab-state-export.sh` with the contents as shown in the 
example below which can then be used by downstream utilities. 

```shell
export SIAB_URL=https://server1.meltingturret.io:5986
export SIAB_USERNAME=azureuser
export SIAB_PASSWORD=mypassword
export SIAB_CA_TRUST_PATH=siab-client/chain.meltingturret.io.pem
export SIAB_CERT_PEM=siab-client/azureuser@meltingturret.io.pem
export SIAB_CERT_KEY_PEM=siab-client/azureuser@meltingturret.io.key
export TF_VAR_group_owner=Paul Gilligan
export TF_VAR_group_department=DevOps
export TF_VAR_group_location=UK South
export TF_VAR_siab_name=001-arm-uksouth-dev
export TF_VAR_siab_name_underscore=001_arm_uksouth_dev
```

```shell
source ./siab-state-export.sh
```

## Cloud Init Data Use Case

Example cloud init command that generates the zip file that is loaded onto Windows machines for WimRM certificate authentication. 

```shell
poetry run agileupstate cloud-init --server-path=siab-pfx/ags-w-arm1.meltingturret.io.pfx --client-path=siab-pfx/azureuser@meltingturret.io.pfx
```

## Ansible Windows Inventory Use Case

`inventory.ini` is generated with the target(s) and configuration information for a successful SSH connection from Ansible. 

**When `export SIAB_DOMAIN=meltingturret.io`:**

```ini
[001_arm_uksouth_dev]
ags-w-arm1.meltingturret.io
[001_arm_uksouth_dev:vars]
ansible_user=azureuser
ansible_password=heTgDg!J4buAv5kc
ansible_connection=winrm
ansible_port=5986
ansible_winrm_ca_trust_path=chain.meltingturret.io.pem
ansible_winrm_cert_pem=azureuser@meltingturret.io.pem
ansible_winrm_cert_key_pem=azureuser@meltingturret.io.key
ansible_winrm_transport=certificate
```

## Ansible Linux Inventory Use Case

`inventory.ini` is generated with the target(s) and configuration information for a successful SSH connection from Ansible. 

**When `export SIAB_DOMAIN=meltingturret.io`:**

```ini
[001_arm_uksouth_dev]
ags-w-arm1.meltingturret.io ansible_ssh_private_key_file=vm-rsa-private-key.pem
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



