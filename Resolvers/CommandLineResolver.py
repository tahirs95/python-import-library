from Resolvers.DataResolver import DataResolver
from Resolvers import CommandLineInput

class CommandLineResolver(DataResolver):
    
    def resolvePlatform(self, platformName):
        actionChoice = CommandLineInput.getChoiceInput(f"Platform {platformName} not found: ",
                                                        ["Create new platform",
                                                         f"Search for existing platform, and provide {platformName} as a synonym",
                                                         "Drop out"])

        if actionChoice == 1:
            addAccount.doAction(env, token)
        elif actionChoice == 2:
            configAccount.doAction(env, token)
        elif actionChoice == 3:
            validateAccount.doAction(env, token)

    def resolveSensor(self, sensorName):
        pass