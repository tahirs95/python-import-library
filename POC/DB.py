import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
import psycopg2.extras

Base = declarative_base()

# TODO: add foreign key refs
# TODO: add proper uuid funcs that interact with entries table
class Sensors(Base):
    __tablename__ = 'Sensors'

    sensor_id = Column(UUID, primary_key=True)
    name = Column(String(150), nullable=False)
    sensortype_id = Column(UUID, nullable=False)
    platform_id = Column(UUID, nullable=False)

class Platforms(Base):
    __tablename__ = 'Platforms'

    platform_id = Column(UUID, primary_key=True)
    name = Column(String(150))
    platformtype_id = Column(UUID, nullable=False)
    host_platform_id = Column(UUID)
    nationality_id = Column(UUID, nullable=False)

class State(Base):
    __tablename__ = 'State'

    state_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    time = Column(TIME, nullable=False)
    sensor_id = Column(UUID(as_uuid=True), nullable=False)
    # location = Column(Geometry(geometry_type='POINT', srid=4326))
    location = Column(String(150), nullable=False)
    heading = Column(DOUBLE_PRECISION)
    course = Column(DOUBLE_PRECISION)
    speed = Column(DOUBLE_PRECISION)
    datafile_id = Column(UUID(as_uuid=True), nullable=False)
    privacy_id = Column(UUID(as_uuid=True))

class Nationalities(Base):
    __tablename__ = 'Nationalities'

    nationality_id = Column(UUID(as_uuid=True), primary_key=True, server_default="val")
    name = Column(String(150), nullable=False)


class DB:
    def __init__(self):
        engine = create_engine('postgresql+psycopg2://postgres:passw0rd@localhost:5433/postgres', echo=True)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        #psycopg2.extras.register_uuid

    def addNationality(self, country):
        countryObj = Nationalities(name=country)
        self.session.add(countryObj)
        self.session.commit()

    def addToStates(self, repLine):
        stateObj = State(
            time=repLine.timestamp,
            sensor_id='c1cd04fd-8b29-4ded-b146-fed4fd65167c',
            location='('+repLine.longDegrees+','+repLine.latDegrees+')',
            heading=repLine.heading,
            # TODO: how to calculate course?
            #course=,
            speed=repLine.speed,
            datafile_id='5aa6e5bc-94b7-48e2-bd10-940a10d11dcf',
            privacy_id='477f43a1-37b0-4a49-9d95-9b20729ee6b7'
        )
        self.session.add(stateObj)
        self.session.commit()