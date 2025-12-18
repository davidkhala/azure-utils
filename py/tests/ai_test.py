import os
import unittest

from azure.ai.agents.models import RunStatus

from davidkhala.azure.ci import credentials

foundry_id = 'ai-japanest'
project = 'default'
credential = credentials()


class ProjectTestcase(unittest.TestCase):
    def setUp(self):
        from davidkhala.azure.ai import Project
        self.project = Project(foundry_id, project, credential)

    def test_chat(self):
        instruction = "You are a storytelling agent. You craft engaging one-line stories based on user prompts and context."
        prompt = 'Tell me a one line story'
        self.project.as_chat("gpt-4o", instruction, agent_name='new-foundry-agent')
        response = self.project.chat(prompt)
        print(f"Response output: {response.output_text}")
    def test_direct_chat(self):
        self.project.as_chat('gpt-4o', agent_name=None)
        response = self.project.chat('Tell me a one line story')
        print(f"Response output: {response.output_text}")
    def test_agents(self):
        agents = self.project.agents
        for agent in agents:
            print(agent)


class AgentTestCase(unittest.TestCase):
    def setUp(self):
        from davidkhala.azure.ai.agent import Client
        self.client = Client(foundry_id, project, credential)

    def test_bing_tools(self):
        # elapsed time:7.925 seconds
        from davidkhala.azure.ai.tools import bing_tools
        bing_instance = os.environ.get("BING")
        tools = bing_tools(bing_instance)

        self.client.as_agent('gpt-4o', tools=tools)
        from azure.ai.agents.models import ThreadMessageOptions
        from azure.ai.agents.models import MessageRole

        run = self.client.begin_chat(ThreadMessageOptions(
            role=MessageRole.USER,
            content='香港大埔区明日天气'
        ))

        self.client.wait_for_run(run, RunStatus.COMPLETED)

        messages = self.client.get_messages(run)
        for m in messages:
            print(m.text_messages)


if __name__ == '__main__':
    unittest.main()
