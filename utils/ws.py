from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, channel: str, websocket: WebSocket):
        await websocket.accept()
        self.channel(channel).append(websocket)

    def disconnect(self, channel: str, websocket: WebSocket):
        self.channel(channel).remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, channel: str, message: str):
        for connection in self.channel(channel):
            await connection.send_text(message)

    def channel(self, name: str):
        if name not in self.active_connections:
            self.active_connections[name] = []
        return self.active_connections[name]