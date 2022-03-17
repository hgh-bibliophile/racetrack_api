import datetime
import ormar
import sqlalchemy
from db import database, metadata
from fastapi_users import models as user_models
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase
# ----------
# Mixins
# ----------

class DateFieldMixin:
    created_date = ormar.DateTime(server_default=sqlalchemy.func.now(),  sql_nullable=False)

class PKMixin:
    id: int = ormar.Integer(primary_key=True)

# ----------
# BaseMeta & BaseModel -> Most Classes should inherit both
# ----------

class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata

class BaseModel(ormar.Model, PKMixin):
    class Meta(BaseMeta):
        abstract = True

# ----------
# User
# ----------

class UserM(user_models.BaseUser):
    username: str


class UserCreate(user_models.BaseUserCreate):
    username: str


class UserUpdate(user_models.BaseUserUpdate):
    username: str


class UserDB(User, user_models.BaseUserDB):
    username: str

class User(OrmarBaseUserModel):
    class Meta(BaseMeta):
        tablename = "users"

    username: str = ormar.String(max_length=64, unique=True, index=True)



async def get_user_db():
    yield OrmarUserDatabase(UserDB, User)

# class User(BaseModel):
#     class Meta(BaseMeta):
#         tablename = 'users'

#     username: str = ormar.String(max_length=64, unique=True, index=True)
#     password: str = ormar.String(max_length=128,
#                                 encrypt_secret="X$u54$C*x9^5",
#                                 encrypt_backend=ormar.EncryptBackends.HASH)

#     is_active: bool = ormar.Boolean(default=True)

# #CreateUser = User.get_pydantic(exclude={"id": ...,"is_active": ...})

# ----------
# Track
# ----------

class Track(BaseModel):
    class Meta(BaseMeta):
        tablename = 'tracks'

    name = ormar.String(max_length=50, unique=True)  # WetzelRoadDerby 3-19-2022

    @ormar.property_field
    def lanes_ct(self):
        return len(self.lanes)

# ----------
# Race
# ----------

class Race(BaseModel, DateFieldMixin):
    class Meta(BaseMeta):
        tablename = 'races'

    name: str = ormar.String(max_length=64, index=True)
    watch_link: str = ormar.String(max_length=25, index=True, unique=True)
    track = ormar.ForeignKey(Track, skip_reverse=True)

    place: str = ormar.String(max_length=255, nullable=True)
    race_date = ormar.Date(index=True, nullable=True)
    race_time = ormar.Time(nullable=True)

    status = ormar.String(max_length=6, default='future', nullable=False, choices=['future', 'active', 'closed'])

    owner = ormar.ForeignKey(User)

# ----------
# Lane
# ----------

class Lane(BaseModel):
    class Meta(BaseMeta):
        tablename = 'lanes'
        constraints = [ormar.UniqueColumns("track", "lane_number")]

    track = ormar.ForeignKey(Track)

    lane_number = ormar.Integer(index=True)

    color: str = ormar.String(max_length=16, nullable=True)
    distance: float = ormar.Float(default=24.0)

# ----------
# Car
# ----------

class Car(BaseModel):
    class Meta(BaseMeta):
        tablename = 'cars'
        constraints = [ormar.UniqueColumns("race", "car_number")]

    race = ormar.ForeignKey(Race)

    car_number = ormar.Integer(index=True)
    name = ormar.String(max_length=64)

# ----------
# Heat
# ----------

class Heat(BaseModel, DateFieldMixin):
    class Meta(BaseMeta):
        tablename = 'heats'
        constraints = [ormar.UniqueColumns("race", "heat_number")]

    race = ormar.ForeignKey(Race)

    heat_number = ormar.Integer(index=True)

    ran_at = ormar.DateTime(nullable=True)

# ----------
# HeatRun
# ----------

class HeatRun(BaseModel):
    class Meta(BaseMeta):
        tablename = 'heat_runs'

    heat = ormar.ForeignKey(Heat, related_name="runs")
    car = ormar.ForeignKey(Car)
    lane = ormar.ForeignKey(Lane, skip_reverse=True)

    delta_ms = ormar.Integer()

