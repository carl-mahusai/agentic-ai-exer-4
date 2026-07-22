from rag.models import RAGContext
from rag.rewriter import rewrite_query
from rag.router_service import route_query
from rag.retriever import (
    retrieve_context,
    format_context,
)
from rag.vectorstore import VectorStore


class RAGAgent:
    """
    Coordinates the RAG pipeline.

    Responsibilities:
    - Rewrite the user's query if necessary.
    - Route the query to the correct knowledge base.
    - Retrieve relevant document chunks.
    """

    def __init__(self):

        #
        # One ChromaDB connection for the lifetime
        # of the application.
        #

        self.store = VectorStore()

    def retrieve(
        self,
        history: str,
        user_query: str,
        top_k: int = 5,
    ) -> RAGContext:

        #
        # Step 1
        # Rewrite the query
        #

        rewritten = rewrite_query(
            history=history,
            query=user_query,
        )

        #
        # Step 2
        # Route to a knowledge base
        #

        decision = route_query(
            rewritten.rewritten_query,
        )

        #
        # Step 3
        # Retrieve matching chunks
        #

        chunks = retrieve_context(
            store=self.store,
            collection_name=decision.knowledge_base.value,
            query=rewritten.rewritten_query,
            top_k=top_k,
        )

        #
        # Step 4
        # Convert chunks into prompt text
        #

        context = format_context(chunks)

        return RAGContext(
            rewritten_query=rewritten.rewritten_query,
            knowledge_base=decision.knowledge_base.value,
            context=context,
        )