from typing import List, Optional

import datetime

from .base import BaseModel, BaseId, RequiredBaseId

class _Heat(BaseId):
    heat_number: Optional[int]
    name: Optional[str]
    runs_ct: Optional[int]
    ran_at: Optional[datetime.datetime]

class _Lane(BaseId):
    lane_number: Optional[int]
    color: Optional[str]
    distance: Optional[float]

class _HeatRun(BaseId):
    heat: Optional[_Heat]
    lane: Optional[_Lane]
    delta_ms: Optional[int]
    mph: Optional[float]
    fps: Optional[float]
    mps: Optional[float]

class _HeatRunIds(BaseModel):
    heat: Optional[BaseId]
    lane: Optional[BaseId]
    delta_ms: Optional[int]

class CarBase(BaseModel):
    race: Optional[BaseId]
    car_number: Optional[int]
    name: Optional[str]

class CarCreate(CarBase):
    runs: Optional[List[_HeatRunIds]]

class CarReturn(CarBase, BaseId):
    runs_ct: Optional[int]

class CarReturnIds(CarCreate, CarReturn):
    pass

class CarReturnFull(CarReturn):
    runs: Optional[List[_HeatRun]]
