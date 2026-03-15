import httpx
from app.config import OLLAMA_CHAT_MODEL, OLLAMA_BASE_URL

def ollama_chat(messages):
    payload = {
        "model": OLLAMA_CHAT_MODEL,
        "messages": messages,
        "stream": False
    }
    r = httpx.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=300.0)
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("content", "")

def stream_scaffold():
    yield "Better vector RAG stream connected."
    yield "[DONE]"
