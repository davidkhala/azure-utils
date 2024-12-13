# Data ingestion and preparation
> Instead of ETL, design ELT

[Overview](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/design-elt-data-loading?context=%2Fazure%2Fsynapse-analytics%2Fcontext%2Fcontext)
- Tools
  - classic and popular SQL Server options: `bcp` and `SqlBulkCopy` API
  - Recommended (fastest and scalable) :
    -  [PolyBase external tables](https://github.com/davidkhala/database/blob/main/mssql/polybase.md)
    -  `COPY` statement (recommend for most flexibility in loading)
- File Format
  - For fastest load
    - use compressed delimited text files
    - Split large compressed files into smaller compressed files
    - into heap table (without index)
  - For export data
    - when into an ORC File Format, you might get Java out-of-memory errors when there are large text columns
      - Solution: export only a subset of the columns.
