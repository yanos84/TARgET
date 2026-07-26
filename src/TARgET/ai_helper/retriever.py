import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from .indexer import SemanticUnit


class SemanticRetriever:
    """
    Retrieves relevant source-code units from a codebase.

    Embeddings are generated from both semantic metadata and actual source
    code. This allows retrieval to match user questions against implementation
    details, not only class names and docstrings.
    """

    def __init__(
        self,
        units: list[SemanticUnit],
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.units = units

        self.model = SentenceTransformer(model_name)

        texts = [
            self._unit_to_text(unit)
            for unit in units
        ]

        self.embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        self.embeddings = np.asarray(
            self.embeddings,
            dtype="float32",
        )

        dimension = self.embeddings.shape[1]

        # With normalized vectors, inner product is equivalent
        # to cosine similarity.
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(self.embeddings)

    @staticmethod
    def _unit_to_text(unit: SemanticUnit) -> str:
        """
        Converts a semantic unit into the text used for embedding.
        """

        parent = (
            f"Parent: {unit.parent}\n"
            if unit.parent
            else ""
        )

        bases = (
            f"Bases: {', '.join(unit.bases)}\n"
            if unit.bases
            else ""
        )

        decorators = (
            f"Decorators: {', '.join(unit.decorators)}\n"
            if unit.decorators
            else ""
        )

        return (
            f"Type: {unit.kind}\n"
            f"Name: {unit.name}\n"
            f"File: {unit.file}\n"
            f"Signature: {unit.signature}\n"
            f"{parent}"
            f"{bases}"
            f"{decorators}"
            f"Documentation:\n"
            f"{unit.docstring}\n\n"
            f"Source code:\n"
            f"{unit.code}"
        )

    def retrieve(
        self,
        query: str,
        k: int = 4,
    ) -> list[SemanticUnit]:
        """
        Retrieves the k most relevant source-code units.
        """

        if not self.units:
            return []

        k = min(k, len(self.units))

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        _, indices = self.index.search(
            query_embedding,
            k,
        )

        return [
            self.units[index]
            for index in indices[0]
            if index != -1
        ]