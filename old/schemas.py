from pydantic import BaseModel
from datetime import datetime

## Run
class RunBase(BaseModel):
    mph: int | None = None
    fps: int | None = None
    mps: int | None = None


class RunCreate(RunBase):
    pass


class Run(RunBase):
    id: int
    created_at: datetime.now
    race_id: int
    heat_id: int
    lane_id: int
    car_id: int

    class Config:
        orm_mode = True



## Race
class RaceBase(BaseModel):
    name: str

    place: str | None = None
    race_date: datetime.date | None = None
    race_time: datetime.time | None = None


class RaceCreate(RaceBase):
    pass


class Race(RaceBase):
    id: int
    created_at: datetime.now
    owner_id: int

    class Config:
        orm_mode = True


## User
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    races: list[Race] = []

    class Config:
        orm_mode = True