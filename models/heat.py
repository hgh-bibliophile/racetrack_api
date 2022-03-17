import ormar

from .base import BaseModel, BaseMeta, DateFieldMixin
from .race import Race

# ----------
# Heat
# ----------

class Heat(BaseModel, DateFieldMixin):
    class Meta(BaseMeta):
        tablename = 'heats'
        constraints = [ormar.UniqueColumns("race", "heat_number")]

    race = ormar.ForeignKey(Race)

    heat_number = ormar.Integer(index=True)

    ran_at = ormar.DateTime(nullable=True)

