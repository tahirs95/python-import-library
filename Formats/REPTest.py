print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from Formats.REPFile import REPFile
from Formats.Location import Location
import pathlib

# l = State(1, "100112 121000 SUBJECT VC 60 23 36.32 N 000 01 48.82 E 109.08  6.00  0.00 ")
# l.parse()
# l.print()
#
# loc = Location("10.9", "115.7", "12.0", "N")
# if not loc.parse():
#     print("error")
#     exit()
#
# print(loc)

filePath = pathlib.Path(__file__).parent.parent / "Resources/Ambig_tracks2_short.rep"
repFile = REPFile(str(filePath))
for repLine in repFile.getLines():
    repLine.print()
