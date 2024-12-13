# Data ingestion and preparation
> Instead of ETL, design ELT

[Overview](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/design-elt-data-loading?context=%2Fazure%2Fsynapse-analytics%2Fcontext%2Fcontext)
- Tools
  - classic and popular SQL Server options: `bcp` and `SqlBulkCopy` API
  - Recommended (fastest and most scalable) :
    -  PolyBase external tables
    -  `COPY` statement.
