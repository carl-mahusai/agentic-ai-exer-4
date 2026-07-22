from pathlib import Path
import fitz

from rag.models import Document


def load_documents(folder: str) -> list[Document]:
    """
    Reads every PDF in a folder and returns their extracted text.
    """

    documents = []

    folder = Path(folder)

    for pdf_path in folder.glob("*.pdf"):

        pdf = fitz.open(pdf_path)

        text = ""

        for page in pdf:
            text += page.get_text()

        documents.append(
            Document(
                filename=pdf_path.name,
                filepath=str(pdf_path),
                text=text,
            )
        )

    return documents