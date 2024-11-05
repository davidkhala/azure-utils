# Vault

## Permission
Please ensure your key vault is using modern Azure RBAC `Access control (IAM)` instead of `Key Vault access policy`
- Azure portal page of a key vault > **Settings / Access configuration** > **Permission model**
- **Contributor** role has no permission to manage secrets. You need **Key Vault Administrator** assignment