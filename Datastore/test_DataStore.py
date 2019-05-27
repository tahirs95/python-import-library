import sys
sys.path.insert(0, 'c:/mikee/python/up/python-import-library/Formats')
from REPFile import *
from DataStore import *

session = DataStore()

singleLine = REPLine(1, "100112 121000 SUBJECT2 VC 60 23 36.32 N 000 01 48.82 E 109.08  6.00  0.00 ")
singleLine.parse()
#singleLine.print()

session.addPlatform(singleLine.getPlatform())