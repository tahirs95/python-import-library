from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.dialects.sqlite import REAL
import uuid

from Store.DBBase import BaseSQLite as Base
from Store.DBStatus import TableTypes
from Store.UUID import UUID

def mapUUIDType(val):
    # sql does not need to map to string
    return val

class Entry(Base):
    __tablename__ = 'Entry'
    tabletype = TableTypes.METADATA

    entry_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    tabletype_id = Column(Integer, nullable=False)
    created_user = Column(Integer)

class TableType(Base):
    __tablename__ = 'TableTypes'
    tabletype = TableTypes.METADATA

    tabletype_id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(150))

class SensorType(Base):
    __tablename__ = 'SensorTypes'
    tabletype = TableTypes.REFERENCE

    sensortype_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150))

class Sensor(Base):
    __tablename__ = 'Sensors'
    tabletype = TableTypes.METADATA

    # These only needed for tables referenced by Entry table
    tabletypeId = 2
    tableName = 'Sensor'

    sensor_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    sensortype_id = Column(UUID, nullable=False)
    platform_id = Column(UUID, nullable=False)

class PlatformType(Base):
    __tablename__ = 'PlatformTypes'
    tabletype = TableTypes.REFERENCE

    platformtype_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150))
    # TODO: add relationships and ForeignKey entries to auto-create Entry ids

class Platform(Base):
    __tablename__ = 'Platforms'
    tabletype = TableTypes.METADATA

    # These only needed for tables referenced by Entry table
    tabletypeId = 1
    tableName = 'Platforms'

    platform_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150))
    platformtype_id = Column(UUID(), nullable=False)
    host_platform_id = Column(UUID())
    nationality_id = Column(UUID(), nullable=False)
    # TODO: add relationships and ForeignKey entries to auto-create Entry ids

class DatafileType(Base):
    __tablename__ = 'DatafileTypes'
    tabletype = TableTypes.REFERENCE

    datafiletype_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150), nullable=False)

class Datafile(Base):
    __tablename__ = 'Datafiles'
    tabletype = TableTypes.METADATA

    # These only needed for tables referenced by Entry table
    tabletypeId = 4
    tableName = 'Datafiles'

    datafile_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    # TODO: does this, or other string limits need checking or validating on file import?
    simulated = Column(Boolean)
    reference = Column(String(150))
    url = Column(String(150))
    privacy_id = Column(UUID(), nullable=False)
    datafiletype_id = Column(UUID(), nullable=False)
    # TODO: add relationships and ForeignKey entries to auto-create Entry ids

class State(Base):
    __tablename__ = 'State'
    tabletype = TableTypes.MEASUREMENT

    # These only needed for tables referenced by Entry table
    tabletypeId = 3
    tableName = 'State'

    state_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    time = Column(DATETIME, nullable=False)
    sensor_id = Column(UUID(), nullable=False)
    # location = Column(Geometry(geometry_type='POINT', srid=4326))
    location = Column(String(150), nullable=False)
    heading = Column(REAL)
    course = Column(REAL)
    speed = Column(REAL)
    datafile_id = Column(UUID(), nullable=False)
    privacy_id = Column(UUID())

class Nationality(Base):
    __tablename__ = 'Nationalities'
    tabletype = TableTypes.REFERENCE

    nationality_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)

class Privacy(Base):
    __tablename__ = 'Privacies'
    tabletype = TableTypes.REFERENCE

    privacy_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)

