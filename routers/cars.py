from fastapi_crudrouter import OrmarCRUDRouter

from models.car import Car


router = OrmarCRUDRouter(schema=Car)