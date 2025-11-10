[Acount Console](https://accounts.azuredatabricks.net)

You cannot move Azure Databricks across Resource Group
> Resource move is not supported for resource types 'Microsoft.Databricks/workspaces'

# Managed Resource Group

[Managed resource group is a special Azure Resource Group that holds ancillary resources created by Azure Synapse Analytics/Azure Databricks for your workspace.](https://learn.microsoft.com/en-us/answers/questions/762405/synapseworkspace-managedrg-and-databricks-rg)

- By default, it is created for you when your workspace is created. It will be named as `databricks-rg-$WorspaceName-$randomNumber`.
- It is visible as a normal Azure Resource Group
- Immutable: it is not modifiable.
  - To alter permissions on the managed resource group you need to **open a support ticket**
- The NAT gateway inside it is billable and will cost your $33.5 each month silently
  - This gateway provision is due to opt-in "Deploy Azure Databricks workspace with Secure Cluster Connectivity (No Public IP)" (enableNoPublicIp=true)
