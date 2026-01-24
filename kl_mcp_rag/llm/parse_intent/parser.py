from openai import OpenAI
from kl_mcp_rag.constants_and_types.listings import CINEMAS, CinemaName
import json

from typing import TypedDict, List

from kl_mcp_rag.llm.parse_intent.parser_versions import ParseIntentVersion


class Intent(TypedDict):
    cinemas: List[CinemaName]
    date_expression: str
    film_mention: str


# TODO:
# how to handle multiple films and single films?
# dates with gaps (next "wednesday and friday not thursday")?
# ambiguous cinemas ("the cinema")?
# TODO: raise custom exception
# todo: test no cinema vs all cinemas
def _validate_cinemas(cinemas: list[str]) -> None:
    """Validate that the cinemas list contains only valid cinema names."""
    assert isinstance(cinemas, list)
    for cinema in cinemas:
        assert isinstance(cinema, str)
        assert cinema in CINEMAS


# todo add error handling
def validate_intent(data: Intent) -> None:
    # --- assertions (deterministic guardrails) ---
    assert isinstance(data, dict)

    # required keys
    assert set(data.keys()) == {
        "cinemas",
        "date_expression",
        "film_mention",
    }

    _validate_cinemas(data["cinemas"])

    # type validation
    assert data["date_expression"] is None or isinstance(data["date_expression"], str)
    assert data["film_mention"] is None or isinstance(data["film_mention"], str)


# "gpt-4.1-mini"
# SYSTEM
def parse_intent(
    parse_intent_version: ParseIntentVersion, client: OpenAI, query: str
) -> Intent:
    resp = client.chat.completions.create(
        model=parse_intent_version["model_version"],
        messages=[
            {"role": "system", "content": parse_intent_version["prompt_version"]},
            {"role": "user", "content": query},
        ],
        response_format={"type": "json_object"},
    )

    data: Intent = json.loads(resp.choices[0].message.content)  # type: ignore

    return data


# TODO: add handling for multiple intents in one query
# or user feedback for restricting flow to one query -- have a think which is best
# for the moment we assume single queries, with all fields required (dates, cinema, film)
# This is a very limited set of queries but good for intial e2e dev
