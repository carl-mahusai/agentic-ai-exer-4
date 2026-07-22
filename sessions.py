from agents.memory import SQLiteSession
from agents.memory import SQLiteSession
from agents.items import (
    MessageInputItem,
    MessageOutputItem,
)
from openai.types.responses import (
    ResponseOutputMessage,
)

DB_PATH = "sessions.db"

_sessions = {}

MAX_CONTEXT_TURNS = 10
MAX_CONTEXT_ITEMS = MAX_CONTEXT_TURNS * 2

def get_session(username: str, session_id: str):

    key = (username, session_id)

    if key not in _sessions:
        _sessions[key] = SQLiteSession(
            session_id=session_id,
            db_path=DB_PATH,
        )

    return _sessions[key]

async def trim_session_history(session: SQLiteSession) -> None:
    """
    Retain only the most recent conversation items in the session.

    This keeps the session from growing indefinitely while preserving
    enough context for follow-up questions.
    """
    recent_items = await session.get_items(limit=MAX_CONTEXT_ITEMS)

    await session.clear_session()
    await session.add_items(recent_items)


async def get_history_text(
    session: SQLiteSession,
    max_turns: int = 20,
) -> str:
    """
    Convert the recent conversation history into a plain-text transcript.

    This helper is shared by both the chatbot and the RAG pipeline.
    """

    items = await session.get_items(
        limit=max_turns * 2,
    )

    history = []

    for item in items:

        #
        # User message
        #

        if isinstance(item, MessageInputItem):

            raw = item.raw_item

            if (
                isinstance(raw, dict)
                and raw.get("role") == "user"
            ):

                content = raw.get("content")

                if isinstance(content, str):
                    history.append(
                        f"User: {content}"
                    )

        #
        # Assistant message
        #

        elif isinstance(item, MessageOutputItem):

            raw = item.raw_item

            if isinstance(raw, ResponseOutputMessage):

                text = []

                for part in raw.content:

                    if hasattr(part, "text"):
                        text.append(part.text)

                if text:

                    history.append(
                        "Assistant: "
                        + "".join(text)
                    )

    return "\n".join(history)