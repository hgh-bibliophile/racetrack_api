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
        constraints = [
            ormar.UniqueColumns("heat", "car"),
            ormar.UniqueColumns("heat", "lane")]

    heat = ormar.ForeignKey(Heat, related_name="runs", ondelete='CASCADE')
    car = ormar.ForeignKey(Car, related_name="runs", ondelete='CASCADE')
    lane = ormar.ForeignKey(Lane, skip_reverse=True, ondelete='SET NULL')

    delta_ms = ormar.Integer(nullable=True)
