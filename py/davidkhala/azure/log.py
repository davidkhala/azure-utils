from typing import Iterable, List, MutableMapping, Any

from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.loganalytics.models import WorkspaceListResult, Table
from azure.mgmt.loganalytics.operations import TablesOperations
from azure.monitor.ingestion import LogsIngestionClient

from davidkhala.azure import TokenCredential
from davidkhala.azure.monitor import DCR, DCE, AbstractResource


class Analytics:
    def __init__(self, credential: TokenCredential, subscription_id: str):
        self.client = LogAnalyticsManagementClient(credential, subscription_id)

    def list(self) -> Iterable[WorkspaceListResult]:
        return self.client.workspaces.list()
    class Workspace(AbstractResource):
        def __init__(self, resource_group_name: str, client: LogAnalyticsManagementClient):
            super().__init__(resource_group_name)
            self.client = client
        @property
        def tables(self):
            return AnalyticsTable(self.client.tables, self)

    def create(self, resource_group_name, name) -> Workspace:
        promise = self.client.workspaces.begin_create_or_update(resource_group_name, name)
        return Analytics.Workspace(resource_group_name, self.tables).from_resource(promise.result())

    @property
    def tables(self):
        return self.client.tables

    def delete(self, resource_group_name: str, name: str, force=True):
        """
        :param name:
        :param resource_group_name:
        :param force: Deletes the workspace without the recovery option (kept for 14 days).
        """
        promise = self.client.workspaces.begin_delete(resource_group_name, name, force)
        promise.result()
    def get(self, resource_group_name, name)->Workspace:
        return Analytics.Workspace(resource_group_name, self.tables).from_resource(self.client.workspaces.get(resource_group_name, name))




class AnalyticsTable:
    def __init__(self, tables: TablesOperations, workspace: Analytics.Workspace):
        self.tables = tables
        self.workspace = workspace.name
        self.resource_group_name = workspace.resource_group_name
    def list(self):
        return self.tables.list_by_workspace(self.resource_group_name, self.workspace)
    def create(self,  table_name: str)->Table:
        parameters = Table()
        # TODO https://learn.microsoft.com/en-us/azure/azure-monitor/logs/tutorial-logs-ingestion-portal?source=recommendations#create-new-table-in-log-analytics-workspace
        return self.tables.create(self.resource_group_name,self.workspace,table_name, parameters)


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
