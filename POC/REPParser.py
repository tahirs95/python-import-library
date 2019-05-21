from datetime import datetime

class REPLine:

    def __init__(self, linenumber, line):
        self.lineNum = linenumber
        self.line = line

        self.date = ""
        self.time = ""
        self.vesselName = ""
        self.symbology = ""
        self.latDegrees = ""
        self.latMins = ""
        self.latSecs = ""
        self.latHemi = ""
        self.longDegrees = ""
        self.longMins = ""
        self.longSecs = ""
        self.longHemi = ""
        self.heading = ""
        self.speed = ""
        self.depth = ""
        self.textLabel = ""
        self.textLabel = ""

        print("Read line {}. Tokens: date    time    vessel   symbology   latDegrees   latMins   latSecs   latHemi   longDegrees   longMins   longSecs   longHemi   heading   speed   depth   textLabel".format(self.lineNum))
        print("                     " + line)

    def parse(self):

        tokens = self.line.split()
        self.date = tokens[0]
        self.time = tokens[1]
        self.vesselName = tokens[2]
        self.symbology = tokens[3]
        self.latDegrees = tokens[4]
        self.latMins = tokens[5]
        self.latSecs = tokens[6]
        self.latHemi = tokens[7]
        self.longDegrees = tokens[8]
        self.longMins = tokens[9]
        self.longSecs = tokens[10]
        self.longHemi = tokens[11]
        self.heading = tokens[12]
        self.speed = tokens[13]
        self.depth = tokens[14]
        self.textLabel = ""
        if len(tokens) >= 16:
            self.textLabel = tokens[15]

        self.timestamp = None

        if len(tokens) < 15:
            print("Error on line {} not enough tokens: {}".format(self.lineNum, self.line))



        if len(self.date) != 6 and len(self.date) != 8:
            print("Line {}. Error in Date format {}. Should be either 2 of 4 figure date, followed by month then date".format(self.lineNum, self.date))
            return False
        # TODO: check chars and attempt to convert

        # Times always in Zulu/GMT
        if len(self.time) != 6 and  len(self.time) != 10:
            print("Line {}. Error in Time format {}. Should be HHMMSS[.SSS]".format(self.lineNum, self.time))
            return False

        self.timestamp = self.parseTimestamp(self.date, self.time)

        # TODO: strip quotes off vessel name if neccesary

        symVals = self.symbology.split("[")
        if len(symVals) >= 1:
            if len(symVals[0]) != 2 and len(symVals[0]) != 5:
                print("Line {}. Error in Symbology format {}. Should be 2 or 5 chars".format(self.lineNum, self.symbology))
                return False
        if len(symVals) != 1 and len(symVals) != 2:
            print("Line {}. Error in Symbology format {}".format(self.lineNum, self.symbology))
            return False

        try:
            deg = float(self.latDegrees)
        except ValueError:
            print("Line {}. Error in latitude degrees value {}. Couldn't convert to a number".format(self.lineNum, self.latDegrees))
            return False

        try:
            mins = float(self.latMins)
        except ValueError:
            print("Line {}. Error in latitude minutes value {}. Couldn't convert to a number".format(self.lineNum, self.latMins))
            return False

        try:
            secs = float(self.latSecs)
        except ValueError:
            print("Line {}. Error in latitude seconds value {}. Couldn't convert to a number".format(self.lineNum, self.latSecs))
            return False

        if self.latHemi != "N" and self.latHemi != "S":
            print("Line {}. Error in latitude hemisphere format {}. Should be N or S".format(self.lineNum, self.latHemi))
            return False

        # TODO: refactor checking logic to reuse
        try:
            deg = float(self.longDegrees)
        except ValueError:
            print("Line {}. Error in longitude degrees value {}. Couldn't convert to a number".format(self.lineNum, self.longDegrees))
            return False

        try:
            mins = float(self.longMins)
        except ValueError:
            print("Line {}. Error in longitude minutes value {}. Couldn't convert to a number".format(self.lineNum, self.longMins))
            return False

        try:
            secs = float(self.longSecs)
        except ValueError:
            print("Line {}. Error in longitude seconds value {}. Couldn't convert to a number".format(self.lineNum, self.longSecs))
            return False

        if self.longHemi != "E" and self.longHemi != "W":
            print("Line {}. Error in longitude hemisphere format {}. Should be E or W".format(self.lineNum, self.longHemi))
            return False

        try:
            head = float(self.heading)
        except ValueError:
            print("Line {}. Error in heading value {}. Couldn't convert to a number".format(self.lineNum, self.heading))
            return False
        if 0.0 > head >= 360.0:
            print("Line {}. Error in heading value {}. Should be be between 0 and 359.9 degrees".format(self.lineNum, self.heading))
            return False

        try:
            speed = float(self.speed)
        except ValueError:
            print("Line {}. Error in speed value {}. Couldn't convert to a number".format(self.lineNum, self.speed))
            return False

        try:
            depth = float(self.depth)
        except ValueError:
            print("Line {}. Error in depth value {}. Couldn't convert to a number".format(self.lineNum, self.depth))
            return False

        return True

    def parseTimestamp(self, date, time):
        if len(date) == 6:
            formatStr = '%y%m%d'
        else:
            formatStr = '%Y%m%d'

        if len(self.time) == 6:
            formatStr += '%H%M%S'
        else:
            formatStr += '%H%M%S.%f'

        return datetime.strptime(date + time, formatStr)

def load(filename):
    with open(filename, "r") as file:
        lineNum = 0
        lines = []
        for line in file:
            lineNum += 1

            if len(line) == 0 or line[0] == ';':
                continue

            repL = REPLine(lineNum, line)
            if not repL.parse():
                raise Exception("failed parsing line {}".format(lineNum))

            lines.append(repL)

    return lines