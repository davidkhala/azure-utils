[wiki](https://github.com/davidkhala/azure-utils/wiki/Log)

We can now reproduce steps in [tutorial](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/tutorial-logs-ingestion-portal), but in Python 
```
Message: The authentication token provided does not have access to ingest data for the data collection rule with immutable Id 'dcr-d2784248993e4127b5be12676fc436c9'.
```
- > [give the application permission to use the DCR](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/tutorial-logs-ingestion-portal?source=recommendations#assign-permissions-to-the-dcr)
  



# Notes
- Azure Monitor workspace **IS NOT** Log Analytics workspace