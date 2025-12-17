from azure.ai.agents.models import Agent
from azure.core.paging import ItemPaged
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from davidkhala.azure.auth import TokenCredential
from azure.ai.projects.models import AgentVersionObject
from openai import OpenAI
from openai.types.responses.response import Response
from azure.ai.projects.models import AgentObject


class Project:
    def __init__(self, foundry_id, project, credential: TokenCredential):
        self.client = AIProjectClient(
            endpoint=f"https://{foundry_id}.services.ai.azure.com/api/projects/{project}",
            credential=credential,
        )

    def as_chat(self, model: str, sys_prompt: str = None, *, agent_name: str) -> AgentVersionObject:
        self.agent = self.client.agents.create_version(
            agent_name=agent_name,
            definition=PromptAgentDefinition(
                model=model,
                instructions=sys_prompt
            ),
        )

    @property
    def agents(self) -> list[AgentObject]:
        return [*self.client.agents.list()]

    def chat(self, *user_prompt, **kwargs) -> Response:
        openai_client: OpenAI = self.client.get_openai_client()
        extra_body = {}
        if self.agent:
            extra_body["agent"] = {"name": self.agent.name, "type": "agent_reference"}
        response = openai_client.responses.create(
            input=[{"role": "user", "content": _} for _ in user_prompt],
            extra_body=extra_body,
        )
        return response
