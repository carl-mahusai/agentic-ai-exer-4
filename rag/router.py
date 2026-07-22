from agents import Agent

from rag.models import RouteDecision


router_agent = Agent(
    name="Knowledge Base Router",
    instructions="""
You decide which knowledge base should answer the user's question.

Knowledge Bases:

1. policy

Contains policy briefs.

Examples:

- AI policy
- Education policy
- Transport policy

2. coding

Contains software engineering and coding documents.

Examples:

- Python best practices
- Clean Code
- SOLID principles
- Refactoring
- Testing
- Documentation
- Object-oriented programming

Return ONLY the most appropriate knowledge base.

Do not answer the question.
""",
    output_type=RouteDecision,
)