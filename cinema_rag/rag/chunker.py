

# this is bad chunking as we miss out on having time information which is going to be key for queries.
def chunk_film_records(records: list[dict]) -> list[dict]:
    chunks = []

    for record in records:
        # Extract human-readable dates and times (simple version)
        screening_summaries = []
        for screening in record["screenings"]:
            day = screening["structured_date_strings"]["Weekday"]
            date_str = screening["structured_date_strings"]["day_str"]
            times = ", ".join(screening["showtimes"])
            screening_summaries.append(f"{day} {date_str} at {times}")

        screening_text = "; ".join(screening_summaries)

        text = (
            f"Film: {record['title']}. "
            f"Cinema: {record['cinema']}. "
            f"Showings: {screening_text}. "
            f"Runtime: {record['runtime']}. "
            f"Description: {record['description']}."
        )

        chunks.append({
            "text": text,
            "metadata": {
                "cinema": record["cinema"],
                "title": record["title"],
                "url": record["url"],
                # TODO: store structured date + showtime metadata for filtering (currently embedded only)
            }
        })

        # TODO: split into screening-level chunks (one per date) for improved recall
        # TODO: add time-of-day buckets (matinee / evening / late)
        # TODO: deduplicate long-running films across weeks
        
        # TODO: Add multiple chunk views that better semantically capcture different aspects of the data

    return chunks
