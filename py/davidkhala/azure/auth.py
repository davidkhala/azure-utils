# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/samples/credential_creation_code_snippets.py

from azure.identity import (
    DefaultAzureCredential, AzureCliCredential,
    EnvironmentCredential, ManagedIdentityCredential, SharedTokenCacheCredential,
    AzurePowerShellCredential, AzureDeveloperCliCredential, ClientSecretCredential,
)

from davidkhala.azure import TokenCredential

DefaultCredentialType = EnvironmentCredential | ManagedIdentityCredential | SharedTokenCacheCredential | AzureCliCredential | AzurePowerShellCredential | AzureDeveloperCliCredential
cli = AzureCliCredential
default = DefaultAzureCredential


def from_service_principal(tenant_id: str, client_id: str, client_secret: str) -> TokenCredential:
    return TokenCredential(ClientSecretCredential(tenant_id, client_id, client_secret))

# TODO Check this AI content
# from azure.identity import DefaultAzureCredential
# from azure.mgmt.resource import SubscriptionClient
#
# # Authenticate using DefaultAzureCredential
# credential = DefaultAzureCredential()
#
# # Create a SubscriptionClient to query subscription details
# subscription_client = SubscriptionClient(credential)
#
# # Get the first subscription (you can iterate through all subscriptions if needed)
# subscription = next(subscription_client.subscriptions.list())
#
# # Get the tenant ID and subscription ID
# tenant_id = subscription.tenant_id
# subscription_id = subscription.subscription_id
#
# # Get the subscription details
# subscription_details = subscription_client.subscriptions.get(subscription_id)
#
# # Print the account information
# print(f"Subscription ID: {subscription_id}")
# print(f"Tenant ID: {tenant_id}")
#
# # Check the principal type by inspecting the subscription details
# if hasattr(subscription_details, 'user'):
#     print("This is a User Principal.")
# elif hasattr(subscription_details, 'service_principal'):
#     print("This is a Service Principal.")
# else:
#     print("The principal type could not be determined.")