from agents.memory import SQLiteSession


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
    Convert the recent conversation history into plain text.

    This helper intentionally avoids depending on the internal
    item classes of the Agents SDK so it remains compatible across
    SDK versions.
    """

    items = await session.get_items(
        limit=max_turns * 2,
    )

    history = []

    for item in items:

        #
        # SQLiteSession may return SDK objects or dictionaries.
        #

        if hasattr(item, "to_input_item"):
            item = item.to_input_item()

        if not isinstance(item, dict):
            continue

        role = item.get("role")

        content = item.get("content")

        if not role or not content:
            continue

        #
        # Flatten the Responses API content format.
        #

        if isinstance(content, list):

            text_parts = []

            for part in content:

                if isinstance(part, dict):

                    text = part.get("text")

                    if text:
                        text_parts.append(text)

            content = "".join(text_parts)

        if isinstance(content, str) and content.strip():

            history.append(
                f"{role.capitalize()}: {content}"
            )

    # return "\n".join(history)

    history_text = "\n".join(history)

    # print("===== RAG HISTORY =====")
    # print(history_text)
    # print("=======================")

    return history_text