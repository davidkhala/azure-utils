import os
import unittest

from azure.core.credentials import TokenCredential
from azure.identity import ManagedIdentityCredential, SharedTokenCacheCredential, AzureCliCredential, \
    EnvironmentCredential, AzurePowerShellCredential, AzureDeveloperCliCredential

from davidkhala.azure import default_scopes
from davidkhala.azure.auth import default, actually, DefaultCredentialType, CliCredential
from davidkhala.azure.ci import credentials
from davidkhala.azure.subscription import Subscription


class CredentialsCase(unittest.TestCase):
    def test_default(self):
        if os.environ.get("CI") == 'true': self.skipTest("No DefaultAzureCredential in CI environment")
        d = default()

        for i, credential in enumerate(d.credentials):
            self.assertIsInstance(credential, DefaultCredentialType)
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
                    data = vars(credential)
                    # no raw credential info found
                    self.assertEqual('', data['tenant_id'])
                    self.assertIsNone(data['subscription'])
                case 4:
                    self.assertIsInstance(credential, AzurePowerShellCredential)
                case 5:
                    self.assertIsInstance(credential, AzureDeveloperCliCredential)

        d.get_token(*default_scopes)

        # test actually
        actual = list(actually(d))
        self.assertEqual(1, actual.__len__())
        self.assertIsInstance(actual[0], AzureCliCredential)

    def test_from_env(self):
        auth = credentials()
        # validate
        auth.get_token(*default_scopes)
    def test_cli(self):
        if os.environ.get("CI") == 'true': self.skipTest("No CliCredential in CI environment")
        r = CliCredential.current()
        print(r)



if __name__ == '__main__':
    unittest.main()
