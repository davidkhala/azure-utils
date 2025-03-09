import unittest

from azure.mgmt.monitor.v2022_06_01.models import KnownColumnDefinitionType

from davidkhala.azure.auth import default
from davidkhala.azure.log import Ingestion
from davidkhala.azure.log import Analytics as LogManagement
from davidkhala.azure.monitor import Management as MonitorManagement

credential = default()
subscription_id = "3fc7b4b0-def4-470c-a27a-8cddb4e0639f"
rg = "AppTeamDemo"


class LogAnalyticsTestCase(unittest.TestCase):
    management = LogManagement(credential, subscription_id)

    def test_workspace_list(self):
        for w in self.management.list():
            print(w)

    def test_dcr_create(self):
        ...


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
        dcr = self.management.dcr
        for dcr_item in dcr.list():
            print(dcr_item)

    def test_dcr_create(self):
        dce = DCETestCase().test_dce_create()
        workspace = MonitorTestCase().test_workspace_create()
        name = 'dcr'
        schema_name  = "..."
        schema = {
            'batch_id': KnownColumnDefinitionType.INT
        }
        from azure.mgmt.monitor.v2022_06_01.models import DataCollectionRuleDestinations

        destinations = DataCollectionRuleDestinations(
            monitoring_accounts=[workspace.as_destination()]
        )

        dcr = dce.create_dcr(
            self.management.client,
            name,
            schema,
            destinations)
        print(dcr)


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
