from abc import ABC
from dataclasses import dataclass


@dataclass
class AbstractResource(ABC):
    immutable_id: str | None
    id: str
    location: str
    name: str
    resource_group_name: str

    def __init__(self, resource_group_name: str):
        self.resource_group_name = resource_group_name
        self.immutable_id = None

    def from_resource(self, resource):
        self.id = resource.id
        self.location = resource.location
        self.name = resource.name
        if hasattr(resource, 'immutable_id'):
            self.immutable_id = resource.immutable_id
