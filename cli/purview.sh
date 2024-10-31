# install extension
install() {
  az config set extension.dynamic_install_allow_preview=true
  az upgrade
  echo y | az purview -h
}
desc() {
  local tenantId=$(az account show --query tenantId --output tsv)
  az purview default-account show --scope-type "Tenant" --scope-tenant-id $tenantId
}
name(){
  desc --query accountName --output tsv
}
$@

