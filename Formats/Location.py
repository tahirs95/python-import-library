
class Location:

    def __init__(self, degrees, minutes, seconds, hemisphere):
        self.degrees = degrees
        self.minutes = minutes
        self.seconds = seconds
        self.hemisphere = hemisphere

    def __repr__(self):
        return "(" + str(self.degrees) + ", " + str(self.minutes) + ", " + str(self.seconds) + ", " + self.hemisphere + ")"

    def parse(self):
        try:
            self.degrees = float(self.degrees)
        except ValueError:
            print("Error in degrees value {}. Couldn't convert to a number".format(self.degrees))
            return False

        try:
            self.minutes = float(self.minutes)
        except ValueError:
            print("Error in minutes value {}. Couldn't convert to a number".format(self.minutes))
            return False

        try:
            self.seconds = float(self.seconds)
        except ValueError:
            print("Error in seconds value {}. Couldn't convert to a number".format(self.seconds))
            return False

        if self.hemisphere not in ("N", "S", "E", "W"):
            print("Error in hemisphere value {}. Should be one of N, S, E or W".format(self.hemisphere))
            return False

        return True