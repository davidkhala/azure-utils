# https://github.com/fsspec/adlfs
from adlfs import AzureBlobFileSystem
from azure.core.exceptions import ClientAuthenticationError


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
        except ClientAuthenticationError as e:
            if (
                    e.status_code == 403 and
                    e.reason == 'Server failed to authenticate the request. Make sure the value of Authorization header is formed correctly including the signature.'
            ): return False
            raise e
