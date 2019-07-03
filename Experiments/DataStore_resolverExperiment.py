import sys
import pathlib
# TODO: do this properly!
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from Formats.REPFile import REPFile
from Store.DataStoreModule import DataStore
from Resolvers.CommandLineResolver import CommandLineResolver

datastore = DataStore("postgres", "passw0rd", "localhost", 5433, "postgres", missing_data_resolver=CommandLineResolver())

filePath = pathlib.Path(__file__).parent.parent / "Resources/missing_platform.rep"
rep = REPFile(str(filePath.absolute()))

with datastore.session_scope() as session:
    datafile = session.addDatafile(rep.getDatafileName(), rep.getDatafileType())
    for repLine in rep.getLines():
        platform = session.addPlatform(repLine.getPlatform())
        sensor = session.addSensor("GPS", platform)
        session.addState(repLine.getTimestamp(), datafile, sensor, repLine.getLatitude(), repLine.getLongitude(), repLine.getHeading(), repLine.getSpeed())
