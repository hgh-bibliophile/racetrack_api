import sqlalchemy
import databases

import os

POSTGRESQL_DATABASE_URL = os.environ.get('DATABASE_URL', False)
SQLITE_DATABASE_URL = "sqlite:///racetrack_api.db"

ORMAR_DATABASE_URL = SQLITE_DATABASE_URL if not  POSTGRESQL_DATABASE_URL else POSTGRESQL_DATABASE_URL

metadata = sqlalchemy.MetaData()
database = databases.Database(ORMAR_DATABASE_URL)
engine = sqlalchemy.create_engine(ORMAR_DATABASE_URL)