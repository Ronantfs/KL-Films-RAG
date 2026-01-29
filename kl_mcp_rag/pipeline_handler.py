import asyncio
import argparse
import os
import json
from pathlib import Path
from typing import Any

from kl_mcp_rag.constants_and_types.listings import RawCinemaFilms
from kl_mcp_rag.constants_and_types.pipeline import QueryDetails
from kl_mcp_rag.determinisitic_lookups.lookup_router import route_query
from kl_mcp_rag.query_pre_processor import extract_query_details

# from kl_mcp_rag.mcp_server.client import MCPClient

BASE_DIR = Path(__file__).resolve().parent  # kl_mcp_rag/
DATA_DIR = BASE_DIR / "data"

# static for testing
V1_TEST_RAW_LISTINGS_PATH = BASE_DIR / "data" / "raw_listings_v1.json"
# PRODUCTION
RAW_LISTINGS_PATH = BASE_DIR / "data" / "raw_listings_v1.json"


def resolve_raw_listings_file(filename: str) -> Path:
    """
    Resolve a raw listings filename to an absolute path.

    Expectation:
    - filename ONLY (e.g. 'v1_test_raw_listings.json')
    - file must exist in kl_mcp_rag/data/

    Raises early and loudly if the contract is violated.
    """
    if "/" in filename or "\\" in filename:
        raise ValueError(f"Expected filename only, got path-like value: {filename}")

    path = (DATA_DIR / filename).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Raw listings file not found: {path}")

    return path


def _load_raw_listings(path: Path) -> Any:
    with path.open("r") as f:
        return json.load(f)


async def handle_user_query(
    user_query: str,
    raw_listings_path: Path,
) -> Any:
    """
    Orchestrates the full query execution flow.

    Flow:
    1. Preprocess natural language query and extract structured parameters.
    2. Determine which tool to call determinstically
    3. Call lookup tool with extracted parameters on kinologue data.
    """

    # 1. Preprocess query into structured intent
    preprocessed_query: QueryDetails = extract_query_details(user_query)

    raw_listings: RawCinemaFilms = _load_raw_listings(path=raw_listings_path)

    look_up_return: str = route_query(
        q=preprocessed_query,
        raw_listings=raw_listings,
    )

    print(look_up_return)
    return look_up_return


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-query", required=True)  # injected query text
    parser.add_argument("--raw-listings-path", required=True)  # injected json path
    return parser.parse_args()


def cli_entrypoint():
    args = _parse_args()
    raw_path = resolve_raw_listings_file(args.raw_listings_path)
    asyncio.run(
        handle_user_query(
            user_query=args.user_query,
            raw_listings_path=raw_path,
        )
    )


def lambda_handler(event, context):
    user_query = event.get("user_query") or os.environ["USER_QUERY"]
    filename = event.get("raw_listings_path") or os.environ["RAW_LISTINGS_PATH"]
    raw_path = resolve_raw_listings_file(filename)

    return asyncio.run(
        handle_user_query(
            user_query=user_query,
            raw_listings_path=raw_path,
        )
    )


if __name__ == "__main__":
    cli_entrypoint()

# e2e test queries: V1_TEST_RAW_LISTINGS_PATH for raw listings (only 18th/19th Jan data)
# matches correct look up function in each case
# look up working as expected

# cfd
# user_query = "Is Sentimental Value showing at the ICA or barbicn on 18th Jan?" ✅✅

# c_d
# user_query = "what is on at BFI, ica, closeUP 17th and 18th Jan" ✅✅
# user_query = "what is on at BFI, ica, closeUP 25 feb" ✅✅ (fake date)

# cf_
# user_query = when is Sentimental Value at ica or barbican? ✅✅

# c__
# user_query = What is on at BFI and ICA? ✅✅

# see v3.0 docs for why these are only cases for this system.
