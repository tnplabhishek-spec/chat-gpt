from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import JWT_SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Ensure password doesn't exceed bcrypt's 72-byte limit
    password = str(password)[:72]
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # Fallback: use plaintext if hashing fails (not recommended for production)
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    password = str(password)[:72]
    try:
        return pwd_context.verify(password, hashed)
    except:
        # Fallback: check sha256 hash
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest() == hashed

def create_token(user_id: str):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
