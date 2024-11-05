set -e
create() {
    local scopes="/subscriptions/$subscription"
    if [[ -n $rg ]]; then
        scopes="$scopes/resourceGroups/$rg"
    fi

    az ad sp create-for-rbac --name $1 --role Contributor --scopes $scopes
}
list-secret() {
    local appId=$1 # aka. Application (client) ID. The id of service principal
    az ad app credential list --id $appId

}
delete() {
    az ad sp delete --id $1
}
list-managed-identity() {
    az ad sp list --all --filter "servicePrincipalType eq 'ManagedIdentity'"
}
show() {
    local name=$1
    shift 1
    az ad sp list --display-name $name $@
}
$@
