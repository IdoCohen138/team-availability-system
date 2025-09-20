from typing import Set, Dict
from fastapi import WebSocket
import json
from .models import User


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, User] = {}
    
    async def connect(self, ws: WebSocket, user: User):
        await ws.accept()
        self.active_connections[ws] = user
    
    def disconnect(self, ws: WebSocket):
        if ws in self.active_connections:
            del self.active_connections[ws]
    
    async def broadcast(self, message: dict):
        data = json.dumps(message)
        for ws in list(self.active_connections.keys()):
            try:
                await ws.send_text(data)
            except Exception:
                self.disconnect(ws)
    
    def get_user_count(self) -> int:
        return len(self.active_connections)


manager = ConnectionManager()