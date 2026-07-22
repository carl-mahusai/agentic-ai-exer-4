from rag.models import Document, Chunk
from rag.split_sections import split_into_sections
import uuid




def chunk_section(
    document_name: str,
    section_name: str,
    text: str,
    chunk_size: int,
    overlap: int,
    start_chunk_number: int,
):

    words = text.split()

    chunks = []

    chunk_number = start_chunk_number

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_text = " ".join(words[start:end])

        chunks.append(
            Chunk(
                id=str(uuid.uuid4()),
                document_name=document_name,
                chunk_number=chunk_number,
                section=section_name,
                text=chunk_text,
            )
        )

        chunk_number += 1
        start += chunk_size - overlap

    return chunks

def chunk_document(
    document: Document,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[Chunk]:
    """
    Splits a document into semantic sections and then chunks each section.
    """

    sections = split_into_sections(document)

    chunks = []

    chunk_number = 1

    for section in sections:

        section_chunks = chunk_section(
            document_name=document.filename,
            section_name=section.heading,
            text=section.text,
            chunk_size=chunk_size,
            overlap=overlap,
            start_chunk_number=chunk_number,
        )

        chunks.extend(section_chunks)

        chunk_number += len(section_chunks)

    return chunks