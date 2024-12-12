# Azure Synapse Analytics
aka. Azure SQL Data Warehouse

## Dedicated SQL pools
- Jobs used to load data must maintain uniqueness and referential integrity by themselves (like bq)
  - It does not support *foreign key*
  - `PRIMARY KEY` is only supported when `NONCLUSTERED` and `NOT ENFORCED` are both used.
  - `UNIQUE` constraint is only supported when `NOT ENFORCED` is used.
