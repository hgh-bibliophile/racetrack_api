import sqlalchemy
import databases
from sqlalchemy import pool

import os

POSTGRESQL_DATABASE_URL = os.environ.get('DATABASE_URL', False)
SQLITE_DATABASE_URL = "sqlite:///racetrack_api.db"

if not POSTGRESQL_DATABASE_URL:
    ORMAR_DATABASE_URL = SQLITE_DATABASE_URL
    database = databases.Database(ORMAR_DATABASE_URL)
else:
    ORMAR_DATABASE_URL = POSTGRESQL_DATABASE_URL
    database = databases.Database(ORMAR_DATABASE_URL, min_size=2, max_size=5)

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(ORMAR_DATABASE_URL)