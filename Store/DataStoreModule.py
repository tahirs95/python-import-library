import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, FetchedValue
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
from contextlib import contextmanager

Base = declarative_base()

# TODO: add foreign key refs
# TODO: add proper uuid funcs that interact with entries table

class Entry(Base):
    __tablename__ = 'Entry'

    entry_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    tabletype_id = Column(Integer, nullable=False)
    created_user = Column(Integer)

class Sensor(Base):
    __tablename__ = 'Sensors'
    tabletypeId = 2  # Only needed for tables referenced by Entry table

    sensor_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    name = Column(String(150), nullable=False)
    sensortype_id = Column(UUID, nullable=False)
    platform_id = Column(UUID, nullable=False)

class Platform(Base):
    __tablename__ = 'Platforms'
    tabletypeId = 1  # Only needed for tables referenced by Entry table

    platform_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150))
    platformtype_id = Column(UUID, nullable=False)
    host_platform_id = Column(UUID)
    nationality_id = Column(UUID, nullable=False)
    # TODO: add relationships and ForeignKey entries to auto-create Entry ids

class DatafileType(Base):
    __tablename__ = 'DatafileTypes'

    datafiletype_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150), nullable=False)

class Datafile(Base):
    __tablename__ = 'Datafiles'
    tabletypeId = 4  # Only needed for tables referenced by Entry table

    datafile_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    # TODO: does this, or other string limits need checking or validating on file import?
    simulated = Column(Boolean)
    reference = Column(String(150))
    url = Column(String(150))
    privacy_id = Column(UUID(as_uuid=True), nullable=False)
    datafiletype_id = Column(UUID(as_uuid=True), nullable=False)
    # TODO: add relationships and ForeignKey entries to auto-create Entry ids

class State(Base):
    __tablename__ = 'State'
    tabletypeId = 3  # Only needed for tables referenced by Entry table

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

class Nationality(Base):
    __tablename__ = 'Nationalities'

    nationality_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    name = Column(String(150), nullable=False)


class DataStore:

    # TODO: supply or lookup user id
    def __init__(self, DBUsername, DBPassword, DBHost, DBPort, DBName, missing_data_resolver=None):
        connectionString = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DBUsername, DBPassword, DBHost, DBPort, DBName)
        self.engine = create_engine(connectionString, echo=False)
        Base.metadata.bind = self.engine
        #DBSession = sessionmaker(bind=self.engine)
        #self.session = DBSession()
        #psycopg2.extras.register_uuid
        self.missing_data_resolver = missing_data_resolver

        # caches of known data
        self.platforms = {}
        self.sensors = {}
        self.datafiles = {}
        self.datafileTypes = {}

        # TEMP list of values for defaulted IDs, to be replaced by missing info lookup mechanism
        self.defaultPlatformTypeId = '89a63755-b40d-42ad-a156-9b69cfc7b484'  # Warship
        self.defaultSensorTypeId = '88c62daf-f808-41f0-8882-942aa41627fc'  # Sonar
        self.defaultNationalityId = 'a29033d7-3046-410a-8b80-8faf5f024f1e'  # UK
        self.defaultPrivacyId = '477f43a1-37b0-4a49-9d95-9b20729ee6b7'  # PUBLIC
        self.defaultUserId = 1  # DevUser

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        try:
            yield self
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()


    def addEntry(self, tabletypeId):
        entry_obj = Entry(
            tabletype_id=tabletypeId,
            created_user=self.defaultUserId
        )
        self.session.add(entry_obj)
        self.session.flush()

        return entry_obj.entry_id


    def addNationality(self, country):
        countryObj = Nationality(name=country)
        self.session.add(countryObj)
        self.session.flush()

    def addDatafileType(self, datafile_type):
        if datafile_type in self.datafileTypes:
            return self.datafileTypes[datafile_type]

        # doesn't exist in cache, try to lookup in DB
        datafile_type_lookup = self.session.query(DatafileType).filter(DatafileType.name == datafile_type).first()
        if datafile_type_lookup:
            return datafile_type_lookup

        datafile_type_obj = DatafileType(
            name=datafile_type
        )

        self.session.add(datafile_type_obj)
        self.session.flush()

        self.datafileTypes[datafile_type] = datafile_type_obj
        # should return DB type or something else decoupled from DB?
        return datafile_type_obj

    def addDatafile(self, datafileName, datafileType):
        if datafileName in self.datafiles:
            return self.datafiles[datafileName]

        # doesn't exist in cache, try to lookup in DB
        datafilelookup = self.session.query(Datafile).filter(Datafile.reference == datafileName).first()
        if datafilelookup:
            return datafilelookup

        datafile_type_obj = self.addDatafileType(datafileType)

        # doesn't exist in DB, create in DB
        # TODO: make a missing info resolver to provide missing info
        entry_id = self.addEntry(Datafile.tabletypeId)

        datafile_obj = Datafile(
            datafile_id=entry_id,
            simulated=False,
            reference=datafileName,
            url=None,
            privacy_id=self.defaultPrivacyId,
            datafiletype_id=datafile_type_obj.datafiletype_id
        )

        self.session.add(datafile_obj)
        self.session.flush()

        self.datafiles[datafileName] = datafile_obj
        # should return DB type or something else decoupled from DB?
        return datafile_obj

    def addPlatform(self, platformName):
        if platformName in self.platforms:
            return self.platforms[platformName]

        # doesn't exist in cache, try to lookup in DB
        platformlookup = self.session.query(Platform).filter(Platform.name == platformName).first()
        if platformlookup:
            return platformlookup

        # doesn't exist in DB, use resolver to query for data
        if self.missing_data_resolver:
            entry_id = self.missing_data_resolver.resolvePlatform(platformName)
        else:
            # enough info to proceed and create entry
            entry_id = self.addEntry(Platform.tabletypeId)

        platform_obj = Platform(
            platform_id=entry_id,
            name=platformName,
            platformtype_id=self.defaultPlatformTypeId,
            host_platform_id=None,
            nationality_id=self.defaultNationalityId
        )

        self.session.add(platform_obj)
        self.session.flush()

        self.platforms[platformName] = platform_obj
        # should return DB type or something else decoupled from DB?
        return platform_obj

    def addSensor(self, sensorName, platform):
        if sensorName in self.sensors:
            return self.sensors[sensorName]

        # doesn't exist in cache, try to lookup in DB
        sensorlookup = self.session.query(Sensor).filter(Sensor.name == sensorName).first()
        if sensorlookup:
            return sensorlookup

        # doesn't exist in DB, create in DB
        # TODO: make a missing info resolver to provide missing info
        entry_id = self.addEntry(Sensor.tabletypeId)

        sensor_obj = Sensor(
            sensor_id=entry_id,
            name=sensorName,
            sensortype_id=self.defaultSensorTypeId,
            platform_id=str(platform.platform_id)
        )

        self.session.add(sensor_obj)
        self.session.flush()

        self.sensors[sensorName] = sensor_obj
        # should return DB type or something else decoupled from DB?
        return sensor_obj

    def addState(self, timestamp, datafile, sensor, lat, long, heading, speed):
        entry_id = self.addEntry(Sensor.tabletypeId)

        state_obj = State(
            time=timestamp,
            sensor_id=sensor.sensor_id,
            location='('+str(long.degrees)+','+str(lat.degrees)+')',
            heading=heading,
            # TODO: how to calculate course?
            #course=,
            speed=speed,
            datafile_id=datafile.datafile_id,
            privacy_id=self.defaultPrivacyId
        )
        self.session.add(state_obj)
        self.session.flush()

        return state_obj
