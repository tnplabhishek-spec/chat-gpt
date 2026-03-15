# ChatGPT Clone V6.2 with RAG - Quick Start

**Get started in 5 minutes!**

---

## 🚀 Quick Setup (One-Time)

### **1️⃣ Install Requirements**
```powershell
# Python (if needed)
winget install Python.Python.3.11

# Node.js (if needed)
winget install OpenJS.NodeJS

# Ollama (if needed)
winget install Ollama.Ollama
```

### **2️⃣ Download AI Models**
```powershell
ollama pull llama3.1
ollama pull nomic-embed-text
```

### **3️⃣ Setup Backend**
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### **4️⃣ Setup Frontend**
```powershell
cd frontend
npm install
```

---

## 🎯 Run Every Time (3 Terminals)

### **Terminal 1: Ollama**
```powershell
# Ollama runs automatically as a service
# Or start manually if needed:
"$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```
✅ http://localhost:11434

---

### **Terminal 2: Backend**
```powershell
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```
✅ http://localhost:8000  
📚 Docs: http://localhost:8000/docs

---

### **Terminal 3: Frontend**
```powershell
cd frontend
npm run dev
```
✅ http://localhost:3000

---

## 🎬 Using the App

1. **Open** http://localhost:3000
2. **Register** with email and password
3. **Login** with your credentials
4. **Upload** a PDF document
5. **Ask** questions about the document
6. **Get** AI responses with citations

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| **Backend won't start** | `pip install -r requirements.txt` in backend dir |
| **Frontend won't start** | `npm install` in frontend dir |
| **Models not found** | `ollama pull llama3.1 && ollama pull nomic-embed-text` |
| **Port in use** | Change port or kill process: `taskkill /PID xxxxx /F` |
| **"Failed to fetch"** | Check backend is running on port 8000 |

---

## ✅ Verify Services

```powershell
# Test Frontend
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing

# Test Backend
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing

# Test Ollama
Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing
```

All should return **200 OK**

---

## 📋 Full Documentation

- **Setup Details:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Project Info:** [PROJECT_SETUP_COMPLETE.md](PROJECT_SETUP_COMPLETE.md)
- **Running Guide:** [RUNNING_PROJECT.md](RUNNING_PROJECT.md)

---

**Version:** 1.0  
**Status:** ✅ Ready to Use
