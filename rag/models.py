from dataclasses import dataclass

@dataclass
class Document:
    filename: str
    filepath: str
    text: str

@dataclass
class Section:
    heading: str
    text: str

@dataclass
class Chunk:
    id: str
    document_name: str
    chunk_number: int
    section: str
    text: str