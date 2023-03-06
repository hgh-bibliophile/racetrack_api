import ormar

#from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase
#from fastapi_users import models

from .base import BaseModel, BaseMeta



class User(BaseModel):
    class Meta(BaseMeta):
        tablename = "users"

    email: str = ormar.String(max_length=64, unique=True, index=True)
    username: str = ormar.String(max_length=64, unique=True, index=True)


async def get_user_db():
    yield OrmarUserDatabase(PydUserDB, User)