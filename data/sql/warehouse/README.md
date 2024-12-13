# Azure Synapse Analytics
aka. [Azure SQL Data Warehouse](https://azure.microsoft.com/en-us/blog/azure-sql-data-warehouse-is-now-azure-synapse-analytics/?msockid=0856cf962dec6dc43723dad52ca96ca4)

## Dedicated SQL pools
- Jobs used to load data must maintain uniqueness and referential integrity by themselves (like bq)
  - It does not support *foreign key*
  - `PRIMARY KEY` is only supported when `NONCLUSTERED` and `NOT ENFORCED` are both used.
  - `UNIQUE` constraint is only supported when `NOT ENFORCED` is used.
- use [MPP](https://github.com/davidkhala/As-Architect/blob/main/concepts/tech/MPP.md) architecture
