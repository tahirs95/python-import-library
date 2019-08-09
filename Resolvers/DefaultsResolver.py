import sys
from Resolvers.DataResolver import DataResolver


class DefaultsResolver(DataResolver):

    # Hardcoded default values
    defaultPlatformType = "Warship"
    defaultNationality = "UK"
    defaultSensorType = "Position"
    defaultPrivacy = "Private"

    def resolvePlatform(self, datastore, platformName):
        # needs to establish defaults for platformType, nationality

        platformType = datastore.searchPlatformType(self.defaultPlatformType)
        if not platformType:
            platformType = datastore.addPlatformType(self.defaultPlatformType)

        nationality = datastore.searchNationality(self.defaultNationality)
        if not nationality:
            nationality = datastore.addNationality(self.defaultNationality)

        return platformName, platformType, nationality

    def resolveSensor(self, datastore, sensorName):
        # needs to establish defaults for sensorType

        sensorType = datastore.searchSensorType(self.defaultSensorType)
        if not sensorType:
            sensorType = datastore.addSensorType(self.defaultSensorType)

        return sensorName, sensorType

    def resolvePrivacy(self, datastore, tabletypeId, tablename):
        # needs to establish defaults for privacy

        privacy = datastore.searchPrivacy(self.defaultPrivacy)
        if not privacy:
            privacy = datastore.addPrivacy(self.defaultPrivacy)

        return tabletypeId, privacy

