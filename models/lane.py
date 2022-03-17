import ormar

from .base import BaseModel, BaseMeta
from .track import Track

# ----------
# Lane
# ----------

class Lane(BaseModel):
    class Meta(BaseMeta):
        tablename = 'lanes'
        constraints = [ormar.UniqueColumns("track", "lane_number")]

    track = ormar.ForeignKey(Track)

    lane_number = ormar.Integer(index=True)

    color: str = ormar.String(max_length=16, nullable=True)
    distance: float = ormar.Float(default=24.0)