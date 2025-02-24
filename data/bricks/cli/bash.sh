set -e
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
    az account get-access-token --resource 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d -o tsv --query accessToken "$@"
}
login() {
    local workspace_name=${1:-$workspace_name}
    if [[ -z $workspace_name ]]; then
        echo missing workspace_name
        exit 1
    fi
    if [[ -z $rg ]]; then
        echo "missing rg (resource group)"
        exit 1
    fi
    local global_adb_token=$(get-access-token)
    local adb_ws_url=$(az databricks workspace show --resource-group $rg --name $workspace_name --query workspaceUrl -o tsv)
    curl -s https://raw.githubusercontent.com/davidkhala/spark/refs/heads/main/databricks/cli/setup.sh | bash -s login $adb_ws_url $global_adb_token
}

$@
