# Azure SQL Database


## cross region copy
- [Move across regions](https://learn.microsoft.com/en-us/azure/resource-mover/tutorial-move-region-sql#move-sql-server)
- [Copy](https://learn.microsoft.com/en-us/azure/azure-sql/database/database-copy?view=azuresql&tabs=azure-powershell) can duplicate current status to another region
- `Data management > Replicas`
## Access

### Network
in SQL server layer, left panal > Security > Networking
- There is no such option to allow all Public network access
   - Alternatively, you can add a special firewall rules to do that
   - **Start IPv4 address**: 0.0.0.0
   - **End IPv4 address**: 255.255.255.255

## SQL elastic pool
