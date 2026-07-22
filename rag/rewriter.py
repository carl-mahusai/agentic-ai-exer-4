from agents import Runner

from rag.query_rewriter import query_rewriter_agent
from rag.models import RewrittenQuery


async def rewrite_query(
    history: str,
    query: str,
) -> RewrittenQuery:

    prompt = f"""
Conversation History

{history}

Latest User Question

{query}
"""

    result = await Runner.run(
        query_rewriter_agent,
        prompt,
    )

    return result.final_output