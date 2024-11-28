[Acount Console](https://accounts.azuredatabricks.net)
- [Catalog admin page](https://accounts.azuredatabricks.net/data) allow user to manage **Metastore Admin**
- The Entra ID signed in must has `Global Administrator` role, to have access more than just go to workspace.

You cannot move Azure Databricks across Resource Group
> Resource move is not supported for resource types 'Microsoft.Databricks/workspaces'

# Cluster
[serverless compute beyond SQL warehouse](https://github.com/davidkhala/spark/blob/main/databricks/compute/serverless.md) is disabled by default

## job compute

## All-purpose compute
交互式工作负载通常在Azure Databricks notebook中运行命令

## SQL Warehouses


# Managed Resource Group
[Managed resource group is a special Azure Resource Group that holds ancillary resources created by Azure Synapse Analytics/Azure Databricks for your workspace.](https://learn.microsoft.com/en-us/answers/questions/762405/synapseworkspace-managedrg-and-databricks-rg)
- By default, it is created for you when your workspace is created. It will be named as `databricks-rg-$WorspaceName-$randomNumber`.
- It is visible as a normal Azure Resource Group
- Immutable: it is not modifiable.
    - To alter permissions on the managed resource group you need to **open a support ticket**
