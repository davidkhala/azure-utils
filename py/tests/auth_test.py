import os
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
            self.assertIsInstance(credential, expected_type)
            self.assertIsInstance(credential, TokenCredential)
            if i==0:
                self.assertIsInstance(credential, EnvironmentCredential)
            elif i==1:
                self.assertIsInstance(credential, ManagedIdentityCredential)
            elif i==2:
                self.assertIsInstance(credential, SharedTokenCacheCredential)
            elif i==3:
                self.assertIsInstance(credential, AzureCliCredential)
            elif i==4:
                self.assertIsInstance(credential, AzurePowerShellCredential)
            elif i==5:
                self.assertIsInstance(credential, AzureDeveloperCliCredential)

    def test_from_env(self):
        ci= from_service_principal(
            tenant_id='c2a38aca-e9c7-4647-8dcd-9185476159ae',
            client_id='fa318cde-43db-40a5-a372-5159113bf7d8',
            client_secret=os.environ.get('CLIENT_SECRET'),
        )
        # validate
        ci.get_token()



if __name__ == '__main__':
    unittest.main()
