import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import WebSocket, WebSocketDisconnect, Query, HTTPException


from .database import Base, engine, get_db
from .models import User
from .schemas import Token, LoginRequest, UserPublic, UsersList, UpdateStatus, STATUSES
from .auth import create_access_token, verify_password, get_current_user, get_current_user_from_token
from . import seed
from .ws import manager

app = FastAPI(title="Team Availability API")


origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# Create tables and seed on startup
@app.on_event("startup")
def on_startup():
     print("DEBUG: Starting application startup...")
     Base.metadata.create_all(bind=engine)
     print("DEBUG: Database tables created/verified")
     
     seed_env = os.getenv("SEED", "0")
     print(f"DEBUG: SEED environment variable: {seed_env}")
     
     if seed_env == "1":
          print("DEBUG: SEED=1 detected, running seed process...")
          try:
               with next(get_db()) as db:
                    seed.run(db)
          except Exception as e:
               print(f"DEBUG: Error during seeding: {e}")
               raise
     else:
          print("DEBUG: SEED not set to 1, skipping seed process")


@app.post("/api/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
     user = db.query(User).filter(User.username == form.username).first()
     if not user or not verify_password(form.password, user.password_hash):
          raise HTTPException(status_code=401, detail="Invalid username or password")
     token = create_access_token({"sub": user.username})
     return {"access_token": token}


@app.get("/api/me", response_model=UserPublic)
def me(current: User = Depends(get_current_user)):
     return current


@app.get("/api/statuses", response_model=List[str])
def list_statuses():
     return STATUSES


@app.get("/api/users", response_model=UsersList)
def list_users(q: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
     query = db.query(User)
     if q:
          like = f"%{q.lower()}%"
          query = query.filter(User.full_name.ilike(like) | User.username.ilike(like))
     if status:
          query = query.filter(User.status == status)
     users = query.order_by(User.full_name.asc()).all()
     # Exclude password_hash implicitly via schema
     return {"items": users}


@app.patch("/api/me/status", response_model=UserPublic)
async def update_my_status(body: UpdateStatus, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
     if body.status not in STATUSES:
          raise HTTPException(status_code=400, detail="Invalid status")
     current.status = body.status
     db.add(current)
     db.commit()
     db.refresh(current)
     # Broadcast change
     await manager.broadcast({"type": "status_changed", "user": {"id": current.id, "full_name": current.full_name, "status": current.status}})
     return current

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket, token: str = Query(...)):
    """WebSocket endpoint for real-time updates - requires authentication"""
    try:
        db = next(get_db())
        try:
            user = await get_current_user_from_token(token, db)
            await manager.connect(ws, user)
            print(f"DEBUG: User {user.username} connected to WebSocket")
            try:
                while True:
                    await ws.receive_text()
            except WebSocketDisconnect:
                print(f"DEBUG: User {user.username} disconnected from WebSocket")
                manager.disconnect(ws)
        finally:
            db.close()
    except HTTPException as e:
        print(f"DEBUG: WebSocket authentication failed: {e.detail}")
        await ws.close(code=1008, reason="Authentication failed")
    except Exception as e:
        print(f"DEBUG: WebSocket connection error: {e}")
        await ws.close(code=1011, reason="Internal server error")