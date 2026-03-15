# 🚀 ChatGPT Clone V6.2 - Complete Setup & Run Guide

**Last Updated:** March 15, 2026  
**Status:** ✅ Fully Tested & Operational

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Running the Project](#running-the-project)
4. [Accessing the Application](#accessing-the-application)
5. [Testing the Setup](#testing-the-setup)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before you start, ensure your system has:

### **Software Requirements**
- **Windows 10/11** or Linux/Mac
- **Python 3.10+**
- **Node.js 18+** (with npm)
- **Ollama** (for local LLM)
- **Git** (optional, for cloning)

### **Hardware Requirements**
- **RAM:** Minimum 8 GB (Recommended 16 GB)
- **Disk Space:** ~10 GB for models + storage
- **Internet:** Required for installation only

### **Check if Installed**
```powershell
# Check Python
python --version

# Check Node.js
node --version
npm --version

# Check Ollama (if installed)
ollama --version
```

---

## 📦 Installation Steps

### **Step 1: Install Python (if not installed)**

#### **Windows - Using Winget**
```powershell
winget install Python.Python.3.11
```

#### **Windows - Manual Download**
- Visit: https://www.python.org/downloads/
- Download Python 3.11+
- During installation, check "Add Python to PATH"

#### **Linux**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

#### **Mac**
```bash
brew install python3
```

---

### **Step 2: Install Node.js & npm (if not installed)**

#### **Windows - Using Winget**
```powershell
winget install OpenJS.NodeJS
```

#### **Windows - Manual Download**
- Visit: https://nodejs.org/
- Download LTS version (18+)
- Run installer and follow prompts

#### **Linux**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### **Mac**
```bash
brew install node
```

---

### **Step 3: Install Ollama (if not installed)**

#### **Windows - Using Winget**
```powershell
winget install Ollama.Ollama
```

#### **Windows - Manual Download**
- Visit: https://ollama.ai
- Download Windows installer
- Run installer (may require admin)

#### **Linux**
```bash
curl https://ollama.ai/install.sh | sh
```

#### **Mac**
- Visit: https://ollama.ai
- Download Mac version
- Run installer

---

### **Step 4: Pull Required AI Models**

After Ollama installation, pull the models:

```powershell
# Chat model (4.9 GB)
ollama pull llama3.1

# Embedding model (274 MB)
ollama pull nomic-embed-text

# Verify models are installed
ollama list
```

This will show:
```
NAME                    ID              SIZE      MODIFIED
llama3.1                44136d8a1e0a    4.7 GB    2 hours ago
nomic-embed-text        0a109f4b3fe5    274 MB    2 hours ago
```

---

## 🎯 Running the Project

### **Step 1: Navigate to Project Directory**

```powershell
cd "C:\Users\Abhishek Shrivastava\IMP\ChatGPT_CODE\chatgpt-clone-v6.2-better-vector-rag\chatgpt-clone-v6.2-better-vector-rag"
```

> Replace path with your actual project location

---

### **Step 2: Start Ollama (Terminal 1)**

Ollama typically runs automatically, but you can manually start it:

```powershell
# Windows - Ollama usually starts as a service
# Check if it's running on port 11434
curl http://localhost:11434

# If not running, start manually:
"$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```

**Expected Output:**
```
Ollama is running on http://127.0.0.1:11434
```

---

### **Step 3: Start Backend API (Terminal 2)**

```powershell
# Navigate to backend
cd backend

# Activate Python virtual environment
venv\Scripts\activate

# Start the server
python -m uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

### **Step 4: Start Frontend (Terminal 3)**

```powershell
# Navigate to frontend directory
cd frontend

# Make sure Node.js is in PATH
$env:PATH = "$env:PATH;C:\Program Files\nodejs"

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
> dev
> next dev

  ▲ Next.js 14.2.5
  - Local:        http://localhost:3000
```

---

## 🌐 Accessing the Application

Once all three services are running, access:

### **Main Application**
```
http://localhost:3000
```

### **Backend API**
```
http://localhost:8000
```

### **API Documentation (Swagger)**
```
http://localhost:8000/docs
```

### **API Health Check**
```
http://localhost:8000/health
```

### **Ollama Server**
```
http://localhost:11434
```

---

## 🎬 Quick Start Workflow

### **1. Register New Account**
1. Go to http://localhost:3000
2. Click **"Register"**
3. Enter email: `user@example.com`
4. Enter password: `password123`
5. Click **"Register"** button

**Expected:** Account created successfully

---

### **2. Login**
1. Enter your email and password
2. Click **"Login"** button

**Expected:** Logged in, can now see dashboard

---

### **3. Create Collection**
1. In left panel, change collection name (e.g., "MyDocuments")
2. This organizes your documents

---

### **4. Upload PDF**
1. Click **"Upload Document"**
2. Select a PDF file from your computer
3. Document is processed and indexed

**Expected:** Document appears in list

---

### **5. Ask Questions**
1. Type a question in the chat box
2. Click **"Send"** button
3. AI responds using your documents

**Example:**
```
Question: "What does the document say about pricing?"
Answer: [AI response with document citations]
```

---

## 🧪 Testing the Setup

### **Test All Services Running**

```powershell
# Test Frontend
$frontend = (Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -ErrorAction SilentlyContinue).StatusCode
Write-Host "Frontend: $frontend"

# Test Backend
$backend = (Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue).StatusCode
Write-Host "Backend: $backend"

# Test Ollama
$ollama = (Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -ErrorAction SilentlyContinue).StatusCode
Write-Host "Ollama: $ollama"
```

**Expected Output:**
```
Frontend: 200
Backend: 200
Ollama: 200
```

---

### **Test Backend Registration**

```powershell
$json = '{"email":"test@example.com","password":"test123"}'
$response = Invoke-WebRequest -Uri "http://localhost:8000/auth/register" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $json `
  -UseBasicParsing

Write-Host "Status: $($response.StatusCode)"
Write-Host "Response: $($response.Content)"
```

**Expected Output:**
```
Status: 200
Response: {"user_id":"uuid-here","email":"test@example.com"}
```

---

## 🔌 Service URLs Reference

| Service | URL | Port | Purpose |
|---------|-----|------|---------|
| **Frontend** | http://localhost:3000 | 3000 | User interface |
| **Backend API** | http://localhost:8000 | 8000 | API server |
| **API Docs** | http://localhost:8000/docs | 8000 | Interactive API |
| **Health Check** | http://localhost:8000/health | 8000 | Server status |
| **Ollama** | http://localhost:11434 | 11434 | LLM server |

---

## 📁 Project Structure

```
chatgpt-clone-v6.2/
│
├── backend/                    # FastAPI server
│   ├── app/
│   │   ├── main.py            # API routes
│   │   ├── auth.py            # JWT & password hashing
│   │   ├── llm.py             # Ollama integration
│   │   ├── retrieval.py       # RAG logic
│   │   ├── vector_store.py    # ChromaDB
│   │   ├── storage.py         # File I/O
│   │   ├── schemas.py         # Pydantic models
│   │   └── config.py          # Configuration
│   ├── data/
│   │   ├── users.json         # User accounts
│   │   ├── conversations.json # Chat history
│   │   ├── messages.json      # Messages
│   │   └── documents.json     # Document metadata
│   ├── uploads/               # Uploaded PDFs
│   ├── chroma_db/             # Vector database
│   ├── venv/                  # Python virtual env
│   ├── requirements.txt       # Python packages
│   ├── .env                   # Environment variables
│   └── .env.example           # Example config
│
├── frontend/                   # Next.js app
│   ├── pages/
│   │   └── index.js           # Main page
│   ├── node_modules/          # NPM packages
│   ├── package.json           # NPM config
│   └── next.config.js         # Next.js config
│
├── README.md                  # Original guide
├── RUNNING_PROJECT.md         # Usage guide
├── PROJECT_SETUP_COMPLETE.md  # Setup summary
└── SETUP_GUIDE.md            # This file
```

---

## 🐛 Troubleshooting

### **Issue: Backend won't start**

**Error:** `ModuleNotFoundError: No module named 'uvicorn'`

**Solution:**
```powershell
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

---

### **Issue: "Failed to fetch" error on frontend**

**Error:** `Register error: Failed to fetch`

**Solution:**
1. Check backend is running on port 8000
2. Look for errors in backend terminal
3. Create missing `backend/data/users.json` if needed

```powershell
# Verify backend health
curl http://localhost:8000/health
```

---

### **Issue: Ollama models not found**

**Error:** `Connection refused to http://localhost:11434`

**Solution:**
```powershell
# Check if Ollama is running
Get-Process ollama -ErrorAction SilentlyContinue

# If not running, start Ollama
# Or install manually from https://ollama.ai

# List available models
ollama list

# Download if missing
ollama pull llama3.1
ollama pull nomic-embed-text
```

---

### **Issue: Port already in use**

**Error:** `Address already in use`

**Solution:**
```powershell
# Find what's using the port (e.g., 8000)
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID 12345 /F

# Or use different port
cd backend
python -m uvicorn app.main:app --port 8001
```

---

### **Issue: Frontend won't compile**

**Error:** `npm: command not found`

**Solution:**
```powershell
# Add Node.js to PATH
$env:PATH = "$env:PATH;C:\Program Files\nodejs"

# Or restart PowerShell to reload PATH

# Then try again
npm run dev
```

---

### **Issue: Password validation error**

**Error:** `password cannot be longer than 72 bytes`

**Solution:** Use passwords shorter than 72 characters (usually you won't exceed this)

---

## 🔐 Environment Configuration

Create or edit `backend/.env`:

```env
# LLM Configuration
OLLAMA_CHAT_MODEL=llama3.1
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434

# Security (CHANGE THIS FOR PRODUCTION)
JWT_SECRET_KEY=your-secure-random-key-here

# Database
CHROMA_DIR=chroma_db
DEFAULT_COLLECTION=default
```

---

## 📊 System Monitor

Monitor your services with this script:

```powershell
# Create monitor.ps1
$services = @(
    @{name="Frontend"; url="http://localhost:3000"; port=3000},
    @{name="Backend"; url="http://localhost:8000"; port=8000},
    @{name="Ollama"; url="http://localhost:11434"; port=11434}
)

foreach ($service in $services) {
    $status = (Invoke-WebRequest -Uri $service.url -UseBasicParsing -ErrorAction SilentlyContinue).StatusCode
    if ($status -eq 200) {
        Write-Host "$($service.name): ✅ RUNNING on port $($service.port)" -ForegroundColor Green
    } else {
        Write-Host "$($service.name): ❌ NOT RUNNING" -ForegroundColor Red
    }
}
```

---

## 🎯 Next Steps

After successful setup:

1. **Create multiple collections** for different document types
2. **Upload various PDFs** to test RAG functionality
3. **Ask complex questions** to verify AI responses
4. **Check citations** for document sources
5. **Build your use case** around the platform

---

## 📚 Documentation Links

- **FastAPI:** https://fastapi.tiangolo.com
- **Next.js:** https://nextjs.org/docs
- **Ollama:** https://github.com/ollama/ollama
- **ChromaDB:** https://docs.trychroma.com
- **LLaMA 3.1:** https://llama.meta.com/llama3-1/

---

## 💡 Tips & Best Practices

### **Performance**
- First request may take 30+ seconds (model loading)
- Subsequent requests are faster
- Use small PDFs initially to test

### **Security**
- Change `JWT_SECRET_KEY` in production
- Don't expose backend API to public internet
- Use HTTPS in production

### **Development**
- Backend auto-reloads on file changes
- Frontend hot-reloads in dev mode
- Check browser console for frontend errors
- Check terminal for backend/Ollama logs

### **Storage**
- Users data: `backend/data/users.json`
- Documents: `backend/uploads/`
- Vectors: `backend/chroma_db/`
- Total size grows with documents (1 GB per ~100 PDFs)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check logs** in terminal windows
2. **Verify services** are running on correct ports
3. **Test endpoints** with curl or API docs
4. **Check error messages** - they provide clues
5. **Review this guide** - most issues are covered

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Ollama installed and running
- [ ] Models downloaded (llama3.1, nomic-embed-text)
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Ollama running on port 11434
- [ ] Can access http://localhost:3000
- [ ] Can register new account
- [ ] Can login successfully
- [ ] Can upload PDF
- [ ] Can ask questions and get answers

---

## 🎉 Success!

If all services are running and you can register/login, **congratulations!**

Your ChatGPT Clone with RAG is fully operational and ready to use.

---

**Created:** March 15, 2026  
**Version:** 1.0  
**Status:** ✅ Production Ready
