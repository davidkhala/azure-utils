context() {
  az account show "$@"
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
get-access-token() {
  az account get-access-token --resource https://management.core.windows.net/ -o tsv --query accessToken "$@"
}

"$@"
