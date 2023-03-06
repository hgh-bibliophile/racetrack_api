from typing import List, Optional

import datetime

from .base import BaseModel, BaseId, RequiredBaseId

from .heats import HeatReturnFull, HeatReturnIds, _Car, _Lane, _HeatRun, _HeatRunIds
from .live import WS_HeatRun, WS_HeatRunUpdate

# ----------
# Race
# ----------

class RHeatRunIds(WS_HeatRun):
    pass

class RHeatRunUpdateIds(WS_HeatRunUpdate):
    pass

class RTrack(BaseId):
    name: Optional[str]
    lanes_ct: Optional[int]

class ROwner(BaseId):
    username: Optional[str]
    email: Optional[str]

class RCarCreate(BaseModel):
    car_number: Optional[int]
    name: Optional[str]

class RCar(_Car):
    runs_ct: Optional[int]


class RCarHeatRun(BaseId):
    lane: Optional[_Lane]
    delta_ms: Optional[int]
    mph: Optional[float]
    fps: Optional[float]
    mps: Optional[float]

class RCarSpeed(RCar):
    top_run: Optional[RCarHeatRun]

class HeatBase(BaseModel):
    heat_number: Optional[int]

class HeatReturn(HeatBase, BaseId):
    runs_ct: Optional[int]
    ran_at: Optional[datetime.datetime]

class RHeat(HeatReturn):
    runs: Optional[List[_HeatRun]]

class RHeatRunCreate(BaseModel):
    car_number: int
    lane_number: int
    delta_ms: Optional[int]

class RHeatCreate(BaseModel):
    heat_number: int
    runs: Optional[List[RHeatRunCreate]]

class RHeatRunUpdate(BaseModel):
    id: Optional[int]
    car_number: Optional[int]
    lane_number: Optional[int]
    delta_ms: Optional[int]

class RHeatRunUpdateIds(BaseModel):
    id: int
    delta_ms: int

class RHeatUpdate(BaseModel):
    heat_number: Optional[int]
    runs: Optional[List[RHeatRunUpdate]]

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
    cars: Optional[List[RCarCreate]]

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