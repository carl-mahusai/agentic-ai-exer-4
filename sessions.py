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