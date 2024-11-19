set -e
echo y | az purview -h >/dev/null
desc() {
  local tenantId=$(az account show --query tenantId --output tsv)
  az purview default-account show --scope-type "Tenant" --scope-tenant-id $tenantId $@
}
name() {
  desc --query accountName --output tsv
}
$@
