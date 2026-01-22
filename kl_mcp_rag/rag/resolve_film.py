from pathlib import Path
from rag.index import FilmIndex
from rag.build_index import build_index

# Paths
RAG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RAG_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

INDEX_PATH = DATA_DIR / "films.idx"
THRESHOLD = 0.80


def _TEST_film_look_up(
    test_titles: list[str],
    RAW_TEST_DATA_PATH: Path,
    INDEX_PATH: Path,
):

    if not INDEX_PATH.exists():
        build_index()

    index = FilmIndex.load(INDEX_PATH)

    for title in test_titles:
        resolved = resolve_film_title(title)
        print(f"Input: {title} -> Resolved: {resolved}")


def TEMP_film_test_lookup():

    film_titles = [
        "Sentimental Value",
        "Marty Supreme",
        "Nonexistent Film Title",
        "2001",
        "space odesy",  #
    ]


def resolve_film_title(raw_text: str) -> str | None:
    if not INDEX_PATH.exists():
        build_index()

    # vecDB load
    index = FilmIndex.load(INDEX_PATH)

    score, meta = index.search(raw_text, k=1)[0]
    return meta["title"] if score >= THRESHOLD else None
