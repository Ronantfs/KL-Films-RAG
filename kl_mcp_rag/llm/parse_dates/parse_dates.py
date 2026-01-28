import json
import os
from datetime import date
from typing import Optional
from openai import OpenAI
from kl_mcp_rag.llm.parse_dates.utils import (
    build_system_prompt,
    validate_dates,
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Empircally derived system prompt for date parsing
SYSTEM = build_system_prompt(date.today())


def parse_dates(expr: Optional[str]) -> list[str]:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"""
                            Date expression: {expr}
                            """,
            },
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(resp.choices[0].message.content)  # type: ignore

    validate_dates(data)

    return data["dates"]
