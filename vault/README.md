# Vault

## Permission
Please ensure your key vault is using modern Azure RBAC `Access control (IAM)` instead of `Key Vault access policy`
- Azure portal page of a key vault > **Settings / Access configuration** > **Permission model**
- **Contributor** role has no permission to manage secrets. You need **Key Vault Administrator** assignment
- > [The Azure role-based access control permission model is not currently supported with Azure Databricks.](https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes)
