from typing import List, Optional

import datetime

from .base import BaseModel, BaseId, RequiredBaseId

from .heats import HeatReturnFull, HeatReturnIds

# ----------
# Race
# ----------

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

class RHeat(HeatReturnFull):
    pass

class RHeatIds(HeatReturnIds):
    pass

class RHeatRunCreate(BaseModel):
    car_number: int
    lane_number: int
    delta_ms: Optional[int]

class RHeatCreate(BaseModel):
    heat_number: int
    runs: Optional[List[RHeatRunCreate]]

class RaceBase(BaseModel):
    name: Optional[str]
    watch_link: Optional[str]
    place: Optional[str]
    race_date: Optional[datetime.date]
    race_time: Optional[datetime.time]
    status: Optional[str]

class RaceUpdate(RaceBase):
    track: Optional[RequiredBaseId]
    owner: Optional[RequiredBaseId]

class RaceCreate(RaceUpdate):
    cars: Optional[List[RCarBase]]

class RaceReturnBase(RaceBase, BaseId):
    created_date: Optional[datetime.datetime]

class RaceReturn(RaceReturnBase):
    cars_ct: Optional[int]
    heats_ct: Optional[int]

class RaceReturnId(RaceReturn):
    track: Optional[BaseId]
    owner: Optional[BaseId]

class RaceReturnUpdate(RaceReturnBase):
    track: Optional[RTrack]
    owner: Optional[ROwner]
    heats_ct: Optional[int]
    cars_ct: Optional[int]

class RaceReturnFull(RaceReturnUpdate):
    cars: Optional[List[RCar]]