from dotenv import load_dotenv
load_dotenv()


import uuid

import gradio as gr

from openai import BadRequestError

from agents import Runner

from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)

from openai.types.responses import ResponseTextDeltaEvent

from agents_config import get_agent, get_persona_names
from sessions import get_session, trim_session_history

DEFAULT_USERNAME = "guest"


# --------------------------------------------------------------------
# Chat callback
# --------------------------------------------------------------------

async def chat(message, history, username, persona, session_id):

    if history is None:
        history = []
    else:
        history = history.copy()

    username = username.strip()

    if not username:
        username = DEFAULT_USERNAME

    session = get_session(
        username=username,
        session_id=session_id,
    )

    agent = get_agent(persona)

    history.append(
        {
            "role": "user",
            "content": message,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": "",
        }
    )

    user_input = f"""
    User name: {username}

    Message:
    {message}
    """

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=user_input,
            session=session,
        )

        assistant_response = ""

        async for event in result.stream_events():

            # if (
            #     event.type == "raw_response_event"
            #     and event.data.type == "response.output_text.delta"
            # ):
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):

                assistant_response += event.data.delta

                history[-1]["content"] = assistant_response

                yield (
                    "",
                    history,
                    session_id,
                )

        # Trim the conversation history after the response has completed.
        await trim_session_history(session)
        return
    except InputGuardrailTripwireTriggered:

        history[-1]["content"] = (
            "Your request was blocked because it violated the application's safety policy."
        )

        yield "", history, session_id
        return

    except OutputGuardrailTripwireTriggered:

        history[-1]["content"] = (
            "The assistant generated a response that could not be shown because it violated the application's safety policy."
        )

        yield "", history, session_id
        return
    
    except BadRequestError as exc:
        print(exc)

        history[-1]["content"] = (
            "The request could not be processed."
        )

        yield "", history, session_id
        return
# --------------------------------------------------------------------
# Persona changed
# --------------------------------------------------------------------

def persona_changed(persona):

    return (
        [],
        DEFAULT_USERNAME,    # Reset username
        str(uuid.uuid4()),
    )


# --------------------------------------------------------------------
# UI
# --------------------------------------------------------------------

with gr.Blocks() as demo:

    gr.Markdown("# Personality-Driven Assistant")

    session_state = gr.State(str(uuid.uuid4()))

    username = gr.Textbox(
        label="Username",
        value=DEFAULT_USERNAME,
    )

    persona = gr.Dropdown(
        choices=get_persona_names(),
        value=get_persona_names()[0],
        label="Assistant Personality",
    )

    chatbot = gr.Chatbot(
        height=500,
    )

    message = gr.Textbox(
        label="Message",
        placeholder="Type your message...",
    )

    send = gr.Button("Send")

    send.click(
        fn=chat,
        inputs=[
            message,
            chatbot,
            username,
            persona,
            session_state,
        ],
        outputs=[
            message,
            chatbot,
            session_state,
        ],
    )

    message.submit(
        fn=chat,
        inputs=[
            message,
            chatbot,
            username,
            persona,
            session_state,
        ],
        outputs=[
            message,
            chatbot,
            session_state,
        ],
    )

    persona.change(
        fn=persona_changed,
        inputs=persona,
        outputs=[
            chatbot,
            username,
            session_state,
        ],
    )


if __name__ == "__main__":
    demo.launch()