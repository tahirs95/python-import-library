from abc import ABC, abstractmethod

class DataResolver(ABC):

    @abstractmethod
    def resolvePlatform(self, platformName):
        pass

    @abstractmethod
    def resolveSensor(self, sensorName):
        pass
