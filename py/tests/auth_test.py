import os
import unittest
from typing import cast

from azure.core.credentials import TokenCredential
from azure.identity import ManagedIdentityCredential, SharedTokenCacheCredential, AzureCliCredential, \
    EnvironmentCredential, AzurePowerShellCredential, AzureDeveloperCliCredential

from davidkhala.azure import default_scopes
from davidkhala.azure.auth import default, actually
from davidkhala.azure.ci import credentials
from davidkhala.azure.subscription import Subscription


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
        if os.environ.get("CI") is None:
            d.get_token(*default_scopes)

    def test_actual_of_default(self):
        d = default()

        for credential, i in actually(d):
            # no raw credential info found
            data = vars(credential)
            if isinstance(credential, AzureCliCredential):
                self.assertEqual(3, i)
                self.assertEqual('', data['tenant_id'])
                self.assertIsNone(data['subscription'])

    def test_from_env(self):
        auth = credentials()
        # validate
        auth.get_token(*default_scopes)


class SubscriptionTestCase(unittest.TestCase):
    def test_default(self):
        if os.environ.get("CI") == 'true': self.skipTest("in CI environment")
        d = default()
        sub = Subscription(d)

        print(sub.get_one())


if __name__ == '__main__':
    unittest.main()
