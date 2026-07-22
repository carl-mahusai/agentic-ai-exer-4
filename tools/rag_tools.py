from agents import function_tool

from rag.rag_service import RAGService


rag = RAGService()


@function_tool
def search_knowledge_base(
    user_query: str,
) -> str:
    """
    Search the indexed policy and coding knowledge bases.
    """

    result = rag.retrieve(
        user_query=user_query,
    )

    return result.context