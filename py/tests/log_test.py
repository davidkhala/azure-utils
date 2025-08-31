import os
import unittest

from azure.mgmt.loganalytics.models import ColumnTypeEnum

from davidkhala.azure.auth import from_service_principal
from davidkhala.azure.ci import credentials
from davidkhala.azure.monitor.log import AnalyticsWorkspace, AnalyticsTable
from davidkhala.azure.monitor.monitor import Management as MonitorManagement

credential = credentials()
subscription_id = "d02180af-0630-4747-ab1b-0d3b3c12dafb"
rg = "LogAnalyticsDefaultResources"


class LogAnalyticsTestCase(unittest.TestCase):
    management = AnalyticsWorkspace(credential, subscription_id)
    name = 'workspace'

    def test_workspace_list(self):
        for w in self.management.list():
            print(w)

    def test_workspace_get(self):
        r = self.management.get(rg, self.name)
        tableOps = AnalyticsTable(r)
        for table in tableOps.list(no_system=True):
            print(table)
        return r

class MonitorTestCase(unittest.TestCase):
    management = MonitorManagement(credential, subscription_id)
    workspace = management.workspace
    name = 'workspace'

    @classmethod
    def setUpClass(cls):
        provision = cls.workspace.create(rg, cls.name)
        print('provisioned', provision)
    def test_workspace_create(self):
        name = 'test'
        self.workspace.create(rg, name)
        self.workspace.delete(rg, name)
    def test_workspace_get(self):
        r = self.workspace.get(rg, self.name)
        self.assertIsNotNone(r)

    def test_workspace_list(self):
        for w in self.workspace.list():
            print(w)

    def test_dcr_populate(self):
        r = self.workspace.get(rg, self.name)
        dcr = r.default_dcr(self.management.client)

        # Permission denied on managed DCR

    @classmethod
    def tearDownClass(cls):
        cls.workspace.delete(rg, cls.name)


monitorManage = MonitorManagement(credential, subscription_id)


class DCRTestCase(unittest.TestCase):
    from davidkhala.azure.monitor.dcr import DCR
    dcr = DCR(monitorManage.dcr)
    name = 'dcr'

    def test_dcr_list(self):
        for dcr_item in self.dcr.list():
            print(dcr_item)

    def test_dcr_create(self):
        self.dcr.delete(rg, self.name)
        dce = DCETestCase().test_dce_get()

        workspace = LogAnalyticsTestCase().test_workspace_get()
        schema = {
            'batch_id': ColumnTypeEnum.INT
        }
        from davidkhala.azure.monitor.dcr import Factory
        builder = Factory(dce.resource_group_name, self.name)
        builder.with_DataCollectionEndpoint(dce)
        builder.with_LogAnalyticsTable(
            'foreachBatch',
            schema,
            workspace
        )
        builder.build(monitorManage.dcr)

    def test_dcr_get(self):
        r = self.dcr.get(rg, self.name)
        print(r)
        return r


class DCETestCase(unittest.TestCase):
    from davidkhala.azure.monitor.dce import DCE
    dce_operations = DCE(monitorManage.dce)
    dce_name = 'dce'

    def test_dce_list(self):
        for dce in self.dce_operations.list():
            print(dce)

    def test_dce_get(self):
        return self.dce_operations.get(rg, self.dce_name)

    def test_dce_create(self):
        name = 'dce2'
        r = self.dce_operations.create(rg, name)
        print(r)
        self.assertTrue(r.logs_ingestion.startswith(f"https://{name}-"))
        self.assertTrue(r.logs_ingestion.endswith(".eastasia-1.ingest.monitor.azure.com"))
        self.dce_operations.delete(rg, name)


class IngestionTestCase(unittest.TestCase):

    def test_ingestion(self):
        from davidkhala.azure.monitor.ingestion import Ingestion
        from davidkhala.azure.monitor.dce import DCE
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
        i.log({'batch_id': 0})
        i.commit()


if __name__ == '__main__':
    unittest.main()
