import ormar

from .base import BaseModel, BaseMeta, DateFieldMixin
from .user import User
from .track import Track

# ----------
# Race
# ----------

class Race(BaseModel, DateFieldMixin):
    class Meta(BaseMeta):
        tablename = 'races'

    name: str = ormar.String(max_length=64, index=True)
    watch_link: str = ormar.String(max_length=25, index=True, unique=True)
    track = ormar.ForeignKey(Track, skip_reverse=True, ondelete='SET NULL')

    place: str = ormar.String(max_length=255, nullable=True)
    race_date = ormar.Date(index=True, nullable=True)
    race_time = ormar.Time(nullable=True)

    status = ormar.String(max_length=6, default='future', nullable=False, choices=['future', 'active', 'closed'])

    owner = ormar.ForeignKey(User, ondelete='CASCADE')

    @ormar.property_field
    def cars_ct(self):
        return len(self.cars)

    @ormar.property_field
    def heats_ct(self):
        return len(self.heats)