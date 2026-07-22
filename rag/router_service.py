from agents import Runner

from rag.models import RouteDecision
from rag.router import router_agent


async def route_query(
    query: str,
) -> RouteDecision:

    result = Runner.run(
        router_agent,
        query,
    )

    return result.final_output