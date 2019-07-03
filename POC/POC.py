import REPParser
from DB import *
import pathlib

session = DB()

filePath = pathlib.Path(__file__).parent.parent / "Resources/Ambig_tracks2_short.rep"
repFile = REPParser.load(str(filePath))
for repLine in repFile:
    print("line: " + str(repLine))
    session.addState(repLine)
