create(){
  local name=$1
  az sshkey create --name $name 2>&1 | sed -n '2 p'
}
delete(){
  local name=$1
  az sshkey create --name $name
}



$@
