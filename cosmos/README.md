# Azure Cosmos DB

container for dev
- https://github.com/Azure/azure-cosmos-db-emulator-docker
## No Converged API
provides five APIs. **You must create a separate account for each API.**
- [NoSQL](./nosql/README.md) for document databases
- Gremlin for graph databases
- MongoDB for document databases
- Azure Table
- Cassandra.

# Connect

## Connectivity modes: connectionless or not
Connectionless: gateway mode (default)
> Azure Cosmos DB requests are made over HTTPS/REST when you use gateway mode.
- They're subjected to the connection limit(100 to 1000) per hostname or IP address.
- supported on all language SDK


Direct mode
> The Azure Cosmos DB documentation recommends that you [use a singleton Azure Cosmos DB client for the lifetime of your application](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/performance-tips?tabs=trace-net-core#sdk-usage).
- lower latency with fewer network hops
- only supported on .NET and Java SDK


