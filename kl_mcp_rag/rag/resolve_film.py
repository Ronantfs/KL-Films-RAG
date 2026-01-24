from collections.abc import Callable
from pathlib import Path, PosixPath

import numpy as np
from kl_mcp_rag.rag.index import FilmIndex, openai_embed
from kl_mcp_rag.rag.build_index import build_index


# Paths
PACKAGE_ROOT = Path(__file__).resolve().parents[1]  # kl_mcp_rag
DATA_DIR = PACKAGE_ROOT / "data"

INDEX_BASE_PATH = DATA_DIR / "films"  # films.npz + films.json
npz_path = INDEX_BASE_PATH.with_suffix(".npz")
json_path = INDEX_BASE_PATH.with_suffix(".json")
# TODO: investigate calibration of threshold
THRESHOLD = 0.80


def resolve_film_title(raw_text: str, index: FilmIndex) -> str | None:
    if not npz_path.exists() or not json_path.exists():
        build_index(index)

    index.load_data(INDEX_BASE_PATH)

    score, meta = index.search(raw_text, k=1)[0]
    return meta["title"] if score >= THRESHOLD else None


# TODO: fix path issues so testing actual resolve_film_title function!
def evaluate_film_embedding_function(
    test_titles: list[str],
    # RAW_TEST_DATA_PATH: Path,
    TEST_INDEX_PATH: Path,
    index: FilmIndex,
):

    if not npz_path.exists() or not json_path.exists():
        build_index(index)

    index.load_data(TEST_INDEX_PATH)

    for test_title in test_titles:
        score, _ = index.search(test_title, k=1)[0]
        print(f"Query: {test_title} | Top score: {score:.4f}")


if __name__ == "__main__":
    ##### evaluate embedding apporaches
    test_film_titles = [
        "Sentimental Value",  # 0.886
        "Marty Supreme",  # 0.85
        "Nonexistent Film Title",  #  0.3932
        "2001",  # misspelled on purpose -> 0.41
        "space odesy",  # misspelled on purpose -> performs worse that expected
    ]

    TEST_INDEX_PATH = PosixPath(
        "/Users/ronantwomweyfriedlander/Desktop/code/KL/CV CODE REPOS/KL-Films-RAG/kl_mcp_rag/data/films.idx"
    )

    index = FilmIndex(embed_fn=openai_embed)

    evaluate_film_embedding_function(
        test_titles=test_film_titles,
        TEST_INDEX_PATH=TEST_INDEX_PATH,
        index=index,
    )
