# client.py

import os

# from dotenv import load_dotenv
from openai import AsyncOpenAI

# load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY was not found. Please set it in your .env file."
    )

client = AsyncOpenAI(api_key=api_key)