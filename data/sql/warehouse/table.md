# star schema design
https://learn.microsoft.com/en-us/training/modules/design-multidimensional-schema-to-optimize-analytical-workloads/3-create-tables


# distributed tables
[Dedicated SQL pool supports three methods for distributing data](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute#what-is-a-distributed-table):
- hash
  - improves query performance (by minimize data movement during queries)
  - Design required: Choosing a good distribution columns (as partition columns)
  - more data skew
  - Use case: for large  (>2GB) fact tables with heavy write (insert, update and delete) operations
- round-robin: the default method
  - improving loading speed
  - distributes table rows evenly across all distributions.
    - **random**: rows with equal values are not guaranteed to be assigned to the same distribution.
  - joining a round-robin table usually requires reshuffling the rows (invoke data movement to resolve a query)
  - Use case:
    - No obvious joining key or candidate distribution columns for adopting hash table
    - a temporary staging table

- replicated: for small dimension table
## Design distribution columns in hash table
- select up to 8 columns
- Once setup, you cannot change it
  - Solution: use CREATE TABLE AS SELECT (CTAS) to re-create the table with the updated distribution hash key.
