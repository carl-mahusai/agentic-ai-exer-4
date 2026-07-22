import chromadb
from chromadb.api.models.Collection import Collection

from rag.models import Chunk


class VectorStore:
    """
    Wrapper around ChromaDB that manages the project's vector collections.
    """

    def __init__(self, db_path: str = "./vector_db"):

        self.client = chromadb.PersistentClient(path=db_path)

        self.collections: dict[str, Collection] = {}

        for collection_name in ("policy", "coding"):
            self.collections[collection_name] = (
                self.client.get_or_create_collection(
                    name=collection_name
                )
            )

    def get_collection(self, name: str) -> Collection:
        """
        Returns the requested ChromaDB collection.
        """

        try:
            return self.collections[name]
        except KeyError:
            raise ValueError(f"Unknown collection: {name}")

    def reset_collection(self, collection_name: str) -> None:
        """
        Deletes and recreates a collection.
        Useful while rebuilding the vector database.
        """

        try:
            self.client.delete_collection(collection_name)
        except Exception:
            pass

        self.collections[collection_name] = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def _build_metadata(
        self,
        collection_name: str,
        chunk: Chunk,
    ) -> dict:

        return {
            "knowledge_base": collection_name,
            "document_name": chunk.document_name,
            "section": chunk.section,
            "chunk_number": chunk.chunk_number,
        }

    def add_chunks(
        self,
        collection_name: str,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> int:
        """
        Stores a batch of chunks in ChromaDB.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings."
            )

        collection = self.get_collection(collection_name)

        collection.add(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            embeddings=embeddings,
            metadatas=[
                self._build_metadata(
                    collection_name,
                    chunk,
                )
                for chunk in chunks
            ],
        )

        return len(chunks)

    def count(self, collection_name: str) -> int:
        """
        Returns the number of indexed chunks.
        """

        collection = self.get_collection(collection_name)

        return collection.count()