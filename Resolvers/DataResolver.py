from abc import ABC, abstractmethod

class DataResolver(ABC):

    @abstractmethod
    def resolvePlatform(self, datastore, platformName):
        # Implementation method should return any data necessary to create a platform
        # Currently: platformName, platformType, nationality. Probably hostPlatform when that is needed
        pass

    @abstractmethod
    def resolveSensor(self, datastore, sensorName):
        # Implementation method should return any data necessary to create a sensor
        # Currently: sensorName, sensorType
        pass

    @abstractmethod
    def resolvePrivacy(self, datastore, tabletypeId, tablename):
        # Implementation method should return any data necessary to create a privacy
        # Currently: tabletypeId, privacyName
        pass
