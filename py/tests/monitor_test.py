import unittest

from davidkhala.azure.ci import credentials
from davidkhala.azure.monitor.monitor import Management as MonitorManagement

credential = credentials()


subscription_id = "d02180af-0630-4747-ab1b-0d3b3c12dafb"
rg = "LogAnalyticsDefaultResources"


class StaticAPITestCase(unittest.TestCase):
    workspace = MonitorManagement(credential, subscription_id).workspace

    def test_instance(self):
        for w in self.workspace.list():
            print(w.name)
    def test_lifecycle(self):
        name = 'new'
        self.workspace.create(rg, name)
        self.workspace.delete(rg, name)