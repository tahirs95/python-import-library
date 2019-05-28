import sys
# TODO: do this properly!
sys.path.insert(0, 'c:/mikee/python/up/python-import-library/Formats')
from REPFile import *
from DataStore import *

datastore = DataStore("postgres", "passw0rd", "localhost", 5433, "postgres")
rep = REPFile("../POC/Ambig_tracks2.rep")

with datastore.session_scope() as session:
    datafile = session.addDatafile(rep.getDatafileName(), rep.getDatafileType())
    for repLine in rep.getLines():
        platform = session.addPlatform(repLine.getPlatform())
        sensor = session.addSensor("GPS", platform)
        session.addState(repLine.timestamp, datafile, sensor, repLine.latitude, repLine.longitude, repLine.heading, repLine.speed)
