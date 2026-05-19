import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticRetriever:
    '''
    The SemanticRetriever class is responsible for indexing and retrieving semantic units (classes and functions) from a codebase based on their embeddings. It uses the SentenceTransformer model to generate embeddings for the semantic units and FAISS for efficient similarity search. The retrieve method allows querying the indexed semantic units using a natural language query, returning the most relevant units based on their embeddings. This class is essential for enabling the AI assistant to understand and utilize the existing codebase effectively when responding to user queries.  
    '''
    
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
