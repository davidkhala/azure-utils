echo y | az databricks -h >/dev/null

show() {
    local ADB_WS_NAME=$1 # Azure Databricks workspace name
    az databricks workspace show --resource-group $rg --name $ADB_WS_NAME
}
$@
