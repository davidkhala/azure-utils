# Serverless compute

[serverless compute beyond SQL warehouse](https://github.com/davidkhala/spark/blob/main/databricks/compute/serverless.md) is disabled by default

- [Doc: Feature enablement](https://docs.databricks.com/en/admin/workspace-settings/serverless.html)
- how-to enable: go to [Acount Console](https://accounts.azuredatabricks.net) > `Settings` in left panel > **Feature enablement** > enable **Serverless compute for Workflows, Notebooks, and Delta Live tables**

## network
> serverless compute resources do not have public IP addresses.

# classic compute


## Network

### VNet injection
The VNet must include 2 designated subnets
- container subnet (aka private subnet)
- host subnet (aka public subnet)

### [Secure Cluster Connectivity (SCC)](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/secure-cluster-connectivity)
- aka. no public IP (NPIP)
    - customer virtual networks have no open ports
    - compute resources in the classic compute plane have no public IP addresses.
- Is a relay tunnel
    - Each cluster initiates a connection to the control plane SCC relay during cluster creation.
- Enablement on workspace level
### [Azure Databricks Private Link](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/private-link)
VPN: provides private connectivity from Azure VNets to Azure services without public network traffic
- *users to workspace* (aka *Front-end Private Link*):
    - if clients have no public internet connectivity, use **Browser authentication private endpoint** additionally
        - for SSO login callbacks to Azure Databricks web app from Entra ID.
- *compute plane to control plane* (aka *Back-end Private Link*):
    - This enables private connectivity from the clusters to the SCC relay endpoint and REST API endpoint
    - If enabled, Sample Unity Catalog datasets and Azure Databricks datasets are not available