import unittest
from azure.core.credentials import TokenCredential
from azure.identity import ManagedIdentityCredential, SharedTokenCacheCredential, AzureCliCredential, \
    EnvironmentCredential, AzurePowerShellCredential, AzureDeveloperCliCredential

from davidkhala.azure.auth import default, from_service_principal


class CredentialsCase(unittest.TestCase):
    def test_default(self):
        d = default()
        expected_type = EnvironmentCredential | ManagedIdentityCredential | SharedTokenCacheCredential | AzureCliCredential | AzurePowerShellCredential | AzureDeveloperCliCredential
        for i, credential in enumerate(d.credentials):
            print(i, credential)
            self.assertIsInstance(credential, expected_type)
            self.assertIsInstance(credential, TokenCredential)

    def test_from_env(self):
        # TODO get credentials from token
        ci= from_service_principal(
            tenant_id='54b02cc9-5a7b-42a5-9476-a4f0d3ab0460',
            client_id='4733fc19-291e-46b3-942d-06de7c26f7c8',
            client_secret='',
        )



if __name__ == '__main__':
    unittest.main()
