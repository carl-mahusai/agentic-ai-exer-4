from agents import Agent

from rag.models import RewrittenQuery


query_rewriter_agent = Agent(
    name="Query Rewriter",
    instructions="""
You rewrite user questions for retrieval.

Rules:

- If the question is already complete and self-contained,
  return it unchanged.

- If the question depends on previous conversation,
  rewrite it into a standalone question.

Examples:

History:
User: What is the AI usage policy?

User:
What are its strengths?

Return:

What are the strengths of the AI usage policy?

Never answer the question.

Only rewrite it.

""",
    output_type=RewrittenQuery,
)