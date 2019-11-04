import sys
import pathlib

from Formats.REPFile import REPFile
from Store.DataStoreModule import DataStore
from Store.DBStatus import DBStatus, TableTypes
from Resolvers.CommandLineResolver import CommandLineResolver

#datastore = DataStore("postgres", "passw0rd", "localhost", 5433, "postgres", missing_data_resolver=CommandLineResolver())
datastore = DataStore("", "", "", 0, "c:/temp/datastore.db", db_type='sqlite', missing_data_resolver=CommandLineResolver())

filePath = pathlib.Path(__file__).parent.parent / "Resources/missing_platform.rep"
rep = REPFile(str(filePath.absolute()))

status = DBStatus(datastore, [TableTypes.METADATA, TableTypes.REFERENCE])

with datastore.session_scope() as session:
    stats = status.getStatus()
    status.printStatus()
    datafile = session.addToDatafiles(rep.getDatafileName(), rep.getDatafileType())
    for repLine in rep.getLines():
        platform = session.addToPlatforms(repLine.getPlatform())
        sensor = session.addToSensors("GPS", platform)
        session.addToStates(repLine.getTimestamp(), datafile, sensor, repLine.getLatitude(), repLine.getLongitude(), repLine.getHeading(), repLine.getSpeed())
    status.getStatus()
    status.printStatus(prev_status=stats)