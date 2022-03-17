from fastapi_crudrouter import OrmarCRUDRouter

from models.heat_run import HeatRun


router = OrmarCRUDRouter(schema=HeatRun)