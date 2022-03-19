from typing import List, Optional

import datetime

from .base import BaseModel, BaseId, RequiredBaseId

class _Car(BaseId):
    car_number: Optional[int]
    name: Optional[str]
    #runs_ct: Optional[int]

class _Lane(BaseId):
    lane_number: Optional[int]
    color: Optional[str]
    distance: Optional[float]

class _HeatRun(BaseId):
    car: Optional[_Car]
    lane: Optional[_Lane]
    delta_ms: Optional[int]
    mph: Optional[float]
    fps: Optional[float]
    mps: Optional[float]

class _HeatRunIds(BaseModel):
    car: Optional[BaseId]
    lane: Optional[BaseId]
    delta_ms: Optional[int]

class HeatBase(BaseModel):
    race: Optional[BaseId]
    heat_number: Optional[int]

class HeatCreate(HeatBase):
    runs: Optional[List[_HeatRunIds]]

class HeatReturn(HeatBase, BaseId):
    runs_ct: Optional[int]
    ran_at: Optional[datetime.datetime]

class HeatReturnIds(HeatCreate, HeatReturn):
    pass

class HeatReturnFull(HeatReturn):
    runs: Optional[List[_HeatRun]]
