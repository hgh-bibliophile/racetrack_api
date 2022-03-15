import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from starlette.middleware.cors import CORSMiddleware

from fastapi_crudrouter import OrmarCRUDRouter

from db import database
from models import routers

import ormar

app = FastAPI()

origins = [
    "http://api.racetrack.gratiafides.com",
    "https://api.racetrack.gratiafides.com",
    "http://localhost:3000",
]

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

app.include_router(routers.users)
app.include_router(routers.tracks)
app.include_router(routers.races)
app.include_router(routers.cars)
app.include_router(routers.lanes)
app.include_router(routers.heats)
app.include_router(routers.heat_runs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")