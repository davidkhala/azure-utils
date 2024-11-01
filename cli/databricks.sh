echo y | az databricks -h >/dev/null

show() {
    local ADB_WS_NAME=$1 # Azure Databricks workspace name
    az databricks workspace show --resource-group $rg --name $ADB_WS_NAME $@
}
create() {
    local ADB_WS_NAME=$1 # Azure Databricks workspace name
    az databricks workspace create --name $ADB_WS_NAME --resource-group $rg --sku standard $@
    sleep 60
}
get-access-token() {
    az account get-access-token --resource 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d -o tsv --query accessToken $@
}

$@
