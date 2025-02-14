import os
import unittest
from azure.core.credentials import TokenCredential
from azure.identity import ManagedIdentityCredential, SharedTokenCacheCredential, AzureCliCredential, \
    EnvironmentCredential, AzurePowerShellCredential, AzureDeveloperCliCredential

from davidkhala.azure.auth import default, from_service_principal
from davidkhala.azure.ci import credentials


class CredentialsCase(unittest.TestCase):
    def test_default(self):
        d = default()
        expected_type = EnvironmentCredential | ManagedIdentityCredential | SharedTokenCacheCredential | AzureCliCredential | AzurePowerShellCredential | AzureDeveloperCliCredential
        for i, credential in enumerate(d.credentials):
            self.assertIsInstance(credential, expected_type)
            self.assertIsInstance(credential, TokenCredential)
            match i:
                case 0:
                    self.assertIsInstance(credential, EnvironmentCredential)
                case 1:
                    self.assertIsInstance(credential, ManagedIdentityCredential)
                case 2:
                    self.assertIsInstance(credential, SharedTokenCacheCredential)
                case 3:
                    self.assertIsInstance(credential, AzureCliCredential)
                case 4:
                    self.assertIsInstance(credential, AzurePowerShellCredential)
                case 5:
                    self.assertIsInstance(credential, AzureDeveloperCliCredential)

    def test_from_env(self):
        auth = credentials()
        # validate
        auth.get_token()


if __name__ == '__main__':
    unittest.main()
