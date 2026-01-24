import os
from kl_mcp_rag.llm.parse_intent.parser import parse_intent
from kl_mcp_rag.llm.parse_dates.parse_dates import parse_dates
from kl_mcp_rag.rag.resolve_film import resolve_film_title
from kl_mcp_rag.rag.index import openai_embed
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from kl_mcp_rag.llm.parse_intent.parser_versions import (
    PARSE_INTENT_VERSIONS,
    ParseIntentVersion,
)


CUR_PARSE_INTENT_VERSION = "pi_v1.1"


# TODO: move to free open source models after cost calculation of e2e flow?
def handle_query(query: str) -> dict:
    """
    Returns a deterministic MCP-style tool call payload.
    No MCP client is invoked here.
    """

    parse_intent_version: ParseIntentVersion = PARSE_INTENT_VERSIONS[
        CUR_PARSE_INTENT_VERSION
    ]

    intent = parse_intent(parse_intent_version, client, query)

    dates: list[str] = parse_dates(intent["date_expression"])

    film_title = (
        resolve_film_title(intent["film_mention"], openai_embed)
        if intent.get("film_mention")
        else None
    )

    print(0)

    # This is the *final output* of your system at this stage
    return {
        "tool": "search_film",  # add MCP for tool intened and required keys
        "arguments": {
            "cinema": intent.get("cinema"),
            "dates": dates,
            "film_title": film_title,
        },
    }


if __name__ == "__main__":
    test_queries = [
        "Is Star Wars showing at a cinema next weekend?",
        "Is Sentimental Value playing at the Barbican this or next weekend?",
        "What films are on at the Barbican this weekend?",
        "Is Marty Supreme showing next week?",
    ]

    for q in test_queries:
        print("=" * 80)
        print("QUERY:", q)
        result = handle_query(q)
        print("OUTPUT:")
        print(result)
