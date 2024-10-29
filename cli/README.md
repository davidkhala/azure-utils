

## Example: create service principal
```

name=app
export subscription=${subscription:-"d02180af-0630-4747-ab1b-0d3b3c12dafb"}
# optional: export rg=${rg:-"root-compartment"}

curl https://raw.githubusercontent.com/davidkhala/azure-utils/refs/heads/main/cli/entra.sh | bash -s create-service-principal $name
```