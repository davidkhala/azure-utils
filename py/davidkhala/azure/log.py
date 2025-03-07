from typing import Dict, Iterable, List, MutableMapping, Any

from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.loganalytics.models import WorkspaceListResult, Workspace
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.v2022_06_01.models import KnownColumnDefinitionType
from azure.monitor.ingestion import LogsIngestionClient

from davidkhala.azure import TokenCredential
from davidkhala.azure.monitor import DCR, DCE


class Management:
    def __init__(self, credential: TokenCredential, subscription_id: str):
        self.client = LogAnalyticsManagementClient(credential, subscription_id)

    def list(self) -> Iterable[WorkspaceListResult]:
        return self.client.workspaces.list()

    def create(self, resource_group_name, name) -> Workspace:
        promise = self.client.workspaces.begin_create_or_update(resource_group_name, name)
        return promise.result()

    def delete(self, resource_group_name: str, name: str, force=True):
        """
        :param name:
        :param resource_group_name:
        :param force: Deletes the workspace without the recovery option (kept for 14 days).
        """
        promise = self.client.workspaces.begin_delete(resource_group_name, name, force)
        return promise.result()


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
