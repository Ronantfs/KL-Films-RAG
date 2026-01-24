from collections.abc import Callable
import json
from pathlib import Path

import numpy as np
from kl_mcp_rag.constants_and_types.listings import RawCinemaFilms
from kl_mcp_rag.rag.index import FilmIndex, openai_embed

# Paths
PACKAGE_ROOT = Path(__file__).resolve().parents[1]  # kl_mcp_rag
DATA_DIR = PACKAGE_ROOT / "data"


RAW_PATH = DATA_DIR / "raw_listings.json"  # input
INDEX_BASE_PATH = DATA_DIR / "films"  # output base (no suffix)


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
def build_index(index: FilmIndex) -> None:

    with open(RAW_PATH) as f:
        raw: RawCinemaFilms = json.load(f)

    # minor optimization: only embed unique film titles
    unique_titles = extract_unique_film_titles(raw)

    for title in unique_titles:
        text: str = film_to_embedding_text(title=title)
        index.add(text=text, meta={"title": title})
        print(f"Added to index: {title}")

    index.save(INDEX_BASE_PATH)
