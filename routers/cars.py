from fastapi_crudrouter import OrmarCRUDRouter

from models.car import Car

from .base import CORSRoute

router = OrmarCRUDRouter(schema=Car, route_class=CORSRoute)