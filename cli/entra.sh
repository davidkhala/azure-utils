create-service-principal() {
    local scopes="/subscriptions/$subscription"
    if [[ -n $rg ]]; then
        scopes="$scopes/resourceGroups/$rg"
    fi

    az ad sp create-for-rbac --name $1 --role Contributor --scopes $scopes --query "{appId:appId, password:password}"

}
delete-service-principal() {
    az ad sp delete --id $1
}

$@
