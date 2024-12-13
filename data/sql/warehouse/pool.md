# dedicated SQL pools

- Jobs used to load data must maintain uniqueness and referential integrity by themselves (like bq)
  - [Table constraints](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-table-constraints#table-constraints)
  - It does not support *foreign key*
  - `PRIMARY KEY` is only supported when `NONCLUSTERED` and `NOT ENFORCED` are both used.
  - `UNIQUE` constraint is only supported when `NOT ENFORCED` is used.
- use [MPP](https://github.com/davidkhala/As-Architect/blob/main/concepts/tech/MPP.md) architecture
