from collections.abc import Callable
import argparse
import json
import os
from pathlib import Path
from typing import Any, Optional

import boto3
import numpy as np
from kl_mcp_rag.constants_and_types.listings import RawCinemaFilms
from kl_mcp_rag.rag.index import FilmIndex, openai_embed


# Paths
PACKAGE_ROOT = Path(__file__).resolve().parents[1]  # kl_mcp_rag
DATA_DIR = PACKAGE_ROOT / "data"

RAW_PATH = DATA_DIR / "raw_listings.json"  # input (optional override)
INDEX_BASE_PATH = DATA_DIR / "films"  # output base (no suffix)


# TODO: move to common utils as duplication with main system handler:


BASE_DIR = Path(__file__).resolve().parents[1]  # kl_mcp_rag/
DATA_DIR = BASE_DIR / "data"


def _get_s3_client():
    AWS_REGION = "eu-north-1"
    AWS_PROFILE = "ronantfs"
    # AWS Lambda sets this automatically
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return boto3.client("s3", region_name=AWS_REGION)
    else:
        session = boto3.Session(
            profile_name=AWS_PROFILE,
            region_name=AWS_REGION,
        )
        return session.client("s3")


def _resolve_raw_listings_path(filename: str) -> Path:
    """
    Resolve a raw listings filename to an absolute path.

    Expectation:
    - filename ONLY (e.g. 'raw_listings_v1.json')
    - file must exist in kl_mcp_rag/data/
    """
    if "/" in str(filename) or "\\" in str(filename):
        raise ValueError(f"Expected filename only, got path-like value: {filename}")

    path = (DATA_DIR / filename).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Raw listings file not found: {path}")

    return path


def _load_raw_listings(path: Optional[Path]) -> Any:

    # No path: load from live s3 data
    if path is None:
        s3_client = _get_s3_client()
        raw_listings_bucket = "filmfynder"
        raw_listings_key = "london/cinema-listings/all/active_listings.json"
        print("LOADING PROD RAW LISTINGS FROM S3")
        prod_raw_listings_obj = s3_client.get_object(
            Bucket=raw_listings_bucket, Key=raw_listings_key
        )
        prod_raw_listings_json = json.loads(
            prod_raw_listings_obj["Body"].read().decode("utf-8")
        )

        return prod_raw_listings_json

    # Load from provided path
    with path.open("r") as f:
        return json.load(f)


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
def build_index(
    index: FilmIndex,
    raw_path: Optional[Path] = None,  # backward-compatible default
) -> None:
    """
    Canonical index builder.

    - If raw_path is None (default), raw listings are loaded from S3
    - If raw_path is provided, raw listings are loaded from disk
    """

    raw: RawCinemaFilms = _load_raw_listings(raw_path)

    # minor optimization: only embed unique film titles
    unique_titles = extract_unique_film_titles(raw)

    for title in unique_titles:
        text: str = film_to_embedding_text(title=title)
        index.add(text=text, meta={"title": title})
        print(f"Added to index: {title}")

    index.save(INDEX_BASE_PATH)


def main() -> None:
    # CLI-only entry point
    parser = argparse.ArgumentParser(description="Build film RAG index")
    parser.add_argument(
        "--raw-path",
        type=Path,
        required=False,
        help="Path to raw listings JSON (if omitted, loads from S3)",
    )

    args = parser.parse_args()

    index = FilmIndex(embed_fn=openai_embed)

    raw_path = _resolve_raw_listings_path(args.raw_path) if args.raw_path else None
    build_index(index=index, raw_path=raw_path)


if __name__ == "__main__":
    main()
