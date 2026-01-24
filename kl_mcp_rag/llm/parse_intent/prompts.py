from enum import Enum
from kl_mcp_rag.constants_and_types.listings import CINEMAS, CinemaName

V1_0 = f"""
You will be given a query relating to film showings at select cinemas. 
Queries havew three fields you will need to extract:

Fields:
- cinemas: list[string]
- date_expression: string
- film_mention: string
 
Extract fields and output JSON only.

Valid cinemas in my data:
{[c.value for c in CinemaName]}

Guidance:
CINEMAS LIST:
- If it ambiguous which cinema is being refered to, but one is clearly being mentioned, assume query means all cinemas that are valid in my data,
   cinemas field should then be returned as an arry with all valiid cinema names")
- The query might also not mention any Cinema at all, in which case return empty array for cinemas.

DATE EXPRESSION:
- If no date expression is mentioned, return emtpy string for date_expression.
- Date expressions can be linguistic ("next weekend") or numerical ("25th December 2023") or mixed ("in 2 days time").

Examples: 
Query: "Is Star Wars showing at a cinema next weekend?"
{{
  "cinemas": ["barbican","bfi_southbank","castle", "nickel", "close_up","cine_lumiere","the_cinema_museum","garden_cinema","rio","ica"],
  "date_expression": "next weekend",
  "film_mention": "Star Wars"
}}
"""


class PromptVersions(str, Enum):
    V1_0 = V1_0
