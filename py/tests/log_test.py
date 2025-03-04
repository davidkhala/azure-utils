import unittest

from azure.mgmt.monitor.v2022_06_01.models import KnownColumnDefinitionType

from davidkhala.azure.auth import default
from davidkhala.azure.log import Management, Ingestion, DCR

credential = default()
subscription_id = "3fc7b4b0-def4-470c-a27a-8cddb4e0639f"
rg = "AppTeamDemo"
management = Management(credential, subscription_id)


class LogAnalyticsTestCase(unittest.TestCase):
    workspace = management.log_analytics
    name = 'workspace'
    def test_workspace_list(self):
        for w in self.workspace.list():
            print(w)

    def test_workspace_create(self):

        r = self.workspace.create(rg, self.name)


    def test_dcr_populate(self):
        r = self.workspace.get(rg, self.name)
        dcr = r.default_dcr(management.client)

        # Permission denied on managed DCR
    def test_workspace_delete(self):
        self.workspace.delete(rg, self.name)



class IngestionTestCase(unittest.TestCase):
    dce_name = 'dce'

    def test_dcr_list(self):
        dcr = management.dcr
        for dcr_item in dcr.list():
            print(dcr_item)

    def test_dcr_create(self):
        dce = self.test_dce_create()
        name = 'dcr'
        dcr = dce.create_dcr(management.client, name)
        print(dcr)

    def test_dce_list(self):
        for dce in management.dce.list():
            print(dce)

    def test_dce_create(self):
        r = management.dce.create(rg, self.dce_name)
        print(r)
        self.assertTrue(r.logs_ingestion.startswith(f"https://{self.dce_name}-"))
        self.assertTrue(r.logs_ingestion.endswith(".eastasia-1.ingest.monitor.azure.com"))
        return r

    def test_ingestion(self):
        endpoint = "https://dce-shvq.eastasia-1.ingest.monitor.azure.com"
        i = Ingestion(credential, endpoint)

    def tearDown(self):
        management.dce.delete(rg, self.dce_name)


if __name__ == '__main__':
    unittest.main()
