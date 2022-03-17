import ormar

from .base import BaseModel, BaseMeta
from .lane import Lane
from .car import Car
from .heat import Heat

# ----------
# HeatRun
# ----------

class HeatRun(BaseModel):
    class Meta(BaseMeta):
        tablename = 'heat_runs'

    heat = ormar.ForeignKey(Heat, related_name="runs")
    car = ormar.ForeignKey(Car, related_name="runs")
    lane = ormar.ForeignKey(Lane, skip_reverse=True)

    delta_ms = ormar.Integer()
