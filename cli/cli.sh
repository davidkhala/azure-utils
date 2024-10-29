setup() {
  az login --use-device-code
}
ping() {
  az account list
}
regions() {
  az account list-locations --query "[].{DisplayName:displayName, Name:name}"
}

$@
