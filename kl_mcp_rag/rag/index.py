import json
from pathlib import Path
from typing import Callable
import numpy as np
from openai import OpenAI

client = OpenAI()


# This is slow, looking optimisations:
# concurrent calls with openai batching?
# not run on every query of system - have it run manually with a cli call (eventually linked to  updates of raw data)
# also consider switch to open source embedding model as this is simple vector store
def openai_embed(text: str) -> np.ndarray:
    vec = np.array(
        client.embeddings.create(model="text-embedding-3-small", input=text)
        .data[0]
        .embedding
    )
    return vec / np.linalg.norm(
        vec
    )  # 🔑 see notes on embeddings for why cosine over dot product


class FilmIndex:
    def __init__(self, embed_fn: Callable[[str], np.ndarray]):
        self.vectors = []
        self.meta = []
        self.embed_fn = embed_fn

    def add(self, text: str, meta: dict):
        self.vectors.append(self.embed_fn(text))
        self.meta.append(meta)

    def search(self, query: str, k: int):
        q = self.embed_fn(query)
        q = q / np.linalg.norm(q)

        sims = [
            (float(np.dot(v, q) / np.linalg.norm(v)), m)  # cosine similarity
            for v, m in zip(self.vectors, self.meta)
        ]
        return sorted(sims, reverse=True)[:k]

    def save(self, path: Path):
        path = path.with_suffix("")  # base path

        # vectors
        np.savez(
            path.with_suffix(".npz"),
            vectors=np.stack(self.vectors),
        )
        # meta
        with open(path.with_suffix(".json"), "w") as f:
            json.dump(self.meta, f)

    def load_data(self, path: Path):
        path = path.with_suffix("")

        data = np.load(path.with_suffix(".npz"))
        self.vectors = list(data["vectors"])

        with open(path.with_suffix(".json")) as f:
            self.meta = json.load(f)
