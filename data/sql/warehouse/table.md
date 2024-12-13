# Design tables

[Overview](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/develop-tables-overview)

- [star schema design](https://learn.microsoft.com/en-us/training/modules/design-multidimensional-schema-to-optimize-analytical-workloads/3-create-tables)

# distributed tables

Partitioning and Distributing are different concepts
- TODO

[Dedicated SQL pool supports three methods for distributing data](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute#what-is-a-distributed-table):

- hash
  - improves query performance (by minimize data movement during queries)
  - Design required: Choosing a good distribution columns
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

In joining these columns, to avoid data movement

- The data types of the join columns must match
- joined with `=` (equals operator)
- cannot be a `CROSS JOIN`.

Manage Data Skew

- [wiki: Data Skew](https://github.com/davidkhala/data-warehouse/wiki/Data-Skew)
- [Detect data skew](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute#determine-if-the-table-has-data-skew)
- Solution: to avoid data skiew, the distribution columns should
  - Has many unique values
    - Does not have NULLs, or has only a few NULLs.
  - Not not be a date column
    - If several users are all filtering on today's date, then only single distribution does all the processing work.
  - Be used in `JOIN`, `GROUP BY`, `DISTINCT`, `OVER`, and `HAVING` clauses
  - Not be used in `WHERE` clause

Limit

- Once setup in table create, you cannot change distribution columns (e.g. to resolve data skew)
  - Solution: use CREATE TABLE AS SELECT (CTAS) to re-create the table with the updated distribution hash key.
- Select up to 8 distribution columns

# External Table

- `ALTER` statement is not allowed on external tables
