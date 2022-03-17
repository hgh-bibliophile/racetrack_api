import ormar

from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase
from fastapi_users import models

from .base import BaseMeta


class PydUser(models.BaseUser):
    username: str


class PydUserCreate(models.BaseUserCreate):
    username: str


class PydUserUpdate(models.BaseUserUpdate):
    username: str


class PydUserDB(PydUser, models.BaseUserDB):
    pass

class User(OrmarBaseUserModel):
    class Meta(BaseMeta):
        tablename = "users"

    username: str = ormar.String(max_length=64, unique=True, index=True)


async def get_user_db():
    yield OrmarUserDatabase(PydUserDB, User)