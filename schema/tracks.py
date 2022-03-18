import pydantic
from typing import List, Optional

# ----------
# Track
# ----------

class BaseId(pydantic.BaseModel):
    class Config:
        orm_mode = True

    id: Optional[int]

class TLaneUpdate(pydantic.BaseModel):
    class Config:
        orm_mode = True

    lane_number: Optional[int]
    color: Optional[str]
    distance: Optional[float]

class TLane(TLaneUpdate, BaseId):
    pass

class TrackBase(pydantic.BaseModel):
    class Config:
        orm_mode = True

    name: Optional[str]

class TrackCreate(TrackBase):
    lanes: Optional[List[TLaneUpdate]]

class TrackReturn(TrackBase, BaseId):
    lanes_ct: Optional[int]

class TrackReturnFull(TrackReturn):
    lanes: Optional[List[TLane]]
