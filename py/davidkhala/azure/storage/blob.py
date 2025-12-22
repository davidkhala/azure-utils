from azure.storage.blob import BlobServiceClient
from davidkhala.azure import TokenCredential


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
        except:
            return False

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
