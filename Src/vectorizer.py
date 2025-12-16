import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Always resolve paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
CHROMA_PATH = REPO_ROOT / "openai_mobile_review_embeddings"

DATA_PATH = REPO_ROOT / "data" / "mobile_archive" / "mobiles_reviews_cleaned.csv"  # unused at runtime
COLLECTION_NAME = "mobile_reviews_openai"
OPENAI_EMBED_MODEL = "text-embedding-3-small"

def _require_openai_key():
    # On Render you set OPENAI_API_KEY in env vars
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set in environment variables.")


def get_vector_store() -> Chroma:
    """
    Open an existing persisted Chroma collection.
    This MUST be fast and must not rebuild embeddings on server start.
    """
    _require_openai_key()

    sqlite_path = CHROMA_PATH / "chroma.sqlite3"
    if not sqlite_path.exists():
        raise FileNotFoundError(
            f"Missing persisted Chroma store at {sqlite_path}. "
            f"Make sure embeddings were downloaded/extracted before starting the app."
        )

    # Validate collection exists
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        raise RuntimeError(
            f"Chroma collection '{COLLECTION_NAME}' not found in {CHROMA_PATH}. "
            f"Your embeddings folder may not match this collection name."
        ) from e

    embeddings = OpenAIEmbeddings(model=OPENAI_EMBED_MODEL)
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings,
    )


# Backwards-compatible exports (so UI.py can import vector_store)
vector_store = get_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 8})

__all__ = ["retriever", "vector_store", "COLLECTION_NAME", "CHROMA_PATH", "get_vector_store"]
