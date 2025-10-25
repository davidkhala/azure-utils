import os
import unittest

from azure.ai.agents.models import RunStatus

from davidkhala.azure.ci import credentials


class AgentTestCase(unittest.TestCase):
    def setUp(self):
        from davidkhala.azure.ai.agent import Client
        self.client = Client('ai-japanest', 'default', credentials())

    def test_bing_tools(self):
        # elapsed time:7.925 seconds
        from davidkhala.azure.ai.tools import bing_tools
        bing_instance = os.environ.get("BING")
        tools = bing_tools(bing_instance)

        self.client.as_agent('gpt-4o', tools=tools)
        from azure.ai.agents.models import ThreadMessageOptions
        from azure.ai.agents.models import MessageRole

        run = self.client.begin_chat(ThreadMessageOptions(
            role= MessageRole.USER,
            content = '香港大埔区明日天气'
        ))

        self.client.wait_for_run(run, RunStatus.COMPLETED)

        messages = self.client.get_messages(run)
        for m in messages:
            print(m.text_messages)




if __name__ == '__main__':
    unittest.main()
