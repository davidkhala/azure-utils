create(){
  local name=$1
  az sshkey create --name $name 2>&1 | sed -n '2 p' | awk -F、" '{print $2}'
  
}
delete(){
  local name=$1
  az sshkey create --name $name
}



$@
