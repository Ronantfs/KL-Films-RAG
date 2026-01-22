from openai import OpenAI
from kl_mcp_rag.constants_and_types.listings import CINEMAS
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = f"""
Extract fields and output JSON only.

Valid cinemas:
{CINEMAS}

Fields:
- cinema: string or null
- date_expression: string or null
- film_mention: string or null 
"""

# TODO:
# how to handle multiple films and single films?
# dates with gaps (next "wednesday and friday not thursday")?
# ambiguous cinemas ("the cinema")?
# multiple queries in one: When is x playing at brican and when is y playing at the globe?


def parse_intent(query: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": query},
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(resp.choices[0].message.content)  # type: ignore

    # --- assertions (deterministic guardrails) ---
    assert isinstance(data, dict)

    # required keys
    # later theree will be intents that do not have all keys
    assert set(data.keys()) == {
        "cinema",
        "date_expression",
        "film_mention",
    }

    # cinema validation
    # TODO: raise custom exception
    assert data["cinema"] is None or data["cinema"] in CINEMAS

    # type validation

    assert data["date_expression"] is None or isinstance(data["date_expression"], str)
    assert data["film_mention"] is None or isinstance(data["film_mention"], str)

    return data
