# Vault Development

## Install Vault Binary

https://www.vaultproject.io/downloads

```shell
export DIST="focal"
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $DIST main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault
```

## Localhost Vault

Using a random GUID for the root token of our in memory docker, e.g. `8d02106e-b1cd-4fa5-911b-5b4e669ad07a`.

```sh
docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=8d02106e-b1cd-4fa5-911b-5b4e669ad07a' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' -p8200:8200 vault
```

```sh
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='8d02106e-b1cd-4fa5-911b-5b4e669ad07a'
```


