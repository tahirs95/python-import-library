import REPParser
from DB import *

session = DB()


repFile = REPParser.load("Ambig_tracks2_short.rep")
for repLine in repFile:
    print("line: " + str(repLine))
    session.addState(repLine)
