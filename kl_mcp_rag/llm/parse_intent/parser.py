from typing import Optional
from openai import OpenAI
from kl_mcp_rag.constants_and_types.pipeline import Intent
from kl_mcp_rag.constants_and_types.listings import CINEMAS, CinemaName
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

    _validate_cinemas(data.get("cinemas"))

    # type validation
    assert isinstance(data["date_expression"], Optional[str])
    assert isinstance(data["film_mention"], Optional[str])

    validated_data: Intent = data  # type: ignore
    return validated_data


def _apply_cinema_defaults(intent: dict) -> dict:
    has_cinemas = bool(intent.get("cinemas"))
    has_date = bool(intent.get("date_expression"))
    has_film = bool(intent.get("film_mention"))

    # edge case: no params at all -> leave cinemas empty
    if not has_cinemas and not has_date and not has_film:
        return intent

    # otherwise: empty cinemas means "all cinemas"
    if not has_cinemas:
        intent["cinemas"] = [c.value for c in CinemaName]

    return intent


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
    pre_validated_data = _apply_cinema_defaults(pre_validated_data)

    data: Intent = validate_intent(pre_validated_data)

    return data


# TODO: add handling for multiple intents in one query
# or user feedback for restricting flow to one query -- have a think which is best
# for the moment we assume single queries, with all fields required (dates, cinema, film)
# This is a very limited set of queries but good for intial e2e dev
