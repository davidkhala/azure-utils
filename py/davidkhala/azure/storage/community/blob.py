# https://github.com/fsspec/adlfs
from adlfs import AzureBlobFileSystem, AzureBlobFile
from azure.core.exceptions import ClientAuthenticationError


class FS:
    def __init__(self, account_name: str, account_key: str):
        self._ = AzureBlobFileSystem(
            account_name=account_name,
            account_key=account_key,
        )

    def connect(self):
        try:
            containers = self._.ls("")
            assert isinstance(containers, list)
            return True
        except ClientAuthenticationError as e:
            if (
                    e.status_code == 403 and
                    e.reason == 'Server failed to authenticate the request. Make sure the value of Authorization header is formed correctly including the signature.'
            ): return False
            raise e

class File(AzureBlobFile):

    def __enter__(self):
        self.connect_client()
        return super().__enter__()