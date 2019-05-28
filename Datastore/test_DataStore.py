import sys
# TODO: do this properly!
sys.path.insert(0, 'c:/mikee/python/up/python-import-library/Formats')
from REPFile import *
from DataStore import *

datastore = DataStore("postgres", "passw0rd", "localhost", 5433, "postgres")

singleLine = REPLine(1, "100112 121000 SUBJECT2 VC 60 23 36.32 N 000 01 48.82 E 109.08  6.00  0.00 ")
singleLine.parse()
#singleLine.print()

rep = REPFile("../POC/Ambig_tracks2_short.rep")

datafile = datastore.addDatafile(rep.getDatafileName(), rep.getDatafileType())
platform = datastore.addPlatform(singleLine.getPlatform())
sensor = datastore.addSensor("GPS", platform)
datastore.addState(singleLine.timestamp, datafile, sensor, singleLine.latitude, singleLine.longitude, singleLine.heading, singleLine.speed)
