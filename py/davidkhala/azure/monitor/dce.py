from typing import Iterable
from azure.mgmt.monitor.v2022_06_01.models import DataCollectionEndpointResource, DataCollectionEndpointNetworkAcls, \
    KnownPublicNetworkAccessOptions
from azure.mgmt.monitor.v2022_06_01.operations import DataCollectionEndpointsOperations

from davidkhala.azure.monitor import AbstractResource


class DCE:
    def __init__(self, data_collection_endpoints: DataCollectionEndpointsOperations):
        self.data_collection_endpoints = data_collection_endpoints

    class Resource(AbstractResource):
        configuration_access: str
        logs_ingestion: str

        def __init__(self, resource_group_name: str, data_collection_endpoints: DataCollectionEndpointsOperations):
            super().__init__(resource_group_name)
            self.data_collection_endpoints = data_collection_endpoints

        def from_resource(self, r: DataCollectionEndpointResource):
            super().from_resource(r)
            self.configuration_access = r.configuration_access.endpoint
            self.logs_ingestion = r.logs_ingestion.endpoint
            return self

        def delete(self):
            self.data_collection_endpoints.delete(self.resource_group_name, self.name)

    def create(self, resource_group_name, name, location="East Asia"):
        body = DataCollectionEndpointResource(
            location=location,
            network_acls=DataCollectionEndpointNetworkAcls(
                public_network_access=KnownPublicNetworkAccessOptions.ENABLED
            )
        )
        r = DCE.Resource(resource_group_name, self.data_collection_endpoints)
        return r.from_resource(self.data_collection_endpoints.create(resource_group_name, name, body))

    def delete(self, resource_group_name: str, name: str):
        self.data_collection_endpoints.delete(resource_group_name, name)

    def list(self) -> Iterable[DataCollectionEndpointResource]:
        return self.data_collection_endpoints.list_by_subscription()
