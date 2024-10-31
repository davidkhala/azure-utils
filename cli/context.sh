context() {
  az account show $@
}
tenant() {
  context --query tenantId --output tsv
}
whoami() {
  context --query user.name --output tsv
}
subscription() {
  context --query id --output tsv
}

$@
