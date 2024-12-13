
# type: Clustered columnstore index
- The **default** storage structure (index) type
- usecase: high data compression and query performance on large tables
# type: Clustered index
Clustered indexes sort and store the data rows in the table based on their key values.
- only 1 Clustered index per table
# type: heap
- usecase: loading transient data, such as a staging table
