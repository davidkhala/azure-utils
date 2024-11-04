set -e
create-service-principal() {
    local scopes="/subscriptions/$subscription"
    if [[ -n $rg ]]; then
        scopes="$scopes/resourceGroups/$rg"
    fi

    az ad sp create-for-rbac --name $1 --role Contributor --scopes $scopes
}
service-principal-secret-list(){
    local appId=$1 # aka. Application (client) ID. The id of service principal
    az ad app credential list --id $appId
    
}
delete-service-principal() {
    az ad sp delete --id $1
}

$@
