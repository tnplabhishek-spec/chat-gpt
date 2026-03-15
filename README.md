# ChatGPT Clone V6.2 — Better Vector RAG (Offline)

This version improves V6.1 with a better local vector-RAG workflow.

## Improvements over V6.1

- document delete endpoint
- conversation delete endpoint
- better UI structure
- document metadata support
- multiple vector collections
- collection-based retrieval
- better citations
- streaming scaffold
- updated local run guide

## Tech stack

- FastAPI backend
- Next.js frontend
- Ollama local chat model
- Ollama local embedding model
- ChromaDB local vector database
- JSON storage for app state
- PDF upload + vector retrieval

## Fully offline

This project is fully offline when you use:
- Ollama local chat model
- Ollama local embedding model

No PostgreSQL, Redis, or cloud API is required.
