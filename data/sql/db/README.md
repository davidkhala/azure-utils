# Azure SQL Database

- [Move across regions](https://learn.microsoft.com/en-us/azure/resource-mover/tutorial-move-region-sql#assign-a-target-sql-server)

## Access

### Network
in SQL server layer, left panal > Security > Networking
- There is no such option to allow all Public network access
   - Alternatively, you can add a special firewall rules to do that
   - **Start IPv4 address**: 0.0.0.0
   - **End IPv4 address**: 255.255.255.255
