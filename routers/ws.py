from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from utils.ws import ConnectionManager

from models.heat import Heat

from .base import CORSRoute

router = APIRouter(
  prefix="/ws",
  tags=["Websockets"],
  responses={404: {"description": "Not found"}},
  route_class=CORSRoute
)

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