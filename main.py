from pathlib import Path
from cinema_rag.rag.loader import load_raw_listings
from cinema_rag.rag.cleaner import normalize_listings
from cinema_rag.rag.chunker import chunk_film_records
from cinema_rag.rag.embedder import Embedder
from cinema_rag.rag.vector_store import VectorStore
from cinema_rag.rag.retriever import Retriever
from cinema_rag.rag.context_builder import build_context

raw = load_raw_listings(Path("cinema_rag/data/raw_listings.json"))
records = normalize_listings(raw)
chunks = chunk_film_records(records)

embedder = Embedder()
texts = [c["text"] for c in chunks]
embeddings = embedder.embed_texts(texts)

store = VectorStore(dim=len(embeddings[0]))
store.add(embeddings, [c["metadata"] for c in chunks]) #type: ignore

retriever = Retriever(embedder, store)

results = retriever.retrieve("What films are showing at the BFI this weekend?")
context = build_context(results)

print(context)
