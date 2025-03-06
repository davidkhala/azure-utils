from typing import Iterable, Dict

from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.v2021_06_03_preview.models import AzureMonitorWorkspaceResource
from azure.mgmt.monitor.v2021_06_03_preview.operations import AzureMonitorWorkspacesOperations
from azure.mgmt.monitor.v2022_06_01.models import DataCollectionEndpointResource, DataCollectionEndpointNetworkAcls, \
    KnownPublicNetworkAccessOptions, DataCollectionRuleResource, StreamDeclaration, KnownColumnDefinitionType, \
    ColumnDefinition, DataFlow, DataCollectionRuleDestinations, LogAnalyticsDestination
from azure.mgmt.monitor.v2022_06_01.operations import DataCollectionEndpointsOperations, DataCollectionRulesOperations

from davidkhala.azure import TokenCredential


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

    class Resource:
        immutable_id: str
        id: str
        stream_declarations: Dict[str, StreamDeclaration] | None
        location: str
        data_collection_endpoint_id: str

        def from_resource(self, resource: DataCollectionRuleResource):
            self.immutable_id = resource.immutable_id
            self.id = resource.id
            self.stream_declarations = resource.stream_declarations
            self.location = resource.location
            self.data_collection_endpoint_id = resource.data_collection_endpoint_id
            return self

        def get_one_stream(self) -> str | None:
            if self.stream_declarations is not None:
                for stream in self.stream_declarations.keys():
                    return stream

    def create(self,
               resource_group_name: str,
               name: str,
               data_collection_endpoint_id: str,
               schema: Dict[str, KnownColumnDefinitionType | str],
               WorkspaceResourceId: str,
               location="East Asia") -> DataCollectionRuleResource:
        schema_name = f"Custom-{name}_CL"
        schema["TimeGenerated"] = KnownColumnDefinitionType.DATETIME  # decorate
        columns = [ColumnDefinition(name=name, type=_type) for name, _type in schema.items()]

        workspace_name = WorkspaceResourceId.split('/')[-1]
        body = DataCollectionRuleResource(
            location=location,
            data_collection_endpoint_id=data_collection_endpoint_id,
            stream_declarations={
                schema_name: StreamDeclaration(columns=columns)
            },
            data_flows=[
                DataFlow(streams=[schema_name], destinations=[workspace_name])
            ],
            # TODO
            destinations=DataCollectionRuleDestinations(
                log_analytics=[LogAnalyticsDestination(
                    name=workspace_name,
                    workspace_resource_id=WorkspaceResourceId
                )]
            )

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
        return self.azure_monitor_workspaces.delete(resource_group_name, name)

    class Resource:
        data_collection_rule: str
        data_collection_endpoint: str
        location: str
        id: str

        def __init__(self, resource_group_name: str):
            self.resource_group_name = resource_group_name

        def from_resource(self, resource: AzureMonitorWorkspaceResource):
            self.data_collection_rule = resource.default_ingestion_settings.data_collection_rule_resource_id
            self.data_collection_endpoint = resource.default_ingestion_settings.data_collection_endpoint_resource_id
            self.location = resource.location
            self.id = resource.id
            return self

        def default_dcr(self, client: MonitorManagementClient) -> DCR.Resource:
            words = self.data_collection_rule.split('/')
            control = DCR(client.data_collection_rules)
            got = control.get(words[4], words[-1])
            assert got.stream_declarations is None
            return got

        def create_dcr(self,
                       client: MonitorManagementClient,
                       name,
                       schema: Dict[str, KnownColumnDefinitionType | str],
                       dce_name) -> DCR.Resource:
            control_dce = DCE(client.data_collection_endpoints)
            if not dce_name:
                dce_name = name
            dce = control_dce.create(self.resource_group_name, dce_name, self.location)
            dcr = dce.create_dcr(client, name, schema, self.id)
            return dcr


class DCE:
    def __init__(self, data_collection_endpoints: DataCollectionEndpointsOperations):
        self.data_collection_endpoints = data_collection_endpoints

    class Resource:
        immutable_id: str
        id: str
        configuration_access: str
        logs_ingestion: str

        def __init__(self,
                     data_collection_endpoints: DataCollectionEndpointsOperations,
                     resource_group_name: str,
                     name: str,
                     location: str):
            self.data_collection_endpoints = data_collection_endpoints
            self.resource_group_name = resource_group_name
            self.name = name
            self.location = location

        def from_resource(self, r: DataCollectionEndpointResource):
            self.immutable_id = r.immutable_id
            self.id = r.id
            self.configuration_access = r.configuration_access.endpoint
            self.logs_ingestion = r.logs_ingestion.endpoint
            return self

        def delete(self):
            self.data_collection_endpoints.delete(self.resource_group_name, self.name)

        def create_dcr(self,
                       client: MonitorManagementClient,
                       name: str,
                       schema: Dict[str, KnownColumnDefinitionType | str],
                       log_analytics: str):
            control = DCR(client.data_collection_rules)
            print(log_analytics)  # TODO debug
            return control.create(
                self.resource_group_name,
                name,
                self.id,
                schema,
                log_analytics,
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


from azure.monitor.ingestion import LogsIngestionClient


class Ingestion:
    def __init__(self, credential: TokenCredential, end_point: str):
        self.client = LogsIngestionClient(end_point, credential)

    def log(self, workspace: Workspace.Resource):
        rule = workspace.data_collection_rule  # TODO has to be immutable id?

        self.client.upload(workspace.data_collection_rule)
