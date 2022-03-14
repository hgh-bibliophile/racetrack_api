import pydantic
from typing import List, Optional

# ----------
# Lane
# ----------

class LaneUpdate(pydantic.BaseModel):
    class Config:
        orm_mode = True

    lane_number: Optional[int]
    track: Optional[int]
    color: Optional[str]
    distance: Optional[float]

class LTrackId(pydantic.BaseModel):
    class Config:
        orm_mode = True

    id: Optional[int]

class LTrack(LTrackId):
    name: Optional[str]

class LaneReturn(LaneUpdate):
    id: Optional[int]

class LaneReturn_TrackId(LaneReturn):
    track: Optional[LTrackId]

class LaneReturn_Track(LaneReturn):
    track: Optional[LTrack]