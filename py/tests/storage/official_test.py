import unittest

from pandas import DataFrame

from davidkhala.azure.ci import credentials
from davidkhala.azure.storage.blob import Client as BlobClient


class BlobTest(unittest.TestCase):
    def setUp(self):
        account_name = 'davidkhala'
        self.service = BlobClient(account_name, credential=credentials())

    def test_connect(self):
        self.assertTrue(self.service.connect())
    def test_upload(self):
        df = DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        from davidkhala.data.integration.source.pandas import toArrow
        from davidkhala.data.integration.sink.arrow import bytesFrom
        table = toArrow(df)
        _bytes = bytesFrom(table)
        container = 'data'
        blob_path = 'test.parquet'
        blob = self.service.blob(container, blob_path)
        blob.upload(_bytes)


if __name__ == '__main__':
    unittest.main()
