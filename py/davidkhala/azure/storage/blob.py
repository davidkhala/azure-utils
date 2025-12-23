from typing import Union, Iterable, AnyStr, IO

from azure.core.exceptions import ClientAuthenticationError
from azure.storage.blob import BlobServiceClient

from davidkhala.azure import TokenCredential


class Object:
    def __init__(self, service_client: BlobServiceClient, container: str, file_name: str):
        self.client = service_client.get_blob_client(container, file_name)

    def upload(self, data: Union[bytes, str, Iterable[AnyStr], IO[bytes]], *, overwrite=True):
        self.client.upload_blob(data, overwrite=overwrite)


class Client:
    def __init__(self, account_name: str, credential: TokenCredential | str):
        """

        :param account_name:
        :param credential: could be the access key in str
        """
        self.client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=credential
        )

    def connect(self):
        try:
            self.account_information
            return True

        except ClientAuthenticationError as e:
            if (e.status_code == 401 and e.reason == 'Server failed to authenticate the request. Please refer to the information in the www-authenticate header.'):
                return False
            raise e

    def blob(self, container: str, file_name: str) -> Object:
        return Object(self.client, container, file_name)

    @property
    def account_information(self):
        data = self.client.get_account_information()
        return {
            'version': data.get('version'),
            'date': data.get('date'),
            'sku_name': data.get("sku_name"),
            'account_kind': data.get('account_kind'),
            'is_hns_enabled': data.get("is_hns_enabled"),
        }
