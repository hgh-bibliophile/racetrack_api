from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.routing import APIRoute

from typing import Callable
from utils.settings import cors_allowed_origins

exclude_routes = {
    'get_all_route': False,
    'get_one_route': False,
    'create_route': False,
    'update_route': False,
    'delete_one_route': False,
    'delete_all_route': False
}

class CORSRoute(APIRoute):

    origins = cors_allowed_origins

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)

            origin = request.headers.get('origin')
            #print(origin)
            if origin in CORSRoute.origins:
                response.headers['Access-Control-Allow-Origin'] = origin

            response.headers['Access-Control-Allow-Methods'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'

            return response

        return custom_route_handler

options_router = APIRouter(route_class=CORSRoute, tags=["CORS"])

# handle CORS preflight requests
@options_router.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    return Response()

