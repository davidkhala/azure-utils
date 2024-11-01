
# Cluster

Cluster Mode：集群的模式共有三种，High concurrency（高并发）、Standard（标准，推荐模式）和Single Node（单节点）

# Workload
Azure Databricks的工作负载(workload)分为两个类型
## data engineering (job)

## data analytics (all-purpose)
交互式工作负载通常在Azure Databricks notebook中运行命令

# Managed resource group
[Managed resource group is a container that holds ancillary resources created by Azure Synapse Analytics/Azure Databricks for your workspace.](https://learn.microsoft.com/en-us/answers/questions/762405/synapseworkspace-managedrg-and-databricks-rg)
- By default, it is created for you when your workspace is created. It will be named as `databricks-rg-$WorspaceName-$RandomNumber`.
- Immutable: it is not modifiable.
    - To alter permissions on the managed resource group you need to **open a support ticket**