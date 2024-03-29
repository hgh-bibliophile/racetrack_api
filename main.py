import uvicorn
from fastapi import FastAPI, Response

from db import database
#from ws import ws_router

from routers import users, tracks, races, cars, lanes, heats, heat_runs, live
from routers.base import CORSRoute, options_router

from utils import settings
from utils.socket import SocketManager

app = FastAPI(title='Racetrack.io API')

app.router.route_class = CORSRoute
app.state.database = database

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()

@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

app.include_router(users.router)
app.include_router(tracks.router)
app.include_router(races.router)
app.include_router(cars.router)
app.include_router(lanes.router)
app.include_router(heats.router)
app.include_router(heat_runs.router)
app.include_router(live.router)
app.include_router(options_router)

@app.get('/live/{race_link}')
async def watch(race_link: str):
    await live.sio.emit('start_heat', {'data':'Good'}, room=race_link)
    return 'Good'



app.mount("/live", live.sio.merge(app))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")