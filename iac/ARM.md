# Azure Resource Manager templates (ARM templates)


## Powershell
Deployment Scoped based cmd. To deploy to a
- resource group, use `New-AzResourceGroupDeployment`:
- subscription, use `New-AzSubscriptionDeployment` (alias `New-AzDeployment`)
- tenant, use `New-AzTenantDeployment`
- management group, use `New-AzManagementGroupDeployment`.

