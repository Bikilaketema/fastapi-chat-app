from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    status
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import os

app = FastAPI(title="FastAPI Chat App")

static_dir = os.path.join(os.path.dirname(__file__), "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")


class ConnectionManager:
    """
    Manages active WebSocket connections for the chat room.
    """
    def __init__(self):
        """Initializes the connection manager with an empty list of connections."""
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accepts a new WebSocket connection and adds it to the active list.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New connection: {websocket.client.host}. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active list.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Connection closed. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Sends a JSON message to a single, specific WebSocket connection.
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
            await self.disconnect(websocket)

    async def broadcast(self, message: dict):
        """
        Broadcasts a JSON message to all active WebSocket connections.
        """
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                # If sending fails (e.g., connection is broken), disconnect them
                print(f"Error broadcasting message, disconnecting: {e}")
                self.disconnect(connection)

    async def broadcast_system_message(self, message: str):
        """
        Helper to broadcast a message formatted as a "system" message.
        """
        await self.broadcast({"type": "system", "message": message})

    async def broadcast_chat_message(self, username: str, message: str):
        """
        Helper to broadcast a message formatted as a "chat" message.
        """
        await self.broadcast({"type": "chat", "username": username, "message": message})


manager = ConnectionManager()


@app.get("/")
async def get_root():
    """
    Serve the main index.html file for the chat client.
    """
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """
    The main WebSocket endpoint for the chat.
    
    Accepts a connection, notifies the room, and then listens for messages.
    When a message is received, it broadcasts it to all other users.
    When the user disconnects, it notifies the room.
    """
    await manager.connect(websocket)

    try:
        await manager.broadcast_system_message(f"{username} has joined the chat.")
        
        await manager.send_personal_message(
            {"type": "system", "message": "Welcome to the chat!"},
            websocket
        )

        while True:
            data = await websocket.receive_text()
            
            await manager.broadcast_chat_message(username, data)

    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected for {username} with code: {e.code}")
    
    except Exception as e:
        print(f"An unexpected error occurred for {username}: {e}")
    
    finally:
        manager.disconnect(websocket)
        await manager.broadcast_system_message(f"{username} has left the chat.")

