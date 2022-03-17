from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.routing import APIRoute

from typing import Callable


exclude_routes = {
    'get_all_route': False,
    'get_one_route': False,
    'create_route': False,
    'update_route': False,
    'delete_one_route': False,
    'delete_all_route': False
}

class CORSRoute(APIRoute):

    origins = [
        "http://racetrack.gratiafides.com",
        "https://racetrack.gratiafides.com",
        "http://api.racetrack.gratiafides.com",
        "https://api.racetrack.gratiafides.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)

            origin = request.headers.get('origin')
            if origin in CORSRoute.origins:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Methods'] = '*'
                response.headers['Access-Control-Allow-Headers'] = '*'

            return response

        return custom_route_handler

options_router = APIRouter(route_class=CORSRoute)

# handle CORS preflight requests
@options_router.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    return Response()

