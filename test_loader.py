from rag.loader import load_documents
from rag.chunker import chunk_document
from pathlib import Path
import sys

project_root = Path.cwd()
sys.path.append(str(project_root))

print(project_root)

print(str(project_root / "documents" / "coding"))

docs = coding_docs = load_documents(str(project_root / "documents" / "coding"))

print(coding_docs)

for doc in docs:

    chunks = chunk_document(doc)

    print(doc.filename)

    print(len(chunks))

    print(chunks)