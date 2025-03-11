from typing import List, MutableMapping, Any

from azure.monitor.ingestion import LogsIngestionClient

from davidkhala.azure import TokenCredential
from davidkhala.azure.monitor.dce import DCE
from davidkhala.azure.monitor.dcr import DCR


class Ingestion:
    logs: List[MutableMapping[str, Any]]
    stream_name: str
    dcr: str

    def __init__(self, credential: TokenCredential, end_point: DCE.Resource):
        self.client = LogsIngestionClient(end_point, credential) # TODO FIXE type

    def getLogger(self, dcr: DCR.Resource):
        stream_name = dcr.get_one_stream()
        assert stream_name is not None
        self.stream_name = stream_name
        self.dcr = dcr.immutable_id
        self.logs = []

    def commit(self):
        self.client.upload(self.dcr, self.stream_name, self.logs)

    def log(self, message: MutableMapping[str, Any]):
        self.logs.append(message)
