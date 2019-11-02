from datetime import datetime
from .Location import Location
from .State import State

# TODO: have base class to ensure filename and type are setup and returned
class REPFile:

    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = []

        with open(filepath, "r") as file:
            lineNum = 0
            for line in file:
                lineNum += 1

                if len(line) == 0 or line[0] == ';':
                    continue

                repL = State(lineNum, line)
                if not repL.parse():
                    raise Exception("failed parsing REP file {} line {}".format(filepath, lineNum))

                self.lines.append(repL)

    def getLines(self):
        return self.lines

    # TODO: could organise these values differently, eg. use registry of importers which also defines file type
    # although this works well for encapsulation
    def getDatafileType(self):
        return "REP"

    def getDatafileName(self):
        # TODO: should this be just the filename? or the full absolute or relative path supplied?
        return self.filepath
