from typing import TypedDict, List

ALL_CINEMAS = [
    "barbican",
    "bfi_southbank",
    "castle",
    "nickel",
    "close_up",
    "cine_lumiere",
    "the_cinema_museum",
    "garden_cinema",
    "rio",
    "ica",
]


class ExpectedIntent(TypedDict):
    cinemas: List[str]
    date_expression: str
    film_mention: str


class IntentTestCase(TypedDict):
    id: str
    query: str
    test_label: str
    expected: ExpectedIntent


TEST_CASES: list[IntentTestCase] = [
    {
        "id": "tc_001",
        "query": "Is Star Wars showing next weekend?",
        "test_label": "film + date, no cinema",
        "expected": {
            "cinemas": ALL_CINEMAS,
            "date_expression": "next weekend",
            "film_mention": "Star Wars",
        },
    },
    {
        "id": "tc_002",
        "query": "What films are on at the Barbican tomorrow?",
        "test_label": "cinema + date, no film",
        "expected": {
            "cinemas": ["barbican"],
            "date_expression": "tomorrow",
            "film_mention": "",
        },
    },
]
