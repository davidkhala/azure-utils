import os
import random
import time
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
        r = self.get_workspace()
        tableOps = AnalyticsTable(r)
        for table in tableOps.list(no_system=True):
            print(table)

    def get_workspace(self):
        return self.management.get(rg, self.name)


class MonitorTestCase(unittest.TestCase):
    management = MonitorManagement(credential, subscription_id)
    workspace = management.workspace

    def test_workspace_create(self):
        name = f"test-ws-{random.randint(1000,2000)}"
        self.workspace.create(rg, name)
        r = self.workspace.get(rg, name)
        self.assertIsNotNone(r)
        self.workspace.delete(rg, name)

    def test_workspace_list(self):
        for w in self.workspace.list():
            print(w)


monitorManage = MonitorManagement(credential, subscription_id)


class DCRTestCase(unittest.TestCase):
    from davidkhala.azure.monitor.dcr import DCR
    dcr = DCR(monitorManage.dcr)
    name = 'dcr'

    def test_dcr_list(self):
        for dcr_item in self.dcr.list():
            print(dcr_item)

    def test_dcr_create(self):

        name = f"dcr-{random.randint(1000,2000)}"
        dce = DCETestCase().get_dce()

        workspace = LogAnalyticsTestCase().get_workspace()
        schema = {
            'batch_id': ColumnTypeEnum.INT
        }
        from davidkhala.azure.monitor.dcr import Factory
        builder = Factory(dce.resource_group_name, name)
        builder.with_DataCollectionEndpoint(dce)
        builder.with_LogAnalyticsTable(
            'foreachBatch',
            schema,
            workspace
        )
        builder.build(monitorManage.dcr)
        self.dcr.delete(rg, name)

    def get_dcr(self):
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

    def get_dce(self):
        return self.dce_operations.get(rg, self.dce_name)

    def test_dce_create(self):
        name = f"dce-{int(time.time())}"
        print(name)
        r = self.dce_operations.create(rg, name)
        print(r)
        self.assertTrue(r.logs_ingestion.startswith(f"https://{name}-"))
        self.assertTrue(r.logs_ingestion.endswith(".eastasia-1.ingest.monitor.azure.com"))
        self.dce_operations.delete(rg, name)


class IngestionTestCase(unittest.TestCase):

    def test_ingestion(self):
        from davidkhala.azure.monitor.ingestion import Ingestion
        from davidkhala.azure.monitor.dce import DCE
        dcr = DCRTestCase().get_dcr()
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
