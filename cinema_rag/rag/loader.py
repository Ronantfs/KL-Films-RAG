import json
from pathlib import Path

def load_raw_listings(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


