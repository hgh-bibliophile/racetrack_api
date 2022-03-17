from fastapi_crudrouter import OrmarCRUDRouter

from models.user import User

# ----------
# User
# ----------

router = OrmarCRUDRouter(schema=User)
