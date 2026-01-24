from typing import TypedDict
from enum import Enum
from typing import TypedDict

CINEMAS = [
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


class CinemaName(str, Enum):
    BARBICAN = "barbican"
    BFI_SOUTHBANK = "bfi_southbank"
    CASTLE = "castle"
    NICKEL = "nickel"
    CLOSE_UP = "close_up"
    CINE_LUMIERE = "cine_lumiere"
    THE_CINEMA_MUSEUM = "the_cinema_museum"
    GARDEN_CINEMA = "garden_cinema"
    RIO = "rio"
    ICA = "ica"


class FilmDetails(TypedDict):
    description: str
    screen: str
    screeningType: str
    url: str
    when: list[dict]
    runtime: str


CinemaListings = dict[str, FilmDetails]
RawCinemaFilms = dict[CinemaName, CinemaListings]
