from fastapi import WebSocket
from typing import List


class WebSocketManager:
    """
    Manages WebSocket connections.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Add a WebSocket connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection.
        """
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """
        Send a message to all connected WebSocket clients.
        """
        for connection in self.active_connections:
            await connection.send_text(message)
