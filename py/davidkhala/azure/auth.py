# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/samples/credential_creation_code_snippets.py

from azure.identity import (
    DefaultAzureCredential, AzureCliCredential,
    EnvironmentCredential, ManagedIdentityCredential, SharedTokenCacheCredential,
    AzurePowerShellCredential, AzureDeveloperCliCredential, ClientSecretCredential
)

DefaultCredentialType = EnvironmentCredential | ManagedIdentityCredential | SharedTokenCacheCredential | AzureCliCredential | AzurePowerShellCredential | AzureDeveloperCliCredential
cli = lambda: AzureCliCredential()
default = lambda: DefaultAzureCredential()


def from_service_principal(tenant_id: str, client_id: str, client_secret: str):
    return ClientSecretCredential(tenant_id, client_id, client_secret)
