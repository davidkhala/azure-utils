import unittest

from azure.mgmt.monitor.v2022_06_01.models import KnownColumnDefinitionType

from davidkhala.azure.auth import default
from davidkhala.azure.monitor.dcr import DCR
from davidkhala.azure.monitor.log import AnalyticsWorkspace
from davidkhala.azure.monitor.monitor import Management as MonitorManagement
from davidkhala.azure.monitor.ingestion import Ingestion

credential = default()
subscription_id = "d02180af-0630-4747-ab1b-0d3b3c12dafb"
rg = "root-compartment"


class LogAnalyticsTestCase(unittest.TestCase):
    management = AnalyticsWorkspace(credential, subscription_id)
    name = 'Log-Analytics'
    def test_workspace_list(self):
        for w in self.management.list():
            print(w)

    def test_workspace_get(self):
        r = self.management.get(rg, self.name)
        return r

class MonitorTestCase(unittest.TestCase):
    management = MonitorManagement(credential, subscription_id)
    workspace = management.workspace
    name = 'workspace'

    def test_workspace_list(self):
        for w in self.workspace.list():
            print(w)

    def test_workspace_create(self):
        r = self.workspace.create(rg, self.name)
        print(r)
        return r

    def test_dcr_populate(self):
        r = self.workspace.get(rg, self.name)
        dcr = r.default_dcr(self.management.client)

        # Permission denied on managed DCR

    def test_workspace_delete(self):
        self.workspace.delete(rg, self.name)



class DCRTestCase(unittest.TestCase):
    management = MonitorManagement(credential, subscription_id)

    def test_dcr_list(self):
        dcr = DCR(self.management.dcr)
        for dcr_item in dcr.list():
            print(dcr_item)

    def test_dcr_create(self):
        dce = DCETestCase().test_dce_create()

        name = 'dcr2'
        workspace = LogAnalyticsTestCase().test_workspace_get()
        schema = {
            'batch_id': KnownColumnDefinitionType.INT
        }
        from davidkhala.azure.monitor.dcr import Factory
        builder = Factory(dce.resource_group_name, name)
        builder.with_DataCollectionEndpoint(dce)
        builder.with_LogAnalyticsTable(
            'foreachBatch',
            schema,
            workspace
        )
        builder.build(self.management.dcr)



class DCETestCase(unittest.TestCase):
    management = MonitorManagement(credential, subscription_id)

    def test_dce_list(self):
        for dce in self.management.dce.list():
            print(dce)

    dce_name = 'dce'

    def test_dce_create(self):
        r = self.management.dce.create(rg, self.dce_name)
        print(r)
        self.assertTrue(r.logs_ingestion.startswith(f"https://{self.dce_name}-"))
        self.assertTrue(r.logs_ingestion.endswith(".eastasia-1.ingest.monitor.azure.com"))
        return r

    def tearDown(self):
        self.management.dce.delete(rg, self.dce_name)


class IngestionTestCase(unittest.TestCase):
    def test_ingestion(self):
        endpoint = "https://dce-shvq.eastasia-1.ingest.monitor.azure.com"
        i = Ingestion(credential, endpoint)


if __name__ == '__main__':
    unittest.main()
