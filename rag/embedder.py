from openai import OpenAI

client = OpenAI()


def generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for a piece of text.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for multiple texts in one API call.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )

    return [item.embedding for item in response.data]