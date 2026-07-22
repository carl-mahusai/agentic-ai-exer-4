from dotenv import load_dotenv
load_dotenv()

from rag.chunker import chunk_document
from rag.embedder import generate_embeddings
from rag.loader import load_documents
from rag.vectorstore import VectorStore
from pathlib import Path
import sys

project_root = Path.cwd()
sys.path.append(str(project_root))

def ingest_directory(
    store: VectorStore,
    directory: str,
    collection_name: str,
) -> None:
    """
    Index every document in a directory.
    """

    documents = load_documents(directory)

    print(
        f"\nIndexing '{collection_name}' "
        f"({len(documents)} documents)"
    )

    total_chunks = 0

    for document in documents:

        print(f"\nProcessing {document.filename}")

        #
        # Chunk
        #

        chunks = chunk_document(document)

        print(f"  {len(chunks)} chunks created")

        #
        # Embed
        #

        embeddings = generate_embeddings(
            [chunk.text for chunk in chunks]
        )

        #
        # Store
        #

        added = store.add_chunks(
            collection_name=collection_name,
            chunks=chunks,
            embeddings=embeddings,
        )

        total_chunks += added

        print(f"  {added} chunks stored")

    print(
        f"\nFinished indexing '{collection_name}'"
    )

    print(
        f"Collection now contains "
        f"{store.count(collection_name)} chunks."
    )


def main():

    store = VectorStore()

    #
    # Start with empty collections.
    #

    store.reset_collection("policy")
    store.reset_collection("coding")

    policies_folder = str(project_root / "documents" / "policies")
    coding_folder = str(project_root / "documents" / "coding")

    ingest_directory(
        store,
        policies_folder,
        "policy",
    )

    ingest_directory(
        store,
        coding_folder,
        "coding",
    )

    print("\n==============================")
    print("Indexing Complete")
    print("==============================")
    print(f"Policy chunks : {store.count('policy')}")
    print(f"Coding chunks : {store.count('coding')}")


if __name__ == "__main__":
    main()