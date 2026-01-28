from typing import Any, Dict, List, Optional
from kl_mcp_rag.constants_and_types.listings import (
    CinemaListings,
    CinemaName,
    FilmDetails,
    Listing_When_Date,
    RawCinemaFilms,
)


def _filter_when_by_dates(
    when: List[Listing_When_Date],
    dates: List[str],
) -> List[Listing_When_Date]:
    return [w for w in when if w.get("date") in dates]


# short hand for functions: [cinemas: Optional[List[str]], films: str, dates: List[str]] = [c, f, d]
# [c,f,d] -- [c,f,_] -- [c,_,d] -- [c,_,_]


# cfd
def get_specific_showtimes(
    raw_listings: RawCinemaFilms,
    cinemas: List[CinemaName],  # we know cinema exists
    film: str,  # film exists at some cinema
    dates: List[str],  # yyyy-mm-dd
) -> str:
    lines = []

    for cinema in cinemas:
        cinema_films: CinemaListings = raw_listings.get(cinema, {})
        film_details: Optional[FilmDetails] = cinema_films.get(film)

        if not film_details:  # film not at this cinema on any date
            continue

        # is film showing on any of the requested dates?
        matched_when: list[Listing_When_Date] = _filter_when_by_dates(
            film_details["when"], dates
        )

        if matched_when:
            date_parts = []
            for d in matched_when:
                showtimes = ", ".join(d["showtimes"])  # HH:MM list
                date_parts.append(f"{d['date']} at {showtimes}")

            schedule = " | ".join(date_parts)

            lines.append(f"{film} is playing at {cinema}: {schedule}.")

    if not lines:
        return f"No showtimes found for {film} on the requested dates."

    return "\n".join(lines)


# c_d
def get_all_screenings_at_cinema_on_dates(
    raw_listings: RawCinemaFilms,
    cinemas: List[CinemaName],  # we know cinema exists
    dates: List[str],  # yyyy-mm-dd
) -> str:
    lines: list[str] = []

    for cinema in cinemas:
        cinema_films: CinemaListings = raw_listings.get(cinema, {})
        cinema_has_output = False

        for date in dates:
            film_lines: list[str] = []

            for film, film_details in cinema_films.items():
                matched_when: list[Listing_When_Date] = _filter_when_by_dates(
                    film_details["when"], [date]
                )

                if not matched_when:
                    continue

                showtimes = ", ".join(matched_when[0]["showtimes"])  # HH:MM list
                film_lines.append(f"- {film} is playing at {showtimes}")

            if film_lines:
                if not cinema_has_output:
                    lines.append(f"At {cinema}:")
                    cinema_has_output = True

                lines.append(f"  On {date}, the following are playing:")
                lines.extend(f"  {line}" for line in film_lines)
        lines.append("-- -- -- -- -- ")

    if not lines:
        return f"There are no screenings at {cinemas} on those dates 😭 )"

    return "\n".join(lines)


# cf_
def get_dates_for_film_at_cinema(
    raw_listings: RawCinemaFilms,
    cinemas: List[CinemaName],  # we know cinema exists
    film: str,  # film exists at some cinema
) -> str:
    lines: list[str] = []

    for cinema in cinemas:
        cinema_films: CinemaListings = raw_listings.get(cinema, {})
        film_details: Optional[FilmDetails] = cinema_films.get(film)

        if not film_details:
            continue

        when_list: list[Listing_When_Date] = film_details["when"]

        if not when_list:
            continue

        lines.append(f"{film} is screening at {cinema} on the following dates:")

        for d in when_list:
            showtimes = ", ".join(d["showtimes"])  # HH:MM list
            lines.append(f"{d['date']}: {showtimes}")
        lines.append("-- -- -- -- -- ")

    if not lines:
        return f"No screenings found for {film} at the {cinemas}."

    return "\n".join(lines)


# c__
def get_all_listings_for_cinema(
    raw_listings: RawCinemaFilms,
    cinemas: List[CinemaName],  # we know cinema exists
) -> str:
    lines: list[str] = []

    for cinema in cinemas:
        cinema_films: CinemaListings = raw_listings.get(cinema, {})

        if not cinema_films:
            continue

        lines.append(f"The following films are playing at {cinema}:")

        for film, film_details in cinema_films.items():
            when_list: list[Listing_When_Date] = film_details.get("when", [])

            if not when_list:
                continue

            dates = ", ".join(d["date"] for d in when_list)
            lines.append(f"{film}: {dates}")
        lines.append("-- -- -- -- -- ")

    if not lines:
        return "No listings found for the requested cinemas."

    return "\n".join(lines)


# _fd
def get_cinemas_for_film_and_dates(
    raw_listings: RawCinemaFilms,
    film: str,  # film may exist at some cinemas
    dates: List[str],  # yyyy-mm-dd
) -> str:
    lines: list[str] = []

    for date in dates:
        cinemas_playing: list[str] = []

        for cinema, cinema_films in raw_listings.items():
            film_details: Optional[FilmDetails] = cinema_films.get(film)

            if not film_details:
                continue

            matched_when: list[Listing_When_Date] = _filter_when_by_dates(
                film_details["when"], [date]
            )

            if matched_when:
                cinemas_playing.append(cinema)

        if cinemas_playing:
            cinemas_str = ", ".join(cinemas_playing)
            lines.append(f"On {date}, {film} is playing at: {cinemas_str}.")
        else:
            lines.append(f"On {date}, {film} is not playing at any listed cinema.")
        lines.append("-- -- -- -- -- ")
    if not lines:
        return f"No listings found for {film} on the requested dates."

    return "\n".join(lines)


# ___
def handle_no_params_from_user() -> Any:
    return {"message": "Ask about films, cinemas, or dates to see Kinologue Listings."}


########################################################
# ---- pre-routing validation ----
def handle_requested_film_not_on(raw_film: str) -> str:
    return f'"{raw_film}" is not screening anywhere'
