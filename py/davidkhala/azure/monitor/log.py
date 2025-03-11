from typing import Iterable

from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.loganalytics.models import Table, Workspace as NativeWorkspace
from azure.mgmt.loganalytics.operations import TablesOperations

from davidkhala.azure import TokenCredential
from davidkhala.azure.monitor import AbstractResource


class AnalyticsWorkspace:
    def __init__(self, credential: TokenCredential, subscription_id: str):
        self.client = LogAnalyticsManagementClient(credential, subscription_id)

    def list(self) -> Iterable[NativeWorkspace]:
        return self.client.workspaces.list()

    class Resource(AbstractResource):
        customer_id: str

        def __init__(self, resource_group_name: str, client: LogAnalyticsManagementClient):
            super().__init__(resource_group_name)
            self.client = client

        @property
        def tables(self):
            return AnalyticsTable(self.client.tables, self)

        def from_resource(self, resource: NativeWorkspace):
            super().from_resource(resource)
            self.customer_id = resource.customer_id
            return self

    def create(self, resource_group_name, name) -> Resource:
        promise = self.client.workspaces.begin_create_or_update(resource_group_name, name)
        return AnalyticsWorkspace.Resource(resource_group_name, self.tables).from_resource(promise.result())

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

    def get(self, resource_group_name, name) -> Resource:
        return (
            AnalyticsWorkspace.Resource(resource_group_name, self.tables)
            .from_resource(self.client.workspaces.get(resource_group_name, name))
        )


class AnalyticsTable:
    def __init__(self, tables: TablesOperations, workspace: AnalyticsWorkspace.Resource):
        self.tables = tables
        self.workspace = workspace.name
        self.resource_group_name = workspace.resource_group_name

    def list(self):
        return self.tables.list_by_workspace(self.resource_group_name, self.workspace)

    def create(self, table_name: str) -> Table:
        parameters = Table()
        return self.tables.create(self.resource_group_name, self.workspace, table_name, parameters)
