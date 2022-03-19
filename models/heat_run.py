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

    def get_sec(self):
        return self.delta_ms / 1000000

    @ormar.property_field
    def mph(self):
        if self.delta_ms == 0 or self.delta_ms == None or self.lane.distance == None:
            return

        hours = self.get_sec() / 3600
        miles = (self.lane.distance / 12) / 5280

        return miles / hours * 24.444444444444444444

    @ormar.property_field
    def mps(self):
        if self.delta_ms == 0 or self.delta_ms == None or self.lane.distance == None:
            return

        meters = self.lane.distance / 39.37007874015748

        return meters / self.get_sec()

    @ormar.property_field
    def fps(self):
        if self.delta_ms == 0 or self.delta_ms == None or self.lane.distance == None:
            return

        feet = self.lane.distance / 12

        return feet / self.get_sec()
