import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticRetriever:
    def __init__(self, units):
        self.units = units
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        texts = [
            f"{u.kind} {u.name}\n{u.signature}\n{u.docstring}"
            for u in units
        ]

        self.embeddings = self.model.encode(texts, convert_to_numpy=True)
        print("embeddings shape:", self.embeddings.shape)
        print("embeddings dtype:", self.embeddings.dtype)

        dim = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def retrieve(self, query: str, k=4):
        q_emb = self.model.encode([query], convert_to_numpy=True)
        _, idxs = self.index.search(q_emb, k)
        return [self.units[i] for i in idxs[0]]
