import pydantic
from typing import List, Optional
import datetime
# ----------
# Race
# ----------

class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True

class BaseId(BaseModel):
    id: Optional[int]

class RequiredBaseId(BaseModel):
    id: int

class RTrack(BaseId):
    name: Optional[str]
    lanes_ct: Optional[int]

class ROwner(BaseId):
    username: Optional[str]
    email: Optional[str]

class RCarBase(BaseModel):
    car_number: Optional[int]
    name: Optional[str]

class RCar(RCarBase, BaseId):
    runs_ct: Optional[int]


class RaceBase(pydantic.BaseModel):
    class Config:
        orm_mode = True

    name: Optional[str]
    watch_link: Optional[str]
    place: Optional[str]
    race_date: Optional[datetime.date]
    race_time: Optional[datetime.time]
    status: Optional[str]

class RaceUpdate(RaceBase):
    class Config:
        orm_mode = True

    track: Optional[RequiredBaseId]
    owner: Optional[RequiredBaseId]
    cars: Optional[List[RCarBase]]

class RaceReturnBase(RaceBase, BaseId):
    created_date: Optional[datetime.datetime]

class RaceReturn(RaceReturnBase):
    cars_ct: Optional[int]
    heats_ct: Optional[int]

class RaceReturnId(RaceReturn):
    track: Optional[BaseId]
    owner: Optional[BaseId]

class RaceReturnFull(RaceReturnBase):
    track: Optional[RTrack]
    heats_ct: Optional[int]
    cars_ct: Optional[int]
    cars: Optional[List[RCar]]
    owner: Optional[ROwner]