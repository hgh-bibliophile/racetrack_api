from sqlalchemy import Column, ForeignKey, UniqueConstraint
import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(sqla.Integer, primary_key=True, index=True)

    username = Column(sqla.String, unique=True, index=True)
    hashed_password = Column(sqla.String)

    is_active = Column(sqla.Boolean, default=True)

    # Parent of
    races = relationship("Race", cascade="all,delete", back_populates="owner")


class Race(Base):
    __tablename__ = "races"

    id = Column(sqla.Integer, primary_key=True, index=True)

    name = Column(sqla.String, index=True)

    place = Column(sqla.String)
    race_date = Column(sqla.Date, index=True)
    race_time = Column(sqla.Time)

    owner_id = Column(sqla.Integer, ForeignKey("users.id"))

    created_at = Column(sqla.DateTime, default=datetime.now, nullable=False, server_default=text('0'))

    # Child of
    owner = relationship("User", back_populates="races")

    # Parent of
    lanes = relationship("Lane", cascade="all,delete", back_populates="race")
    cars = relationship("Car", cascade="all,delete", back_populates="race")
    heats = relationship("Heat", cascade="all,delete", back_populates="race")
    runs = relationship("Run", cascade="all,delete", back_populates="race")


class Lane(Base):
    __tablename__ = "lanes"

    # PK
    id = Column(sqla.Integer, primary_key=True, index=True)

    # Required
    number = Column(sqla.Integer, index=True)

    # Optional
    color = Column(sqla.String)
    distance = Column(sqla.Float)

    race_id = Column(sqla.Integer, ForeignKey("races.id"))

    ## FK Relationships
    # Child of
    race = relationship('Race', back_populates='lanes')

    # Parent of
    heats = relationship("Heat", cascade="all,delete", back_populates="lane")
    runs = relationship("Run", cascade="all,delete", back_populates="lane")

    # Unique Contraints
    __table_args__ = (UniqueConstraint(race, number),)


class Car(Base):
    __tablename__ = 'cars'

    id = Column(sqla.Integer, primary_key=True, index=True)

    number = Column(sqla.Integer, index=True)
    name = Column(sqla.String)

    race_id = Column(sqla.Integer, ForeignKey("races.id"))

    ## FK Relationships
    # Child of
    race = relationship('Race', back_populates='cars')

    # Parent of
    heats = relationship("Heat", cascade="all,delete", back_populates="car")
    runs = relationship("Run", cascade="all,delete", back_populates="car")

    # Unique Contraints
    __table_args__ = (UniqueConstraint(race, number),)

class Heat(Base):
    __tablename__ = 'heats'

    id = Column(sqla.Integer, primary_key=True, index=True)

    number = Column(sqla.Integer, index=True)
    track_data = Column(sqla.JSON)
    ran_at = Column(sqla.DateTime)

    race_id = Column(sqla.Integer, ForeignKey("races.id"))

    created_at = Column(sqla.DateTime, default=datetime.now, nullable=False, server_default=text('0'))

    # FK Relationships
    # Child of
    race = relationship('Race', back_populates='heats')

    # Parent of
    runs = relationship("Run", cascade="all,delete", back_populates="heat")

    # Unique Contraints
    __table_args__ = (UniqueConstraint(race, number),)



class Run(Base):
    __tablename__ = 'runs'

    id = Column(sqla.Integer, primary_key=True, index=True)

    mph = Column(sqla.Float)
    fps = Column(sqla.Float)
    mps = Column(sqla.Float)

    race_id = Column(sqla.Integer, ForeignKey("races.id"))
    heat_id = Column(sqla.Integer, ForeignKey("heats.id"))
    lane_id = Column(sqla.Integer, ForeignKey("lanes.id"))
    car_id = Column(sqla.Integer, ForeignKey("cars.id"))

    created_at = Column(sqla.DateTime, default=datetime.now, nullable=False, server_default=text('0'))

    # FK Relationships
    # Child of
    race = relationship('Race', back_populates='runs')
    heat = relationship('Heat', back_populates='runs')
    lane = relationship('Lane', back_populates='runs')
    car = relationship('Car', back_populates='runs')

    # Unique Contraints
    __table_args__ = (UniqueConstraint(heat, lane), UniqueConstraint(heat, car))



