import unittest

from davidkhala.azure.ci import credentials
from davidkhala.azure.storage.blob import Client as BlobClient


class BlobTest(unittest.TestCase):
    def setUp(self):
        account_name = 'davidkhala'
        self.blob = BlobClient(account_name, credential=credentials())

    def test_connect(self):
        self.assertTrue(self.blob.connect())


if __name__ == '__main__':
    unittest.main()
