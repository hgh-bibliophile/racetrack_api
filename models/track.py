import ormar

from .base import BaseModel, BaseMeta

# ----------
# Track
# ----------

class Track(BaseModel):
    class Meta(BaseMeta):
        tablename = 'tracks'

    name = ormar.String(max_length=50, unique=True)  # WetzelRoadDerby 3-19-2022

    @ormar.property_field
    def lanes_ct(self):
        return len(self.lanes)