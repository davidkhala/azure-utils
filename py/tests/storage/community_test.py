import os
import unittest

from pandas import DataFrame

from davidkhala.azure.storage.community import FS


class ADLFSTest(unittest.TestCase):
    def setUp(self):
        account_name = 'davidkhala'
        key1 = os.environ.get('key1')
        self.fs = FS(account_name, key1)
    def test_connect(self):
        self.assertTrue(self.fs.connect())
    def test_upload(self):
        df = DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        from davidkhala.data.integration.to.arrow import fromPandas, bytesFrom
        table = fromPandas(df)
        _bytes = bytesFrom(table)
        container = 'data'
        blob_path = 'test.parquet'
        with self.fs.blob_fs.open(f"{container}/{blob_path}", "wb") as f:
            f.write(_bytes)


if __name__ == '__main__':
    unittest.main()