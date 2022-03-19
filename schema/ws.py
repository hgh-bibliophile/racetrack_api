from typing import Optional

from .base import BaseModel, BaseId

class _Lane(BaseId):
    lane_number: int
    color: str

class _Car(BaseId):
    car_number: int
    name: str

class WS_HeatRun(BaseId):
    car: _Car
    lane: _Lane
    delta_ms: Optional[int]
    mph: Optional[float]
    fps: Optional[float]
    mps: Optional[float]

class WS_HeatRunUpdate(BaseModel):
    id: int
    delta_ms: int
