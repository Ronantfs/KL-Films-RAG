from typing import Optional
from openai import OpenAI
from kl_mcp_rag.constants_and_types.pipeline import Intent
from kl_mcp_rag.constants_and_types.listings import CINEMAS
import json

from kl_mcp_rag.llm.parse_intent.parser_versions import ParseIntentVersion


# TODO:
# how to handle multiple films and single films?
# dates with gaps (next "wednesday and friday not thursday")?
# ambiguous cinemas ("the cinema")?
# TODO: raise custom exception
# todo: test no cinema vs all cinemas


def _validate_cinemas(cinemas: Optional[list[str]]) -> None:
    """Validate that the cinemas list contains only valid cinema names."""
    assert isinstance(cinemas, list)
    for cinema in cinemas:
        assert isinstance(cinema, str)
        # need to think how I want to handle cases where the cinema is str not in my db
        # do I want to assert this here?
        assert cinema in CINEMAS


# todo add error handling
def validate_intent(data: dict) -> Intent:
    # data likly typed as Intent, this function enforces that with assertions
    assert isinstance(data, dict)

    # required keys
    assert set(data.keys()) == {
        "cinemas",
        "date_expression",
        "film_mention",
    }

    # TODO: need to think about what I want to eonforce for cinemas at this point
    _validate_cinemas(data.get("cinemas"))

    # type validation
    assert isinstance(data["date_expression"], Optional[str])
    assert isinstance(data["film_mention"], Optional[str])

    validated_data: Intent = data  # type: ignore
    return validated_data


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

    pre_validated_data: dict = json.loads(resp.choices[0].message.content)  # type: ignore
    data: Intent = validate_intent(pre_validated_data)

    return data


# TODO: add handling for multiple intents in one query
# or user feedback for restricting flow to one query -- have a think which is best
# for the moment we assume single queries, with all fields required (dates, cinema, film)
# This is a very limited set of queries but good for intial e2e dev
