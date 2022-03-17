from fastapi_crudrouter import OrmarCRUDRouter

from models.heat import Heat


router = OrmarCRUDRouter(schema=Heat)