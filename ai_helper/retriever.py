import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticRetriever:
    """
    The SemanticRetriever class is responsible for indexing and retrieving semantic units (classes and functions) from a codebase based on their embeddings. It uses the SentenceTransformer model to generate embeddings for the semantic units and FAISS for efficient similarity search. The retrieve method allows querying the indexed semantic units using a natural language query, returning the most relevant units based on their embeddings. This class is essential for enabling the AI assistant to understand and utilize the existing codebase effectively when responding to user queries.  
    """
    
    def __init__(self, units):
        """
        Initializes the SemanticRetriever with a list of SemanticUnit objects. It generates embeddings for each unit using the SentenceTransformer model and builds a FAISS index for efficient retrieval. The embeddings capture the semantic meaning of the units, allowing for similarity-based searches. The retrieve method can then be used to find the most relevant semantic units based on a user's query.  
        """
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
        """
        Retrieves the top-k most relevant semantic units based on the provided query. It generates an embedding for the query using the SentenceTransformer model and performs a similarity search against the indexed embeddings. The method returns a list of the most relevant SemanticUnit objects, allowing the AI assistant to access the most pertinent information from the codebase when responding to user queries.  
        """
        q_emb = self.model.encode([query], convert_to_numpy=True)
        _, idxs = self.index.search(q_emb, k)
        return [self.units[i] for i in idxs[0]]
