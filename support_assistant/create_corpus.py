from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DOCS_DIR = BASE_DIR / "docs"

CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "zepto_policies"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():

    documents = []

    document_ids = []

    metadata = []

    files = sorted(
        DOCS_DIR.glob("doc_*.txt")
    )

    print(
        f"Found {len(files)} document files."
    )

    if len(files) != 8:

        raise ValueError(
            f"Expected exactly 8 documents, "
            f"but found {len(files)}."
        )

    for file_path in files:

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:

            raise ValueError(
                f"{file_path.name} is empty."
            )

        document_id = file_path.stem

        documents.append(text)

        document_ids.append(
            document_id
        )

        metadata.append(
            {
                "document_id": document_id,
                "source": file_path.name
            }
        )

        print(
            f"Loaded: {file_path.name}"
        )

    return (
        documents,
        document_ids,
        metadata
    )


# ============================================================
# CREATE VECTOR DATABASE
# ============================================================

def create_vector_database():

    print()
    print("=" * 60)
    print("STEP 1 - LOAD DOCUMENTS")
    print("=" * 60)

    (
        documents,
        document_ids,
        metadata
    ) = load_documents()

    print()
    print("=" * 60)
    print("STEP 2 - LOAD EMBEDDING MODEL")
    print("=" * 60)

    print(
        f"Model: {EMBEDDING_MODEL}"
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print(
        "Embedding model loaded successfully."
    )

    print()
    print("=" * 60)
    print("STEP 3 - GENERATE EMBEDDINGS")
    print("=" * 60)

    embeddings = model.encode(
        documents,
        normalize_embeddings=True
    )

    embeddings = embeddings.tolist()

    print(
        f"Generated {len(embeddings)} embeddings."
    )

    print()
    print("=" * 60)
    print("STEP 4 - CREATE CHROMADB")
    print("=" * 60)

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Delete existing collection so the script
    # can regenerate the database from scratch.

    try:

        client.delete_collection(
            COLLECTION_NAME
        )

        print(
            "Existing collection deleted."
        )

    except Exception:

        print(
            "No existing collection found."
        )

    collection = client.create_collection(

        name=COLLECTION_NAME,

        metadata={
            "description":
                "Zepto support policy corpus"
        },

        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )

    collection.add(

        ids=document_ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadata
    )

    print()
    print("=" * 60)
    print("VECTOR DATABASE CREATED")
    print("=" * 60)

    print(
        "Collection:",
        COLLECTION_NAME
    )

    print(
        "Document count:",
        collection.count()
    )

    print(
        "Database path:",
        CHROMA_DIR
    )

    return collection


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_vector_database()

    print()
    print(
        "Corpus creation completed successfully."
    )