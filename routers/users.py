from fastapi_crudrouter import OrmarCRUDRouter

from models.user import User

from .base import CORSRoute

# ----------
# User
# ----------

router = OrmarCRUDRouter(schema=User, route_class=CORSRoute)
