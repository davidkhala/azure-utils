import os
import unittest

import pandas as pd
from davidkhala.azure.storage.community import FS


class ADLFSTest(unittest.TestCase):
    def setUp(self):
        account_name = 'davidkhala'
        key1 = os.environ.get('key1')
        self.fs = FS(account_name, key1)
    def test_connect(self):
        self.assertTrue(self.fs.connect())
    def test_upload(self):
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        self.fs.fromPandas(df, "data","test.parquet")




if __name__ == '__main__':
    unittest.main()