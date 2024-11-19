az config set extension.dynamic_install_allow_preview=true
login() {
  az login --use-device-code
}

regions() {
  az account list-locations --query "[].{DisplayName:displayName, Name:name}"
}

$@
