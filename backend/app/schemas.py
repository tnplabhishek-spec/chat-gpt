from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ConversationCreateRequest(BaseModel):
    user_id: str
    title: str = "New Chat"

class ChatRequest(BaseModel):
    user_id: str
    conversation_id: str
    message: str
    collection: str = "default"
    use_documents: bool = True

class UploadMetaRequest(BaseModel):
    collection: str = "default"
    tag: str = ""
