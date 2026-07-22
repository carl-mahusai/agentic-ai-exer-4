from agents import function_tool

from rag.rag_service import RAGService


rag = RAGService()


@function_tool
def search_knowledge_base(
    history: str,
    user_query: str,
) -> str:
    """
    Retrieve relevant context from the document knowledge bases.

    Use this tool whenever additional information
    from the policy or coding documents would help answer
    the user's question.
    """

    result = rag.retrieve(
        history=history,
        user_query=user_query,
    )

    return result.context