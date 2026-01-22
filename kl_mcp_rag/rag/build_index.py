import json
from pathlib import Path
from kl_mcp_rag.constants_and_types.listings import RawCinemaFilms
from rag.index import FilmIndex

# Paths
RAG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RAG_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

RAW_PATH = DATA_DIR / "raw_listings.json"
OUT_PATH = DATA_DIR / "films.idx"


def film_to_embedding_text(title: str) -> str:
    """
    Structured film fields -> film record into the canonical text for RAG embeddings.
    """

    return f"Title: {title}".strip()
    # todo: maybe add description?


def extract_unique_film_titles(raw: RawCinemaFilms) -> set[str]:
    return {title for films_by_title in raw.values() for title in films_by_title.keys()}


# add a handler so we can control the building of vector store so can run updates
# also given embeddings are non-neglibible cost, think about a caching layer:
# do we need to re-embed films that we all ready in out database?
# however, we want it to be smart because don;t want vector store to grow unboundedly
def build_index() -> None:
    index = FilmIndex()

    with open(RAW_PATH) as f:
        raw: RawCinemaFilms = json.load(f)

    # minor optimization: only embed unique film titles
    unique_titles = extract_unique_film_titles(raw)

    for title in unique_titles:
        text = film_to_embedding_text(title=title)
        index.add(text=text, meta={"title": title})
        print(f"Added to index: {title}")

    index.save(OUT_PATH)


if __name__ == "__main__":
    build_index()
