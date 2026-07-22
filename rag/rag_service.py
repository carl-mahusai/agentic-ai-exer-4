from agents.memory import SQLiteSession

from rag.models import RAGContext
from rag.rewriter import rewrite_query
from rag.router_service import route_query
from rag.retriever import (
    retrieve_context,
    format_context,
)
from rag.vectorstore import VectorStore

from sessions import MAX_CONTEXT_ITEMS

from sessions import get_history_text

class RAGService:

    def __init__(self):

        self.store = VectorStore()
        self.session: SQLiteSession | None = None

    def set_session(
        self,
        session: SQLiteSession,
    ) -> None:
        """
        Sets the active chat session for the current request.
        """

        self.session = session

    async def _get_history(
        self,
        max_turns: int = MAX_CONTEXT_ITEMS,
    ) -> str:

        if self.session is None:
            return ""

        return await get_history_text(
            session=self.session,
            max_turns=max_turns,
        )

    async def search(
        self,
        user_query: str,
        top_k: int = 5,
    ) -> RAGContext:

        #
        # Step 1
        # Rewrite the query
        #
        print("<------------history start-------->")
        history = await self._get_history()
        print(history)
        print("<------------history end-------->")

        print("<------------rewritten start-------->")
        try:
            rewritten = await rewrite_query(
                history=history,
                query=user_query,
            )
        except Exception as e:
            print(str(e))



        print(rewritten)
        print("<------------rewritten end-------->")
        #
        # Step 2
        # Route to a knowledge base
        #
        print("<------------decision start-------->")
        try:
            decision = await route_query(
                rewritten.rewritten_query,
            )
        except Exception as e:
            print(str(e))

        print(decision)
        print("<------------decision end-------->")
        #
        # Step 3
        # Retrieve matching chunks
        #
        print("<------------chunks start-------->")
        try:
            chunks = retrieve_context(
                store=self.store,
                collection_name=decision.knowledge_base.value,
                query=rewritten.rewritten_query,
                top_k=top_k,
            )
        except Exception as e:
            print(str(e))

        print(chunks)
        print("<------------chunks end-------->")

        #
        # Step 4
        # Convert chunks into prompt text
        #
        print("<------------context start-------->")
        try:
            context = format_context(chunks)
        except Exception as e:
            print(str(e))

        print(context)
        print("<------------context end-------->")

        return RAGContext(
            rewritten_query=rewritten.rewritten_query,
            knowledge_base=decision.knowledge_base.value,
            context=context,
        )