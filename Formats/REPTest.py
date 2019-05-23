from REP import *
from Location import *

# l = REPLine(1, "100112 121000 SUBJECT VC 60 23 36.32 N 000 01 48.82 E 109.08  6.00  0.00 ")
# l.parse()
# l.print()
#
# loc = Location("10.9", "115.7", "12.0", "N")
# if not loc.parse():
#     print("error")
#     exit()
#
# print(loc)

repFile = REP("../POC/Ambig_tracks2_short.rep")
for repLine in repFile.getLines():
    repLine.print()
