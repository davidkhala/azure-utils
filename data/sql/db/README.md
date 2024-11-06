# Azure SQL Database


## cross region copy
- [Move across regions](https://learn.microsoft.com/en-us/azure/resource-mover/tutorial-move-region-sql#move-sql-server)
- [Copy](https://learn.microsoft.com/en-us/azure/azure-sql/database/database-copy?view=azuresql&tabs=azure-powershell) can duplicate current status to another region
- `Data management > Replicas`
  - Not available for free tier

## Access

### Network
in SQL server layer, left panal > Security > Networking
- There is no such option to allow all Public network access
   - Alternatively, you can add a special firewall rules to do that
   - **Start IPv4 address**: 0.0.0.0
   - **End IPv4 address**: 255.255.255.255

## SQL elastic pool



## Troubleshoot
**`Failed to execute query. Error: Cannot drop the credential ... because it is being used.` happened when `DROP DATABASE SCOPED CREDENTIAL "..."`**
It will happen when you 
1. create a Geo Replica active-standby cluster
2. connect with Purview SAMI with the primary
3. stop replica and terimiante the standby db
4. terminate the purview instance
- We should clean up the credential before step 3. 
