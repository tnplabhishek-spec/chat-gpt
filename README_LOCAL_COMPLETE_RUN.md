# ChatGPT Clone V6.2 — Complete Local Run Guide

## 1) Install required software

Install:

- Python 3.10+
- Node.js 18+
- npm
- Ollama

Check:

```bash
python --version
node --version
npm --version
ollama --version
```

## 2) Prepare Ollama

Pull required models:

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

You may replace the chat model with another Ollama model, but keep `nomic-embed-text` for embeddings.

Test:

```bash
ollama run llama3.1
```

## 3) Extract project

Extract ZIP and open terminal in:

```text
chatgpt-clone-v6.2-better-vector-rag/
```

## 4) Backend setup

```bash
cd backend
python -m venv venv
```

Windows:

```cmd
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Copy env:

Linux / Mac:

```bash
cp .env.example .env
```

Windows:

```cmd
copy .env.example .env
```

Edit `backend/.env`:

```env
OLLAMA_CHAT_MODEL=llama3.1
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
JWT_SECRET_KEY=change_this_secret
CHROMA_DIR=chroma_db
DEFAULT_COLLECTION=default
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend URLs:
- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/health

## 5) Frontend setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:
- http://localhost:3000

## 6) Complete flow

1. Start Ollama
2. Start backend
3. Start frontend
4. Register
5. Login
6. Create conversation
7. Choose collection name
8. Upload PDF into that collection
9. Ask question with RAG enabled
10. See citations and history
11. Delete document or conversation if needed

## 7) Storage

### JSON app data
```text
backend/data/
```

### Uploaded PDFs
```text
backend/uploads/
```

### Chroma vector DB
```text
backend/chroma_db/
```

## 8) Reset project

Stop backend, then delete:

```text
backend/data/
backend/uploads/
backend/chroma_db/
```

## 9) Quick commands

### Ollama
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
