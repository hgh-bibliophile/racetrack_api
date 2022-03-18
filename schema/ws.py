from typing import Optional

from .base import BaseModel, BaseId

class _Lane(BaseId):
    lane_number: int

class WS_HeatRun(BaseId):
    car: BaseId
    lane: _Lane
    delta_ms: Optional[int]

class WS_HeatRunUpdate(BaseModel):
    id: int
    delta_ms: int