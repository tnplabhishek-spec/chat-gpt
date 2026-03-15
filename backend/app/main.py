import os
import uuid
import traceback
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pypdf import PdfReader

from app.schemas import RegisterRequest, LoginRequest, ConversationCreateRequest, ChatRequest
from app.storage import read_json, write_json
from app.auth import hash_password, verify_password, create_token
from app.retrieval import chunk_text
from app.vector_store import add_document_chunks, query_similar_chunks, delete_document_chunks
from app.llm import ollama_chat, stream_scaffold
from app.config import UPLOAD_DIR, DEFAULT_COLLECTION

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="ChatGPT Clone V6.2 Better Vector RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Exception occurred: {exc}")
    print(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__}
    )

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/register")
def register(data: RegisterRequest):
    users = read_json("users")
    if any(u["email"].lower() == data.email.lower() for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")
    user = {
        "id": str(uuid.uuid4()),
        "email": data.email.lower(),
        "password": hash_password(data.password),
        "created_at": datetime.utcnow().isoformat()
    }
    users.append(user)
    write_json("users", users)
    return {"user_id": user["id"], "email": user["email"]}

@app.post("/auth/login")
def login(data: LoginRequest):
    users = read_json("users")
    for user in users:
        if user["email"].lower() == data.email.lower() and verify_password(data.password, user["password"]):
            return {"token": create_token(user["id"]), "user_id": user["id"], "email": user["email"]}
    raise HTTPException(status_code=401, detail="Invalid login")

@app.post("/conversations")
def create_conversation(data: ConversationCreateRequest):
    conversations = read_json("conversations")
    conv = {
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "title": data.title,
        "created_at": datetime.utcnow().isoformat()
    }
    conversations.append(conv)
    write_json("conversations", conversations)
    return conv

@app.get("/conversations/{user_id}")
def list_conversations(user_id: str):
    conversations = read_json("conversations")
    return [c for c in conversations if c["user_id"] == user_id]

@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    conversations = read_json("conversations")
    messages = read_json("messages")
    new_conversations = [c for c in conversations if c["id"] != conversation_id]
    new_messages = [m for m in messages if m["conversation_id"] != conversation_id]
    write_json("conversations", new_conversations)
    write_json("messages", new_messages)
    return {"message": "Conversation deleted"}

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    collection: str = Form(DEFAULT_COLLECTION),
    tag: str = Form("")
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    save_name = f"{uuid.uuid4().hex}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, save_name)
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    reader = PdfReader(save_path)
    text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    chunks = chunk_text(text)

    document_id = str(uuid.uuid4())
    add_document_chunks(collection, document_id, file.filename, tag, chunks)

    documents = read_json("documents")
    documents.append({
        "id": document_id,
        "name": file.filename,
        "stored_name": save_name,
        "collection": collection,
        "tag": tag,
        "chunk_count": len(chunks),
        "created_at": datetime.utcnow().isoformat()
    })
    write_json("documents", documents)

    return {"message": "uploaded", "document_id": document_id, "chunks_created": len(chunks)}

@app.get("/documents")
def list_documents(collection: str = ""):
    docs = read_json("documents")
    if collection:
        docs = [d for d in docs if d.get("collection") == collection]
    return docs

@app.delete("/documents/{document_id}")
def delete_document(document_id: str):
    docs = read_json("documents")
    target = None
    remaining = []
    for d in docs:
        if d["id"] == document_id:
            target = d
        else:
            remaining.append(d)

    if not target:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = os.path.join(UPLOAD_DIR, target.get("stored_name", ""))
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass

    delete_document_chunks(target.get("collection", DEFAULT_COLLECTION), document_id)
    write_json("documents", remaining)
    return {"message": "Document deleted"}

@app.post("/chat")
def chat(data: ChatRequest):
    citations = []
    context_parts = []

    if data.use_documents:
        selected = query_similar_chunks(data.collection or DEFAULT_COLLECTION, data.message, top_k=4)
        for rec in selected:
            citations.append({
                "document": rec["document"],
                "chunk_index": rec["chunk_index"],
                "tag": rec.get("tag", ""),
                "preview": rec["chunk"][:160]
            })
            tag_text = f" | Tag: {rec.get('tag')}" if rec.get("tag") else ""
            context_parts.append(f"[Source: {rec['document']} | Chunk: {rec['chunk_index']}{tag_text}]\n{rec['chunk']}")

    prompt = [{"role": "system", "content": "You are a helpful offline AI assistant. Use retrieved vector database context when relevant."}]
    if context_parts:
        prompt.append({"role": "system", "content": "Retrieved context:\n\n" + "\n\n---\n\n".join(context_parts)})
    prompt.append({"role": "user", "content": data.message})

    reply = ollama_chat(prompt)

    messages = read_json("messages")
    messages.append({
        "id": str(uuid.uuid4()),
        "user_id": data.user_id,
        "conversation_id": data.conversation_id,
        "collection": data.collection,
        "question": data.message,
        "answer": reply,
        "citations": citations,
        "created_at": datetime.utcnow().isoformat()
    })
    write_json("messages", messages)

    return {"reply": reply, "citations": citations}

@app.get("/messages/{conversation_id}")
def list_messages(conversation_id: str):
    messages = read_json("messages")
    return [m for m in messages if m["conversation_id"] == conversation_id]

@app.get("/chat/stream")
def stream_demo():
    def gen():
        for part in stream_scaffold():
            yield f"data: {part}\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
