from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from fastapi_websocket_pubsub import PubSubEndpoint

from models.heat import Heat

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
  prefix="/ws",
  tags=["Websockets"],
  responses={404: {"description": "Not found"}},
)


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

manager = ConnectionManager()

# Register a regular HTTP route
@router.get("/{race_link}/heat/{heat_num}")
async def trigger_heat(race_link: str, heat_num: int):
    await manager.broadcast(race_link, f"Trigger recieved: {race_link} {heat_num}")
    return await Heat.objects.filter(race__watch_link=race_link, heat_number=heat_num).get()

# Register a regular HTTP route
@router.put("/{race_link}/heat/{heat_id}")
async def trigger_events(race_link: str):
    await manager.broadcast(race_link, "Trigger recieved")

@router.websocket("/watch/{race_link}")
async def websocket_endpoint(websocket: WebSocket, race_link: str):
    await manager.connect(race_link, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(race_link, websocket)
