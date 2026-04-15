import os
from dotenv import load_dotenv

load_dotenv()

from vanna import Agent, AgentConfig
from vanna.core.user import UserResolver, User, RequestContext

from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool
)

from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService


#  User Resolver
class DefaultUserResolver(UserResolver):
    def resolve_user(self, request: RequestContext) -> User:
        return User(user_id="default_user")


def get_agent():
    print("DEBUG: FINAL CLEAN VERSION")

    # LLM
    llm = GeminiLlmService(
        model="gemini-2.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    # DB
    runner = SqliteRunner("clinic.db")

    # Tools (NO registry)
    tools = [
        RunSqlTool(sql_runner=runner),
        VisualizeDataTool(),
        SaveQuestionToolArgsTool(),
        SearchSavedCorrectToolUsesTool()
    ]

    # Memory
    memory = DemoAgentMemory()

    # User Resolver
    user_resolver = DefaultUserResolver()

    # Config
    config = AgentConfig(
        llm=llm,
        tools=tools,
        memory=memory
    )

    # Agent (your version needs these)
    agent = Agent(
        config,
        None,              # tool_registry not needed here
        user_resolver,
        memory
    )

    return agent