from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os


from .database import get_db
from .models import User


JWT_SECRET = os.getenv("JWT_SECRET")
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain, hashed):
     return pwd_context.verify(plain, hashed)


def hash_password(p):
     return pwd_context.hash(p)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
     to_encode = data.copy()
     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
     to_encode.update({"exp": expire})
     return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGO)


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    cred_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
        username: str = payload.get("sub")
        if username is None:
            print("DEBUG: No username in payload")
            raise cred_exc
    except JWTError as e:
        print(f"DEBUG: JWT Error: {e}")
        raise cred_exc
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"DEBUG: User not found: {username}")
        raise cred_exc
    print(f"DEBUG: User found: {user.username}")
    return user


async def get_current_user_from_token(token: str, db: Session) -> User:
    """Helper function to authenticate user from JWT token for WebSocket connections"""
    cred_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise cred_exc
    except JWTError:
        raise cred_exc
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise cred_exc
    return user