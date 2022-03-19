import ormar

from .base import BaseModel, BaseMeta
from .race import Race

# ----------
# Car
# ----------

class Car(BaseModel):
    class Meta(BaseMeta):
        tablename = 'cars'
        constraints = [ormar.UniqueColumns("race", "car_number")]

    race = ormar.ForeignKey(Race, ondelete='CASCADE')

    car_number = ormar.Integer(index=True)
    name = ormar.String(max_length=64)

    @ormar.property_field
    def runs_ct(self):
        return len(self.runs)

    @ormar.property_field
    def top_run(self):
        if self.runs_ct == 0:
            return
        return sorted(self.runs, key=lambda r: float('inf') if r.delta_ms is None or r.delta_ms == 0 else r.delta_ms)[0]