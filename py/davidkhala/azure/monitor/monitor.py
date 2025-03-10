from typing import Iterable

from azure.core.exceptions import HttpResponseError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.v2021_06_03_preview.models import AzureMonitorWorkspaceResource
from azure.mgmt.monitor.v2021_06_03_preview.operations import AzureMonitorWorkspacesOperations
from azure.mgmt.monitor.v2022_06_01.models import MonitoringAccountDestination

from davidkhala.azure import TokenCredential
from davidkhala.azure.monitor import AbstractResource


class Management:
    def __init__(self, credential: TokenCredential, subscription_id: str):
        self.client = MonitorManagementClient(credential, subscription_id)

    @property
    def dce(self):
        return self.client.data_collection_endpoints

    @property
    def dcr(self):
        return self.client.data_collection_rules

    @property
    def workspace(self):
        return Workspace(self.client.azure_monitor_workspaces)


class Workspace:
    """
    Azure Monitor workspace
    """

    class Resource(AbstractResource):
        data_collection_rule: str
        data_collection_endpoint: str

        def from_resource(self, resource: AzureMonitorWorkspaceResource):
            super().from_resource(resource)
            self.data_collection_rule = resource.default_ingestion_settings.data_collection_rule_resource_id
            self.data_collection_endpoint = resource.default_ingestion_settings.data_collection_endpoint_resource_id
            return self

        def default_dcr(self, client: MonitorManagementClient):
            words = self.data_collection_rule.split('/')
            from davidkhala.azure.monitor.dcr import DCR
            control = DCR(client.data_collection_rules)
            got = control.get(words[4], words[-1])
            assert got.stream_declarations is None
            return got

        def as_destination(self) -> MonitoringAccountDestination:
            return MonitoringAccountDestination(
                account_resource_id=self.id,
                name=self.name
            )

    def __init__(self, azure_monitor_workspaces: AzureMonitorWorkspacesOperations):
        self.azure_monitor_workspaces = azure_monitor_workspaces

    def list(self) -> Iterable[AzureMonitorWorkspaceResource]:
        return self.azure_monitor_workspaces.list_by_subscription()

    def create(self, resource_group_name: str, name: str, location="East Asia") -> Resource:
        r = self.azure_monitor_workspaces.create(
            resource_group_name, name,
            AzureMonitorWorkspaceResource(location=location)
        )
        return Workspace.Resource().from_resource(r)

    def get(self, resource_group_name: str, name: str) -> Resource:
        return (
            Workspace.Resource()
            .from_resource(self.azure_monitor_workspaces.get(resource_group_name, name))
        )

    def delete(self, resource_group_name: str, name: str):
        self.azure_monitor_workspaces.delete(resource_group_name, name)
        try:
            self.azure_monitor_workspaces.delete(resource_group_name, name)
        except HttpResponseError as e:
            if str(e) != "Operation returned an invalid status 'Accepted'":
                raise e


