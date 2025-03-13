import os
import unittest

from azure.mgmt.monitor.v2022_06_01.models import KnownColumnDefinitionType

from davidkhala.azure.auth import from_service_principal
from davidkhala.azure.ci import credentials
from davidkhala.azure.monitor.dce import DCE
from davidkhala.azure.monitor.dcr import DCR
from davidkhala.azure.monitor.ingestion import Ingestion
from davidkhala.azure.monitor.log import AnalyticsWorkspace
from davidkhala.azure.monitor.monitor import Management as MonitorManagement

credential = credentials()
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
    def setUp(self):
        self.workspace.create(rg, self.name)
    def test_workspace_list(self):
        for w in self.workspace.list():
            print(w)

    def test_dcr_populate(self):
        r = self.workspace.get(rg, self.name)
        dcr = r.default_dcr(self.management.client)

        # Permission denied on managed DCR

    def tearDown(self):
        self.workspace.delete(rg, self.name)



dcr_name = 'dcr2'
monitorManage = MonitorManagement(credential, subscription_id)


class DCRTestCase(unittest.TestCase):
    dcr = DCR(monitorManage.dcr)

    def test_dcr_list(self):
        for dcr_item in self.dcr.list():
            print(dcr_item)

    def test_dcr_create(self):
        dce = DCETestCase().test_dce_create()

        workspace = LogAnalyticsTestCase().test_workspace_get()
        schema = {
            'batch_id': KnownColumnDefinitionType.INT
        }
        from davidkhala.azure.monitor.dcr import Factory
        builder = Factory(dce.resource_group_name, dcr_name)
        builder.with_DataCollectionEndpoint(dce)
        builder.with_LogAnalyticsTable(
            'foreachBatch',
            schema,
            workspace
        )
        builder.build(monitorManage.dcr)

    def test_dcr_get(self):
        r = self.dcr.get(rg, dcr_name)
        print(r)
        return r


class DCETestCase(unittest.TestCase):
    dce_operations = DCE(monitorManage.dce)
    dce_name = 'dce'

    def test_dce_list(self):
        for dce in self.dce_operations.list():
            print(dce)

    def test_dce_create(self):
        r = self.dce_operations.create(rg, self.dce_name)
        print(r)
        self.assertTrue(r.logs_ingestion.startswith(f"https://{self.dce_name}-"))
        self.assertTrue(r.logs_ingestion.endswith(".eastasia-1.ingest.monitor.azure.com"))
        return r



class IngestionTestCase(unittest.TestCase):
    def test_ingestion(self):
        dcr = DCRTestCase().test_dcr_get()
        credential = from_service_principal(
            tenant_id=os.environ.get('TENANT_ID'),
            client_id=os.environ.get('CLIENT_ID'),
            client_secret=os.environ.get('CLIENT_SECRET'),
        )
        i = Ingestion(credential, dcr, None,
                      dce_operations=DCE(monitorManage.dce)
                      )
        i.getLogger()
        print(i.schema)
        i.log({'batch_id': 0})
        i.commit()


if __name__ == '__main__':
    unittest.main()
