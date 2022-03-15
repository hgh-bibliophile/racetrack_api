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

origins = [
    "http://racetrack.gratiafides.com",
    "https://racetrack.gratiafides.com",
    "http://api.racetrack.gratiafides.com",
    "https://api.racetrack.gratiafides.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

def cors_headers(request: Request, response: Response) -> Response:
    origin = request.headers.get('origin')
    if origin in origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    return cors_headers(request, response)

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    return cors_headers(request, response)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")