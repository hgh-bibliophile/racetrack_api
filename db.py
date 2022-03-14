import sqlalchemy
import databases

ORMAR_DATABASE_URL = "sqlite:///racetrack_api.db"

metadata = sqlalchemy.MetaData()
database = databases.Database(ORMAR_DATABASE_URL)
engine = sqlalchemy.create_engine(ORMAR_DATABASE_URL)