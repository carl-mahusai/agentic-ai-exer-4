from rag.embedder import generate_embeddings
from rag.vectorstore import VectorStore
from rag.models import RetrievedChunk


def retrieve_context(
    store: VectorStore,
    collection_name: str,
    query: str,
    top_k: int = 5,
) -> list[RetrievedChunk]:
    """
    Retrieves the most relevant chunks for a query.
    """

    query_embedding = generate_embeddings([query])[0]

    return store.search(
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=top_k,
    )

def format_context(chunks: list[RetrievedChunk]) -> str:
    """
    Formats retrieved chunks into a prompt-friendly string.
    """

    parts = []

    for chunk in chunks:
        parts.append(
            f"""Document: {chunk.document_name}
Section: {chunk.section}

{chunk.text}
"""
        )

    return "\n\n---\n\n".join(parts)