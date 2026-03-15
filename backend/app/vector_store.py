import os
import uuid
import chromadb
import httpx
from app.config import CHROMA_DIR, OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL

os.makedirs(CHROMA_DIR, exist_ok=True)
client = chromadb.PersistentClient(path=CHROMA_DIR)

def get_collection(collection_name: str):
    safe = collection_name.strip() or "default"
    return client.get_or_create_collection(name=safe)

def embed_text(text: str):
    r = httpx.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": OLLAMA_EMBED_MODEL, "prompt": text},
        timeout=120.0,
    )
    r.raise_for_status()
    data = r.json()
    return data["embedding"]

def add_document_chunks(collection_name: str, document_id: str, document_name: str, tag: str, chunks: list[str]):
    collection = get_collection(collection_name)
    ids, embeddings, metadatas, documents = [], [], [], []
    for idx, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        embeddings.append(embed_text(chunk))
        metadatas.append({
            "document_id": document_id,
            "document_name": document_name,
            "chunk_index": idx,
            "tag": tag or ""
        })
        documents.append(chunk)
    if ids:
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

def query_similar_chunks(collection_name: str, query: str, top_k: int = 4):
    collection = get_collection(collection_name)
    query_embedding = embed_text(query)
    result = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    output = []
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0] if result.get("distances") else [None] * len(docs)
    for doc, meta, dist in zip(docs, metas, distances):
        output.append({
            "document": meta.get("document_name"),
            "document_id": meta.get("document_id"),
            "chunk_index": meta.get("chunk_index"),
            "tag": meta.get("tag", ""),
            "distance": dist,
            "chunk": doc
        })
    return output

def delete_document_chunks(collection_name: str, document_id: str):
    collection = get_collection(collection_name)
    try:
        collection.delete(where={"document_id": document_id})
    except Exception:
        pass
