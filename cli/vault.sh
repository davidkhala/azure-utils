set -e
grant() {
    local vault=$1 # name of key vault
    local principal=$2 # id of a principal
    local permission=${3:-get}
    
    az keyvault set-policy --name $1 --object-id $principal --secret-permissions $permission
}
$@
