import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from fastapi_crudrouter import OrmarCRUDRouter

from db import database
from models import routers

import ormar

app = FastAPI()

app.state.database = database

origins = [
    "http://racetrack.gratiafides.com",
    "https://racetrack.gratiafides.com",
    "http://api.racetrack.gratiafides.com",
    "https://api.racetrack.gratiafides.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(routers.users)
app.include_router(routers.tracks)
app.include_router(routers.races)
app.include_router(routers.cars)
app.include_router(routers.lanes)
app.include_router(routers.heats)
app.include_router(routers.heat_runs)

# handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ','.join(origins)
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ','.join(origins)
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")