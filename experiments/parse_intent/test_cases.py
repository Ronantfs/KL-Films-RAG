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
    {
        "id": "tc_003",
        "query": "Is anything showing at the Barbican?",
        "test_label": "cinema only, no date, no film",
        "expected": {
            "cinemas": ["barbican"],
            "date_expression": "",
            "film_mention": "",
        },
    },
    {
        "id": "tc_004",
        "query": "Is Sentimental Value playing tonight?",
        "test_label": "film + date, no cinema",
        "expected": {
            "cinemas": ALL_CINEMAS,
            "date_expression": "tonight",
            "film_mention": "Sentimental Value",
        },
    },
    {
        "id": "tc_005",
        "query": "What’s on this weekend?",
        "test_label": "date only, fully ambiguous cinema + film",
        "expected": {
            "cinemas": ALL_CINEMAS,
            "date_expression": "this weekend",
            "film_mention": "",
        },
    },
    {
        "id": "tc_006",
        "query": "Are there any screenings of Marty Supreme at the BFI Southbank?",
        "test_label": "film + cinema, no date",
        "expected": {
            "cinemas": ["bfi_southbank"],
            "date_expression": "",
            "film_mention": "Marty Supreme",
        },
    },
    {
        "id": "tc_007",
        "query": "What films are showing tomorrow at the ICA and the Garden Cinema?",
        "test_label": "multiple cinemas + date",
        "expected": {
            "cinemas": ["ica", "garden_cinema"],
            "date_expression": "tomorrow",
            "film_mention": "",
        },
    },
    {
        "id": "tc_008",
        "query": "Is anything good on next Friday?",
        "test_label": "date only, vague language",
        "expected": {
            "cinemas": ALL_CINEMAS,
            "date_expression": "next Friday",
            "film_mention": "",
        },
    },
    {
        "id": "tc_009",
        "query": "Is Star Wars on at the Rio or Close-Up?",
        "test_label": "film + multiple cinemas, no date",
        "expected": {
            "cinemas": ["rio", "close_up"],
            "date_expression": "",
            "film_mention": "Star Wars",
        },
    },
    {
        "id": "tc_010",
        "query": "What’s playing at the cinema museum this Saturday?",
        "test_label": "cinema alias + date",
        "expected": {
            "cinemas": ["the_cinema_museum"],
            "date_expression": "this Saturday",
            "film_mention": "",
        },
    },
    {
        "id": "tc_011",
        "query": "Is Sentimental Value showing anywhere?",
        "test_label": "film only, implicit all cinemas",
        "expected": {
            "cinemas": ALL_CINEMAS,
            "date_expression": "",
            "film_mention": "Sentimental Value",
        },
    },
    {
        "id": "tc_012",
        "query": "Are there any films on at Castle and Nickel next week?",
        "test_label": "multiple cinemas + date, no film",
        "expected": {
            "cinemas": ["castle", "nickel"],
            "date_expression": "next week",
            "film_mention": "",
        },
    },
    {
        "id": "tc_013",
        "query": "What’s on at the Barbican on the 25th of December?",
        "test_label": "cinema + explicit date",
        "expected": {
            "cinemas": ["barbican"],
            "date_expression": "25th of December",
            "film_mention": "",
        },
    },
    {
        "id": "tc_014",
        "query": "Is anything showing?",
        "test_label": "fully underspecified query",
        "expected": {
            "cinemas": ALL_CINEMAS,
            "date_expression": "",
            "film_mention": "",
        },
    },
    {
        "id": "tc_015",
        "query": "Are there screenings of Sentimental Value and Star Wars this weekend?",
        "test_label": "multiple films mentioned (known limitation)",
        "expected": {
            "cinemas": ALL_CINEMAS,
            "date_expression": "this weekend",
            "film_mention": "Sentimental Value, Star Wars",
        },
    },
    {
        "id": "tc_016",
        "query": "What films are on at the BFI?",
        "test_label": "cinema shorthand / partial name",
        "expected": {
            "cinemas": ["bfi_southbank"],
            "date_expression": "",
            "film_mention": "",
        },
    },
    {
        "id": "tc_017",
        "query": "Is Marty Supreme playing at Barbican this evening?",
        "test_label": "film + cinema + colloquial date",
        "expected": {
            "cinemas": ["barbican"],
            "date_expression": "this evening",
            "film_mention": "Marty Supreme",
        },
    },
]
