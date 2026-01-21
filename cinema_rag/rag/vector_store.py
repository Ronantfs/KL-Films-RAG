import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings: list[list[float]], metadatas: list[dict]):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors) # type: ignore
        self.metadata.extend(metadatas)

    def search(self, query_embedding: list[float], k: int = 5):
        query = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query, k) # type: ignore

        return [
            self.metadata[i]
            for i in indices[0]
            if i < len(self.metadata)
        ]
