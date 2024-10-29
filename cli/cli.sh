setup() {
  az login --use-device-code
}
ping() {
  az account list
}
create-service-principal() {
  local scopes="/subscriptions/$subscription"
  if [[ -n $rg ]]; then
    scopes="$scopes/resourceGroups/$rg"
  fi

  az ad sp create-for-rbac --name $1 --role Contributor --scopes $scopes
}
regions() {
  az account list-locations --query "[].{DisplayName:displayName, Name:name}"
}

$@
