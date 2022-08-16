setup() {
  az login --use-device-code
}
ping() {
  az account list
}
create-service-principal(){
  az ad sp create-for-rbac --name $1 --role Contributor --scopes /subscriptions/d02180af-0630-4747-ab1b-0d3b3c12dafb
}


$@
