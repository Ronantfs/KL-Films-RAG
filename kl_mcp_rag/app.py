from llm.parse_intent import parse_intent
from kl_mcp_rag.llm.parse_dates.parse_dates import parse_dates
from rag.resolve_film import resolve_film_title


# TODO: move to free open source models after cost calculation of e2e flow?


def handle_query(query: str) -> dict:
    """
    Returns a deterministic MCP-style tool call payload.
    No MCP client is invoked here.
    """

    # TODO: add handling for multiple intents in one query
    # or user feedback for restricting flow to one query -- have a think which is best
    # for the moment we assume single queries, with all fields required (dates, cinema, film)
    # This is a very limited set of queries but good for intial e2e dev
    # intent = parse_intent(query)
    # temp hard code for testing later parts of the flow
    intent = {
        "cinema": "barbican",
        "date_expression": "this or next weekend",
        "film_mention": "Sentimental Value",
    }

    # dates: list[str] = parse_dates(intent["date_expression"])
    # temp hard code for testing later parts of the flow
    dates = [
        "2026-01-23",
        "2026-01-24",
        "2026-01-25",
        "2026-01-30",
        "2026-01-31",
        "2026-02-01",
    ]
    print(0)

    film_title = (
        resolve_film_title(intent["film_mention"])
        if intent.get("film_mention")
        else None
    )

    # This is the *final output* of your system at this stage
    return {
        "tool": "search_film",
        "arguments": {
            "cinema": intent.get("cinema"),
            "dates": dates,
            "film_title": film_title,
        },
    }


if __name__ == "__main__":
    test_queries = [
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
