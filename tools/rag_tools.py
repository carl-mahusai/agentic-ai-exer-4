from agents import function_tool

from rag.rag_service import RAGService

rag = RAGService()


@function_tool
async def search_knowledge_base(
    user_query: str,
) -> str:
    """
    Search the indexed policy and coding knowledge bases.
    """

    print("calling search knowledge base")

    result = await rag.search(
        user_query=user_query,
    )

    print(result)

    return result.context