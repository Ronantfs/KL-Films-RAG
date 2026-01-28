import asyncio

from typing import Any, Dict

from custom_types.pipeline import QueryDetails
from kl_mcp_rag.query_pre_processor import extract_query_details


from kl_mcp_rag.mcp_server.client import MCPClient


async def handle_user_query(
    user_query: str,
) -> Any:
    """
    Orchestrates the full query → MCP tool execution flow.

    Flow:
    1. Preprocess natural language query
    2. Fetch available MCP tools
    3. Ask LLM which tool(s) to call
    4. Execute selected tool(s)
    5. Return tool results
    """

    # 1. Preprocess query into structured intent
    """
    think about if I want tool choosing to be LLM determined or determinstic based off logic for parsed parameters
    or some mix or both --> defo some determinism I can noarrow down tool choice before LLM call to help with decsions
    e.g. no date -> exclusdes some look ups ;
    but some combintationbs of extracted aprams might not be deterministic
    """
    preprocessed_query: QueryDetails = extract_query_details(user_query)

    mcp_client = MCPClient()
    await mcp_client.connect_to_mcp_server()

    # 2. Fetch available tools from MCP server
    available_tools = await mcp_client.list_tools()

    # 3. Build prompt for LLM tool selection
    prompt: str = mcp_client.build_tool_selection_prompt(
        preprocessed_query=preprocessed_query,
        tools=available_tools,
    )

    # 4. Ask LLM which tools to call
    llm_response = await mcp_client.select_tools_with_llm(prompt)

    print(1)
    # # 5. Parse LLM response into executable tool calls
    # tool_calls: List[Dict[str, Any]] = mcp_client.parse_llm_tool_selection(
    #     llm_response=llm_response,
    #     preprocessed_query=preprocessed_query,
    # )

    # # 6. Execute selected MCP tools
    # tool_results = await mcp_client.execute_selected_tools(tool_calls)

    # # 7. Return raw tool results (or aggregate later if desired)
    # return tool_results


async def main():
    user_query = "Is Inception showing at the ICA this week?"

    result = await handle_user_query(user_query)


if __name__ == "__main__":
    asyncio.run(main())
