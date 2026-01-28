import asyncio
import os
from kl_mcp_rag.rag.index import FilmIndex
from kl_mcp_rag.llm.parse_intent.parser import parse_intent, validate_intent
from kl_mcp_rag.llm.parse_dates.parse_dates import parse_dates
from kl_mcp_rag.rag.resolve_film import resolve_film_title
from kl_mcp_rag.rag.index import openai_embed
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

from kl_mcp_rag.constants_and_types.pipeline import Intent, QueryDetails

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from kl_mcp_rag.llm.parse_intent.parser_versions import (
    PARSE_INTENT_VERSIONS,
    ParseIntentVersion,
)

CUR_PARSE_INTENT_VERSION = "pi_v1.1"


# TODO: major improvement to reduce hallucinations is to return Typed intent:
# by this I mean ...
# (Preprocessor filters tool candidates)
def extract_query_details(query: str) -> QueryDetails:
    """
    Deterministic preprocessing before MCP call:
    """

    parse_intent_version: ParseIntentVersion = PARSE_INTENT_VERSIONS[
        CUR_PARSE_INTENT_VERSION
    ]

    intent: Intent = parse_intent(parse_intent_version, client, query)
    # TODO: add error handling

    # enforced: [yyyy-mm-dd, ...]
    dates: list[str] = parse_dates(intent["date_expression"])

    index = FilmIndex(embed_fn=openai_embed)

    film_title = (
        resolve_film_title(intent["film_mention"], index)
        if intent.get("film_mention")
        else None
    )

    # Hand-off object to MCP for tool execution
    processed_details: QueryDetails = {
        "raw_query": query,
        "cinemas": intent["cinemas"],
        "dates": dates,
        "matched_film_title": film_title,
        "raw_user_film_title": intent["film_mention"],
    }

    return processed_details
