import { useEffect, useState } from "react";

const API = "http://localhost:8000";

export default function Home() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState("");
  const [conversationId, setConversationId] = useState("");
  const [collection, setCollection] = useState("default");
  const [tag, setTag] = useState("");
  const [conversations, setConversations] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState([]);
  const [messages, setMessages] = useState([]);

  async function register() {
    try {
      if (!email || !password) {
        alert("Please enter email and password");
        return;
      }
      const r = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
      });
      if (!r.ok) {
        const d = await r.json();
        throw new Error(d.detail || `Error: ${r.status}`);
      }
      const d = await r.json();
      if (d.user_id) {
        setUserId(d.user_id);
        setEmail("");
        setPassword("");
        alert("Registered successfully");
      } else {
        alert(d.detail || "Register failed");
      }
    } catch (e) {
      alert(`Register error: ${e.message}\nMake sure backend is running at ${API}`);
      console.error("Register error:", e);
    }
  }

  async function login() {
    try {
      if (!email || !password) {
        alert("Please enter email and password");
        return;
      }
      const r = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
      });
      if (!r.ok) {
        const d = await r.json();
        throw new Error(d.detail || `Error: ${r.status}`);
      }
      const d = await r.json();
      if (d.user_id || d.token) {
        setUserId(d.user_id);
        setPassword("");
        await loadConversations(d.user_id);
        alert("Login successful");
      } else {
        alert(d.detail || "Login failed");
      }
    } catch (e) {
      alert(`Login error: ${e.message}\nMake sure backend is running at ${API}`);
      console.error("Login error:", e);
    }
  }

  async function createConversation() {
    try {
      if (!userId) {
        alert("Please login first");
        return;
      }
      const r = await fetch(`${API}/conversations`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id: userId, title: `Chat - ${collection}` })
      });
      if (!r.ok) throw new Error(`Create conversation failed: ${r.status}`);
      const d = await r.json();
      setConversationId(d.id);
      await loadConversations(userId);
    } catch (e) {
      alert(`Error creating conversation: ${e.message}`);
      console.error("Create conversation error:", e);
    }
  }

  async function deleteConversation(id) {
    try {
      const r = await fetch(`${API}/conversations/${id}`, { method: "DELETE" });
      if (!r.ok) throw new Error(`Delete failed: ${r.status}`);
      if (conversationId === id) {
        setConversationId("");
        setMessages([]);
        setAnswer("");
        setCitations([]);
      }
      await loadConversations(userId);
    } catch (e) {
      alert(`Error deleting conversation: ${e.message}`);
      console.error("Delete conversation error:", e);
    }
  }

  async function loadConversations(uid = userId) {
    try {
      if (!uid) return;
      const r = await fetch(`${API}/conversations/${uid}`);
      if (!r.ok) throw new Error(`Load conversations failed: ${r.status}`);
      const d = await r.json();
      setConversations(d);
    } catch (e) {
      console.error("Load conversations error:", e);
    }
  }

  async function loadDocuments(col = collection) {
    try {
      const r = await fetch(`${API}/documents?collection=${encodeURIComponent(col)}`);
      if (!r.ok) throw new Error(`Load documents failed: ${r.status}`);
      const d = await r.json();
      setDocuments(d || []);
    } catch (e) {
      console.error("Load documents error:", e);
      setDocuments([]);
    }
  }

  async function loadMessages(cid = conversationId) {
    try {
      if (!cid) return;
      const r = await fetch(`${API}/messages/${cid}`);
      if (!r.ok) throw new Error(`Load messages failed: ${r.status}`);
      const d = await r.json();
      setMessages(d || []);
    } catch (e) {
      console.error("Load messages error:", e);
    }
  }

  async function ask() {
    try {
      if (!userId) {
        alert("Please login first");
        return;
      }
      if (!question.trim()) {
        alert("Please enter a question");
        return;
      }
      if (!conversationId) {
        await createConversation();
        return;
      }
      const r = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          user_id: userId,
          conversation_id: conversationId,
          message: question,
          collection,
          use_documents: true
        })
      });
      if (!r.ok) throw new Error(`Chat failed: ${r.status}`);
      const d = await r.json();
      setAnswer(d.reply || "");
      setCitations(d.citations || []);
      setQuestion("");
      await loadMessages(conversationId);
    } catch (e) {
      alert(`Error sending message: ${e.message}`);
      console.error("Chat error:", e);
    }
  }

  async function uploadDoc(e) {
    try {
      const file = e.target.files?.[0];
      if (!file) return;
      if (!userId) {
        alert("Please login first");
        return;
      }
      const fd = new FormData();
      fd.append("file", file);
      fd.append("collection", collection);
      fd.append("tag", tag);
      const r = await fetch(`${API}/documents/upload`, { method: "POST", body: fd });
      if (!r.ok) throw new Error(`Upload failed: ${r.status}`);
      await loadDocuments(collection);
      alert("Document uploaded successfully");
      e.target.value = "";
    } catch (e) {
      alert(`Upload error: ${e.message}`);
      console.error("Upload error:", e);
    }
  }

  async function deleteDocument(id) {
    try {
      const r = await fetch(`${API}/documents/${id}`, { method: "DELETE" });
      if (!r.ok) throw new Error(`Delete failed: ${r.status}`);
      await loadDocuments(collection);
    } catch (e) {
      alert(`Error deleting document: ${e.message}`);
      console.error("Delete document error:", e);
    }
  }

  useEffect(() => { loadDocuments(collection); }, [collection]);
  useEffect(() => { if (conversationId) loadMessages(conversationId); }, [conversationId]);

  return (
    <div style={{padding: 30, fontFamily: "Arial", background: "#0b1020", color: "white", minHeight: "100vh"}}>
      <h1>V6.2 Better Vector RAG</h1>

      <div style={{display: "grid", gridTemplateColumns: "1fr 2fr", gap: 20}}>
        <div>
          <div style={{border: "1px solid #333", padding: 15, marginBottom: 15}}>
            <h3>Auth</h3>
            <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} style={{width:"100%",marginBottom:8}} />
            <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} style={{width:"100%",marginBottom:8}} />
            <div style={{display:"flex", gap:8}}>
              <button onClick={register}>Register</button>
              <button onClick={login}>Login</button>
            </div>
            <p>User ID: {userId || "-"}</p>
          </div>

          <div style={{border: "1px solid #333", padding: 15, marginBottom: 15}}>
            <h3>Collection</h3>
            <input value={collection} onChange={e => setCollection(e.target.value)} placeholder="Collection name" style={{width:"100%",marginBottom:8}} />
            <input value={tag} onChange={e => setTag(e.target.value)} placeholder="Optional tag" style={{width:"100%",marginBottom:8}} />
          </div>

          <div style={{border: "1px solid #333", padding: 15, marginBottom: 15}}>
            <h3>Documents</h3>
            <input type="file" accept="application/pdf" onChange={uploadDoc} />
            <ul>
              {documents.map(d => (
                <li key={d.id}>
                  {d.name} ({d.collection})
                  <button onClick={() => deleteDocument(d.id)} style={{marginLeft:8}}>Delete</button>
                </li>
              ))}
            </ul>
          </div>

          <div style={{border: "1px solid #333", padding: 15}}>
            <h3>Conversations</h3>
            <button onClick={createConversation}>New Chat</button>
            <ul>
              {conversations.map(c => (
                <li key={c.id}>
                  <button onClick={() => setConversationId(c.id)}>{c.title}</button>
                  <button onClick={() => deleteConversation(c.id)} style={{marginLeft:8}}>Delete</button>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div>
          <div style={{border: "1px solid #333", padding: 15, marginBottom: 15}}>
            <h3>Chat</h3>
            <textarea
              value={question}
              onChange={e => setQuestion(e.target.value)}
              rows={4}
              style={{width:"100%", marginBottom:8}}
              placeholder="Ask from uploaded documents"
            />
            <button onClick={ask}>Send</button>
            <div style={{marginTop:15, whiteSpace:"pre-wrap"}}>{answer}</div>
            {citations.length > 0 && (
              <div style={{marginTop:15}}>
                <strong>Sources</strong>
                <ul>
                  {citations.map((c, i) => (
                    <li key={i}>
                      {c.document} - chunk {c.chunk_index}{c.tag ? ` - tag: ${c.tag}` : ""}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div style={{border: "1px solid #333", padding: 15}}>
            <h3>Message History</h3>
            {messages.map(m => (
              <div key={m.id} style={{marginBottom:12, paddingBottom:12, borderBottom:"1px solid #222"}}>
                <div><strong>Q:</strong> {m.question}</div>
                <div><strong>A:</strong> {m.answer}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
