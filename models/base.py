import ormar
import sqlalchemy
from db import database, metadata

# ----------
# Mixins
# ----------

class DateFieldMixin:
    created_date = ormar.DateTime(server_default=sqlalchemy.func.now(),  sql_nullable=False)

class PKMixin:
    id: int = ormar.Integer(primary_key=True)

# ----------
# BaseMeta & BaseModel -> Most Classes should inherit both
# ----------

class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata

class BaseModel(ormar.Model, PKMixin):
    class Meta(BaseMeta):
        abstract = True
