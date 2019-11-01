from enum import Enum


class TableTypes(Enum):
    METADATA = 1
    MEASUREMENT = 2
    REFERENCE = 3


class DBStatus:

    def __init__(self, datastore, tabletypes):
        self.datastore = datastore
        self.tabletypes = tabletypes
        self.currentStatus = None

    # get current table stats, store and return status
    def getStatus(self):
        self.currentStatus = self.datastore.getTabletypeData(self.tabletypes)
        return self.currentStatus

    # print current stats, plus diff to supplied stats if passed
    def printStatus(self, prev_status=None):
        maxLen = len(max(self.currentStatus, key=len))+1
        print("{:<{}} {:<4} {:<4}".format("Table", maxLen, "Num", "Diff"))
        for table in self.currentStatus:
            print(f"{table:<{maxLen}} {self.currentStatus[table]:<4} {self.calcDiff(table, prev_status):<4}")

    def calcDiff(self, table, prev_status):
        if not prev_status or table not in prev_status or table not in self.currentStatus:
            return "-"
        return self.currentStatus[table] - prev_status[table]