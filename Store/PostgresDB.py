from sqlalchemy import Column, Integer, String, Boolean, FetchedValue
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from Store.DBBase import Base
from Store.DBStatus import TableTypes

def mapUUIDType(val):
    # postgres needs to map to string
    return str(val)

class Entry(Base):
    __tablename__ = 'Entry'
    tabletype = TableTypes.METADATA

    entry_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
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

    sensortype_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150))

class Sensor(Base):
    __tablename__ = 'Sensors'
    tabletype = TableTypes.METADATA
    tabletypeId = 2  # Only needed for tables referenced by Entry table

    sensor_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    name = Column(String(150), nullable=False)
    sensortype_id = Column(UUID, nullable=False)
    platform_id = Column(UUID, nullable=False)

class PlatformType(Base):
    __tablename__ = 'PlatformTypes'
    tabletype = TableTypes.REFERENCE

    platformtype_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150))
    # TODO: add relationships and ForeignKey entries to auto-create Entry ids

class Platform(Base):
    __tablename__ = 'Platforms'
    tabletype = TableTypes.METADATA
    tabletypeId = 1  # Only needed for tables referenced by Entry table

    platform_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150))
    platformtype_id = Column(UUID(as_uuid=True), nullable=False)
    host_platform_id = Column(UUID(as_uuid=True))
    nationality_id = Column(UUID(as_uuid=True), nullable=False)
    # TODO: add relationships and ForeignKey entries to auto-create Entry ids

class DatafileType(Base):
    __tablename__ = 'DatafileTypes'
    tabletype = TableTypes.REFERENCE

    datafiletype_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    # TODO: does this, or other string limits need checking or validating on file import?
    name = Column(String(150), nullable=False)

class Datafile(Base):
    __tablename__ = 'Datafiles'
    tabletype = TableTypes.METADATA
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
    tabletype = TableTypes.MEASUREMENT
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
    tabletype = TableTypes.REFERENCE

    nationality_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    name = Column(String(150), nullable=False)

class Privacy(Base):
    __tablename__ = 'Privacies'
    tabletype = TableTypes.REFERENCE

    privacy_id = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())
    name = Column(String(150), nullable=False)

