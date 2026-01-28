from kl_mcp_rag.constants_and_types.listings import CinemaName


from typing import List, TypedDict, Optional


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Query Pre processor
# # # # # # # # # # # # # # # # # # # # # # # # # # #
class QueryDetails(TypedDict):
    raw_query: str
    cinemas: Optional[list[CinemaName]]
    dates: Optional[list[str]]
    matched_film_title: Optional[str]
    raw_user_film_title: Optional[str]


class Intent(TypedDict):
    cinemas: Optional[List[str]]
    date_expression: Optional[str]
    film_mention: Optional[str]
