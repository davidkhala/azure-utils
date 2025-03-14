from dataclasses import dataclass
from typing import Iterable

from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.v2021_06_03_preview.models import AzureMonitorWorkspaceResource, ProvisioningState
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

    @dataclass
    class Resource(AbstractResource):
        data_collection_rule: str
        data_collection_endpoint: str
        state: ProvisioningState | str  # one of ["Creating", "Succeeded", "Deleting","Failed", and "Canceled"]

        def from_resource(self, resource: AzureMonitorWorkspaceResource):
            super().from_resource(resource)
            self.data_collection_rule = resource.default_ingestion_settings.data_collection_rule_resource_id
            self.data_collection_endpoint = resource.default_ingestion_settings.data_collection_endpoint_resource_id
            self.state = resource.provisioning_state
            self.immutable_id = resource.account_id
            return self

        def default_dcr(self, client: MonitorManagementClient):
            from davidkhala.azure.monitor.dcr import DCR
            control = DCR(client.data_collection_rules)
            got = control.get_by_id(self.data_collection_rule)
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
        self.wait_until_gone(resource_group_name, name)
        r = self.azure_monitor_workspaces.create(
            resource_group_name, name,
            AzureMonitorWorkspaceResource(location=location)
        )
        wrapped = Workspace.Resource(*[None] * 8).from_resource(r)
        assert wrapped.state == ProvisioningState.SUCCEEDED
        return wrapped

    def get(self, resource_group_name: str, name: str) -> Resource | None:
        try:
            r = self.azure_monitor_workspaces.get(resource_group_name, name)
            return Workspace.Resource(*[None] * 8).from_resource(r)
        except ResourceNotFoundError:
            return None

    def delete_async(self, resource_group_name: str, name: str):
        try:
            self.azure_monitor_workspaces.delete(resource_group_name, name)
        except HttpResponseError as e:
            if str(e) != "Operation returned an invalid status 'Accepted'":
                raise e

    def wait_until_gone(self, resource_group_name: str, name: str):
        r = self.get(resource_group_name, name)
        while r is not None:
            assert r.state == ProvisioningState.DELETING
            r = self.get(resource_group_name, name)

    def delete(self, resource_group_name: str, name: str):
        self.delete_async(resource_group_name, name)
        self.wait_until_gone(resource_group_name, name)
