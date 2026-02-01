import os
from typing import Any, Dict, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession as MCPClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


class MCPClient:
    def __init__(self):
        self.mcp_client_session: Optional[MCPClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Load server path once during initialization
        self.server_script_path = self._get_server_script_path()

    async def close(self):
        # Cleanly shut down MCP session, stdio pipes, and server subprocess
        await self.exit_stack.aclose()

    def _get_server_script_path(self) -> str:
        """Load MCP server script path from environment variables"""
        path = os.getenv("MCP_SERVER_SCRIPT_PATH")
        if not path:
            raise RuntimeError("MCP_SERVER_SCRIPT_PATH is not set in environment")
        return path

    async def connect_to_mcp_server(self):
        """Connect to the MCP server over stdio"""

        if not self.server_script_path.endswith(".py"):
            raise ValueError("Server script must be a .py file")

        #  object for terminal command to start MCP server
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_script_path],
            env=None,
        )

        #  Start MCP server as subprocess + open async stdio pipes to it.
        # code ⇄ async pipes ⇄ python server.py:
        # stdio → async read byte stream from server (server → client)
        # write → async write byte stream to server (client → server)
        # AsyncExitStack for cleanup
        stdio, write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        # start MCP client session and store in instacne variable
        # AsyncExitStack for cleanup (async process + pipes)
        # Wrap stdio streams in MCPClientSession
        self.mcp_client_session = await self.exit_stack.enter_async_context(
            MCPClientSession(stdio, write)
        )

        # Initialize the MCP client session
        # All MCP clients have initialize()
        await self.mcp_client_session.initialize()

        # All MCP clients have list_tools()
        response = await self.mcp_client_session.list_tools()

        print("Connected to server with tools:", [t.name for t in response.tools])

    async def list_tools(self):
        """List tools exposed by the connected MCP server"""

        if not self.mcp_client_session:
            raise RuntimeError("MCP client is not connected")

        # All MCP clients have list_tools()
        response = await self.mcp_client_session.list_tools()
        return response.tools

    def build_tool_selection_prompt(
        self,
        preprocessed_query: Dict[str, Any],
        tools: list,
    ) -> str:
        """
        Build a prompt that asks the LLM to select the most appropriate MCP tool(s)
        and arguments based on the structured query intent.
        """

        tool_descriptions = "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in tools]
        )

        prompt = f"""
            You are a routing assistant.

            Here is a query, and additional structured fields. 
            Based on this, and the tools available, you must decide which MCP tool or tools to call.

            QUERY + ADDITIONAL STRUCTURED FIELDS:
            {preprocessed_query}

            AVAILBE MCP TOOLS AVAILABLE:
            {tool_descriptions}

            Rules:
            - Only select from the available MCP tools listed above
            - Use only the fields present in the structured query
            - Do not invent values
            - If no tool is appropriate, return an empty list

            Return your answer strictly as JSON in the following format:

            [
            {{
                "tool_name": "<tool name>",
                "arguments": {{
                "<arg_name>": "<value>"
                }}
            }}
            ]
            """

        return prompt

    async def select_tools_with_llm(self, prompt: str) -> str:
        """
        Send the tool-selection prompt to the LLM and return the raw response.
        The response is expected to be JSON describing which MCP tools to call.
        """

        # issue here is original query is in prompt and so empty films overridden by LLM
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "You are a precise tool-routing assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,  # REDUCE HALLUCINATIONS
        )

        # Return raw text for downstream parsing
        return response.output_text
