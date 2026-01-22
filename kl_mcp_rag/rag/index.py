import pickle
import numpy as np
from openai import OpenAI

client = OpenAI()


class FilmIndex:
    def __init__(self):
        self.vectors = []
        self.meta = []

    # This is slow, looking optimisations:
    # concurrent calls with openai batching?
    # not run on every query of system - have it run manually with a cli call (eventually linked to  updates of raw data)
    # also consider switch to open source embedding model as this is simple vector store
    def _embed(self, text: str) -> np.ndarray:
        vec = np.array(
            client.embeddings.create(model="text-embedding-3-small", input=text)
            .data[0]
            .embedding
        )
        return vec / np.linalg.norm(
            vec
        )  # 🔑 see notes on embeddings for why cosine over dot product

    def add(self, text: str, meta: dict):
        self.vectors.append(self._embed(text))
        self.meta.append(meta)

    def search(self, query: str, k: int = 3):
        q = self._embed(query)
        sims = [(float(np.dot(v, q)), m) for v, m in zip(self.vectors, self.meta)]
        return sorted(sims, reverse=True)[:k]

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str):
        with open(path, "rb") as f:
            return pickle.load(f)
