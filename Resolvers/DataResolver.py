from abc import ABC, abstractmethod

class DataResolver(ABC):

    @abstractmethod
    def resolvePlatform(self, datastore, platformName):
        pass

    @abstractmethod
    def resolveSensor(self, datastore, sensorName):
        pass
