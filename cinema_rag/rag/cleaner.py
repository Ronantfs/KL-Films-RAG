
# collapsing nested JSON into retrieval-friendly records.
# why? what is the benefit of this approach? 
def normalize_listings(raw_data: dict) -> list[dict]:
    normalized = []

    for cinema, films in raw_data.items():
        for title, details in films.items():
            normalized.append({
                "cinema": cinema.lower(),
                "title": title,
                "description": details.get("description", "").strip(),
                "runtime": details.get("runtime"),
                "screenings": details.get("when", []),  # TODO: flatten into per-date records for better time-based retrieval
                "url": details.get("url")
            })

    return normalized


# todo: add typing to this collaped data 
