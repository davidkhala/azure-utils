# Azure Synapse Analytics
aka. [Azure SQL Data Warehouse](https://azure.microsoft.com/en-us/blog/azure-sql-data-warehouse-is-now-azure-synapse-analytics/?msockid=0856cf962dec6dc43723dad52ca96ca4)

## Dedicated SQL pools
[confusion clarification: Dedicated SQL pools exist in two different modalities](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/overview-difference-between-formerly-sql-dw-workspace#dedicated-sql-pools-exist-in-two-different-modalities)

> Not all features of the dedicated SQL pool (new provision) in Azure Synapse workspaces apply to dedicated SQL pool (formerly SQL DW), and vice versa
- They are same only when Azure Synapse workspaces is provisioned by `Migration of a dedicated SQL pool (formerly SQL DW)`
### dedicated SQL pools (formerly SQL DW)
> Circa 2016, Microsoft adapted its massively parallel processing (MPP) on-premises appliance to the cloud as "Azure SQL Data Warehouse" or "SQL DW" for short.
- "SQL DW" is short for "Azure SQL Data Warehouse"
- "SQL DW" adopted the constructs of Azure SQL DB such as a logical server. "SQL DW" could exist on the same server as other SQL DBs.
  - made it easy for current Azure SQL DBA to apply the same concepts to data warehouse.
- > "SQL DW" was rebranded as "Dedicated SQL pool (formerly SQL DW)" with intention to create clear indication that the former SQL DW is in fact the same artifact that lives within Synapse Analytics.
- "Dedicated SQL pool (formerly SQL DW)" is referred to as "standalone dedicated SQL pool".
### dedicated SQL pools in Synapse workspaces.
> The original "SQL DW" component is just one part of this (Synapse workspaces). It became known as a dedicated SQL pool.

But 
> (existing) Azure SQL DW instances weren't automatically upgraded to Synapse Analytics workspaces.
- `Migration of a dedicated SQL pool (formerly SQL DW)` the Azure portal **isn't** quite a full migration.
  - In a migration, the dedicated SQL pool (formerly SQL DW) never really is migrated.
  - It stays on the logical server it was originally on.
    - The server DNS server-123.database.windows.net never becomes server-123.sql.azuresynapse.net.
  - The migration create connection to a Synapse workspace
