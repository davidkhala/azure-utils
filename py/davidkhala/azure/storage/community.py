# https://github.com/fsspec/adlfs
from adlfs import AzureBlobFileSystem


class FS:
    def __init__(self, account_name: str, account_key: str):
        self.blob_fs = AzureBlobFileSystem(
            account_name=account_name,
            account_key=account_key,
        )

    def connect(self):
        try:
            containers = self.blob_fs.ls("")
            assert isinstance(containers, list)
            return True
        except:
            return False

    def fromPandas(self, df, container: str, blob_path: str):
        from davidkhala.data.integration.to.arrow import fromPandas, bytesFrom
        table = fromPandas(df)
        _bytes = bytesFrom(table)

        with self.blob_fs.open(f"{container}/{blob_path}", "wb") as f:
            f.write(_bytes)
