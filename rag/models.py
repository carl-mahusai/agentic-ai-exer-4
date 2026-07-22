from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum

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


class RewrittenQuery(BaseModel):
    rewritten_query: str
    was_rewritten: bool


class KnowledgeBase(str, Enum):
    POLICY = "policy"
    CODING = "coding"


class RouteDecision(BaseModel):
    knowledge_base: KnowledgeBase
    reasoning: str


class RetrievedChunk(BaseModel):
    document_name: str
    section: str
    chunk_number: int
    text: str
    distance: float


class RAGContext(BaseModel):
    rewritten_query: str
    knowledge_base: str
    context: str