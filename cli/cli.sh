setup() {
  az login --use-device-code
}

regions() {
  az account list-locations --query "[].{DisplayName:displayName, Name:name}"
}

$@
