from typing import Any
from kl_mcp_rag.constants_and_types.listings import RawCinemaFilms
from kl_mcp_rag.determinisitic_lookups.lookups import (
    get_specific_showtimes,
    get_all_screenings_at_cinema_on_dates,
    get_dates_for_film_at_cinema,
    handle_no_params_from_user,
    handle_requested_film_not_on,
)
from kl_mcp_rag.constants_and_types.pipeline import QueryDetails


def route_query(
    q: QueryDetails,
    raw_listings: RawCinemaFilms,
) -> Any:
    cinemas = q["cinemas"]
    dates = q["dates"]
    film = q["matched_film_title"]
    raw_film = q["raw_user_film_title"]

    has_cinemas = bool(cinemas)
    has_dates = bool(dates)
    has_film = film is not None
    has_raw_film = bool(raw_film)

    if has_raw_film and not has_film:
        return handle_requested_film_not_on(raw_film)

    match (has_cinemas, has_film, has_dates):
        # cfd
        case (True, True, True):
            return get_specific_showtimes(
                raw_listings,
                cinemas=cinemas,  # type: ignore
                film=film,  # type: ignore
                dates=dates,  # type: ignore
            )

        # c_d
        case (True, False, True):
            return get_all_screenings_at_cinema_on_dates(
                raw_listings,
                cinemas=cinemas,  # type: ignore
                dates=dates,  # type: ignore
            )

        # cf_
        case (True, True, False):
            return get_dates_for_film_at_cinema(
                raw_listings,
                cinemas=cinemas,  # type: ignore
                film=film,  # type: ignore
            )

        # ___
        case (False, False, False):
            return handle_no_params_from_user()
