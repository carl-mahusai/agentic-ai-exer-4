from dotenv import load_dotenv
load_dotenv()

from rag.loader import load_documents
from rag.chunker import chunk_document
from rag.embedder import generate_embedding, generate_embeddings
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

    # print(doc.filename)

    # print(len(chunks))

    # print(chunks)

    # for chunk in chunks:

    #     embedding = generate_embedding(chunk.text)

    #     print(chunk.section)
    #     print(len(embedding))

    texts = [chunk.text for chunk in chunks]

    embeddings = generate_embeddings(texts)

    print(embeddings)