from agents import Runner

from rag.query_rewriter import query_rewriter_agent
from rag.models import RewrittenQuery


def rewrite_query(history, query) -> RewrittenQuery:

    prompt = f"""
Conversation History

{history}

Latest User Question

{query}
"""

    result = Runner.run_sync(
        query_rewriter_agent,
        prompt,
    )

    return result.final_output