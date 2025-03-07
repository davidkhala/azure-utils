from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Dict, Optional

from azure.core.exceptions import HttpResponseError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.v2021_06_03_preview.models import AzureMonitorWorkspaceResource
from azure.mgmt.monitor.v2021_06_03_preview.operations import AzureMonitorWorkspacesOperations
from azure.mgmt.monitor.v2022_06_01.models import KnownColumnDefinitionType, StreamDeclaration, \
    DataCollectionRuleResource, DataCollectionRuleDestinations, ColumnDefinition, DataFlow, \
    DataCollectionEndpointResource, DataCollectionEndpointNetworkAcls, KnownPublicNetworkAccessOptions
from azure.mgmt.monitor.v2022_06_01.operations import DataCollectionRulesOperations, DataCollectionEndpointsOperations

from davidkhala.azure import TokenCredential


@dataclass
class AbstractResource(ABC):
    immutable_id: Optional[str]
    id: str
    location: str
    name: str
    resource_group_name: str

    def from_resource(self, resource):
        self.id = resource.id
        self.location = resource.location
        self.name = resource.name
        if hasattr(resource, 'immutable_id'):
            self.immutable_id = resource.immutable_id


class Management:
    def __init__(self, credential: TokenCredential, subscription_id: str):
        self.client = MonitorManagementClient(credential, subscription_id)

    @property
    def dce(self):
        return DCE(self.client.data_collection_endpoints)

    @property
    def dcr(self):
        return DCR(self.client.data_collection_rules)

    @property
    def workspace(self):
        return Workspace(self.client.azure_monitor_workspaces)


class DCR:
    def __init__(self, data_collection_rules: DataCollectionRulesOperations):
        self.data_collection_rules = data_collection_rules

    class Resource(AbstractResource):
        stream_declarations: Dict[str, StreamDeclaration] | None
        data_collection_endpoint_id: str

        def from_resource(self, resource: DataCollectionRuleResource):
            super().from_resource(resource)
            self.stream_declarations = resource.stream_declarations
            self.data_collection_endpoint_id = resource.data_collection_endpoint_id
            return self

        def get_one_stream(self) -> str | None:
            if self.stream_declarations is not None:
                for stream in self.stream_declarations.keys():
                    return stream

    class Destinations:
        def __init__(self, destinations: DataCollectionRuleDestinations):
            mapper = lambda l: (item.name for item in l)

            self.names = [
                *mapper(destinations.log_analytics),
                *mapper(destinations.monitoring_accounts),
                *mapper(destinations.azure_monitor_metrics),
                *mapper(destinations.event_hubs),
                *mapper(destinations.event_hubs_direct),
                *mapper(destinations.storage_blobs_direct),
                *mapper(destinations.storage_tables_direct),
                *mapper(destinations.storage_accounts),
            ]

    def create(self,
               resource_group_name: str,
               name: str,
               data_collection_endpoint_id: str,
               schema: Dict[str, KnownColumnDefinitionType | str],
               destinations: DataCollectionRuleDestinations,
               location="East Asia") -> DataCollectionRuleResource:
        schema_name = f"Custom-{name}_CL"
        schema["TimeGenerated"] = KnownColumnDefinitionType.DATETIME  # decorate
        columns = [ColumnDefinition(name=name, type=_type) for name, _type in schema.items()]

        body = DataCollectionRuleResource(
            location=location,
            data_collection_endpoint_id=data_collection_endpoint_id,
            stream_declarations={
                schema_name: StreamDeclaration(columns=columns)
            },
            data_flows=[
                DataFlow(streams=[schema_name], destinations=DCR.Destinations(destinations).names)
            ],
            destinations=destinations
        )
        r = self.data_collection_rules.create(resource_group_name, name, body)
        return r

    def get(self, resource_group_name: str, name: str) -> Resource:
        r = self.data_collection_rules.get(resource_group_name, name)
        return DCR.Resource().from_resource(r)

    def list(self) -> Iterable[DataCollectionRuleResource]:
        return self.data_collection_rules.list_by_subscription()


class Workspace:
    """
    Azure Monitor workspace
    """

    def __init__(self, azure_monitor_workspaces: AzureMonitorWorkspacesOperations):
        self.azure_monitor_workspaces = azure_monitor_workspaces

    def list(self) -> Iterable[AzureMonitorWorkspaceResource]:
        return self.azure_monitor_workspaces.list_by_subscription()

    def create(self, resource_group_name: str, name: str, location="East Asia"):
        r = self.azure_monitor_workspaces.create(
            resource_group_name, name,
            AzureMonitorWorkspaceResource(location=location)
        )
        return Workspace.Resource(resource_group_name).from_resource(r)

    def get(self, resource_group_name: str, name: str):
        return (
            Workspace.Resource(resource_group_name)
            .from_resource(self.azure_monitor_workspaces.get(resource_group_name, name))
        )

    def delete(self, resource_group_name: str, name: str):
        self.azure_monitor_workspaces.delete(resource_group_name, name)
        try:
            self.azure_monitor_workspaces.delete(resource_group_name, name)
        except HttpResponseError as e:
            if str(e) != "Operation returned an invalid status 'Accepted'":
                raise e

    class Resource(AbstractResource):
        data_collection_rule: str
        data_collection_endpoint: str

        def from_resource(self, resource: AzureMonitorWorkspaceResource):
            super().from_resource(resource)
            self.data_collection_rule = resource.default_ingestion_settings.data_collection_rule_resource_id
            self.data_collection_endpoint = resource.default_ingestion_settings.data_collection_endpoint_resource_id
            return self

        def default_dcr(self, client: MonitorManagementClient) -> DCR.Resource:
            words = self.data_collection_rule.split('/')
            control = DCR(client.data_collection_rules)
            got = control.get(words[4], words[-1])
            assert got.stream_declarations is None
            return got


class DCE:
    def __init__(self, data_collection_endpoints: DataCollectionEndpointsOperations):
        self.data_collection_endpoints = data_collection_endpoints

    class Resource(AbstractResource):
        configuration_access: str
        logs_ingestion: str

        def __init__(self, resource_group_name: str, data_collection_endpoints: DataCollectionEndpointsOperations):
            super().__init__(resource_group_name=resource_group_name)
            self.data_collection_endpoints = data_collection_endpoints

        def from_resource(self, r: DataCollectionEndpointResource):
            super().from_resource(r)
            self.configuration_access = r.configuration_access.endpoint
            self.logs_ingestion = r.logs_ingestion.endpoint
            return self

        def delete(self):
            self.data_collection_endpoints.delete(self.resource_group_name, self.name)

        def create_dcr(self,
                       client: MonitorManagementClient,
                       name: str,
                       schema: Dict[str, KnownColumnDefinitionType | str],
                       destinations: DataCollectionRuleDestinations):
            control = DCR(client.data_collection_rules)

            return control.create(
                self.resource_group_name,
                name,
                self.id,
                schema,
                destinations,
                self.location
            )

    def create(self, resource_group_name, name, location="East Asia"):
        body = DataCollectionEndpointResource(
            location=location,
            network_acls=DataCollectionEndpointNetworkAcls(
                public_network_access=KnownPublicNetworkAccessOptions.ENABLED
            )
        )
        r = DCE.Resource(self.data_collection_endpoints, resource_group_name, name, location)
        r.from_resource(self.data_collection_endpoints.create(resource_group_name, name, body))
        return r

    def delete(self, resource_group_name: str, name: str):
        self.data_collection_endpoints.delete(resource_group_name, name)

    def list(self) -> Iterable[DataCollectionEndpointResource]:
        return self.data_collection_endpoints.list_by_subscription()
