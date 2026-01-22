from typing import TypedDict
from typing_extensions import Literal

CINEMAS = (
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
)

CinemaName = Literal[*CINEMAS]


class FilmDetails(TypedDict):
    description: str
    screen: str
    screeningType: str
    url: str
    when: list[dict]
    runtime: str


CinemaListings = dict[str, FilmDetails]
RawCinemaFilms = dict[CinemaName, CinemaListings]
