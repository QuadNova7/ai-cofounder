"""Idempotent ChromaDB Seeder for Startup Frameworks and Case Studies.

Reads markdown documents from services/business-intelligence/data/seed/
and indexes them into a persistent ChromaDB collection.
"""

import os
import glob
from typing import List, Dict

SEED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "seed"
)
COLLECTION_NAME = "startup_frameworks"


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> List[str]:
    """Splits text into overlapping token-approximated chunks."""
    words = text.split()
    chunks = []
    i = 0
    step = max(1, chunk_size - overlap)
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += step
    return chunks


def seed_chromadb_if_empty(persist_directory: str = "./data/chroma") -> int:
    """Checks collection count; if 0 or uninitialized, seeds documents into ChromaDB.
    Returns total document chunks indexed.
    """
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        print("[RAG Seeder] chromadb not installed, skipping vector store seeding.")
        return 0

    os.makedirs(persist_directory, exist_ok=True)
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    count = collection.count()
    if count > 0:
        print(f"[RAG Seeder] Collection '{COLLECTION_NAME}' already seeded with {count} chunks.")
        return count

    print(f"[RAG Seeder] Seeding collection '{COLLECTION_NAME}' from {SEED_DIR}...")
    md_files = glob.glob(os.path.join(SEED_DIR, "*.md"))
    if not md_files:
        print(f"[RAG Seeder] No markdown files found in {SEED_DIR}.")
        return 0

    total_chunks = 0
    ids, documents, metadatas = [], [], []

    for file_path in md_files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        file_chunks = chunk_text(content)
        for idx, chunk in enumerate(file_chunks):
            chunk_id = f"{filename}_{idx}"
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({"source": filename, "chunk_index": idx})
            total_chunks += 1

    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"[RAG Seeder] Successfully indexed {total_chunks} chunks into ChromaDB.")

    return total_chunks


if __name__ == "__main__":
    seed_chromadb_if_empty()
