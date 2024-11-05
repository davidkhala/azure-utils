set -e -x
legacy-grant() {
    # Vault access policy (legacy)
    local vault=$1        # name of key vault
    local principal_id=$2 # id of a principal
    local permission=${3:-get}

    az keyvault set-policy --name $1 --object-id $principal_id --secret-permissions $permission
}
grant() {
    local vault=$1
    local assignee=$2
    az role assignment create --role "Key Vault Secrets Officer" --assignee $assignee --scope /subscriptions/${subscription}/resourcegroups/${rg}/providers/Microsoft.KeyVault/vaults/${vault}
}
$@
