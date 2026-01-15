import os
import unittest

from pandas import DataFrame

from davidkhala.azure.storage.community.blob import FS


class ADLFSTest(unittest.TestCase):
    def setUp(self):
        account_name = 'davidkhala'
        key1 = os.environ.get('key1')
        self.fs = FS(account_name, key1)
        self.container = 'data'
        self.blob_path = 'test.parquet'

    def test_connect(self):
        self.assertTrue(self.fs.connect())

    def test_upload(self):
        df = DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        from davidkhala.data.integration.source.pandas import toArrow
        from davidkhala.data.integration.sink.arrow import bytesFrom
        table = toArrow(df)
        _bytes = bytesFrom(table)

        with self.fs._.open(f"{self.container}/{self.blob_path}", "wb") as f:
            f.write(_bytes)

    def test_download(self):
        import pyarrow.parquet as pq

        with self.fs._.open(f"{self.container}/{self.blob_path}", "rb") as f:
            table = pq.read_table(f)

        df: DataFrame = table.to_pandas()
        print(df)


if __name__ == '__main__':
    unittest.main()
