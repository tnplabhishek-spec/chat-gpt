import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_secret")
DATA_DIR = "data"
UPLOAD_DIR = "uploads"
CHROMA_DIR = os.getenv("CHROMA_DIR", "chroma_db")
DEFAULT_COLLECTION = os.getenv("DEFAULT_COLLECTION", "default")
