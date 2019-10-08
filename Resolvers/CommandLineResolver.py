import sys
from Resolvers.DataResolver import DataResolver
from Resolvers import CommandLineInput


class CommandLineResolver(DataResolver):

    def __init__(self):
        self.table_privacies = {}

    def synonymSearch(self, datastore, platformName):
        platformSearchInput = input("Please type word stem to search for: ")
        searchResult = datastore.searchPlatform(platformSearchInput)
        if not searchResult:
            # couldn't find it
            notFoundChoice = CommandLineInput.getChoiceInput(f"Platform with '{platformSearchInput}' not found. Do you wish to: ",
                                                             ["Search for another synonym of this name",
                                                              f"Add a new platform, titled '{platformName}'",
                                                              "Cancel import"])

            if notFoundChoice == 1:
                self.synonymSearch(datastore, platformName)
            elif notFoundChoice == 2:
                return 2
            elif notFoundChoice == 3:
                print("Quitting")
                sys.exit(1)
        else:
            # found something
            foundChoice = CommandLineInput.getChoiceInput(f"Platform '{searchResult}' found. Would you like to add this as a synonym: ",
                                                          ["Yes",
                                                           "No, find other synonym",
                                                           "Cancel import"])
            if foundChoice == 1:
                return searchResult
            elif foundChoice == 2:
                self.synonymSearch(datastore, platformName)
            elif foundChoice == 3:
                print("Quitting")
                sys.exit(1)

    def addPlatform(self, datastore, platformName):
        ###### Chose Nationality ######
        print("Ok, adding new platform.")
        nationalityOptions = datastore.getNationalities()
        nationalityNames = [n.name for n in nationalityOptions]
        nationalityNames.append("Add a new nationality")
        nationalityNames.append("Cancel import")
        nationalityChoice = CommandLineInput.getChoiceInput("Please provide nationality: ",
                                                            nationalityNames)
        if nationalityChoice == len(nationalityNames):
            print("Quitting")
            sys.exit(1)
        elif nationalityChoice == len(nationalityNames)-1:
            nationalityCheckOk = False
            while not nationalityCheckOk:
                newNationalityInput = input("Please type name of new nationality: ")
                nationalityCheckOk = datastore.checkNationality(newNationalityInput)
            chosenNationality = datastore.addNationality(newNationalityInput)
        else:
            chosenNationality = nationalityOptions[nationalityChoice-2]

        ###### Chose Class (aka PlatformType) ######
        # "class" is referring to platform type in DB
        classOptions = datastore.getPlatformTypes()
        classNames = [c.name for c in classOptions]
        classNames.append("Add a new class")
        classNames.append("Cancel import")
        classChoice = CommandLineInput.getChoiceInput("Ok, please provide class: ",
                                                      classNames)
        if classChoice == len(classNames):
            print("Quitting")
            sys.exit(1)
        elif classChoice == len(classNames)-1:
            classCheckOk = False
            while not classCheckOk:
                newClassInput = input("Please type name of new class: ")
                classCheckOk = datastore.checkPlatformType(newClassInput)
            chosenClass = datastore.addPlatformType(newClassInput)
        else:
            chosenClass = classOptions[classChoice-2]

        ###### Chose Sensor ######
        newSensor = False
        sensorOptions = datastore.getSensorsByPlatformType(chosenClass)
        if len(sensorOptions) > 0:
            sensorNames = [s.Sensor.name for s in sensorOptions]
            sensorNames.append("Cancel import")
            sensorChoice = CommandLineInput.getChoiceInput(f"We have {len(sensorNames)-1} other instances of {chosenClass.name} class. They contain these sensors. Please indicate which you wish to add to {platformName}: ",
                                                           sensorNames)
            if sensorChoice == len(sensorNames):
                print("Quitting")
                sys.exit(1)

            chosenSensor = sensorOptions[sensorChoice-1]
        else:
            print("No sensors found for that class. Skipping Sensor add")
            chosenSensor = None
            # sensorChoices = ["Add a new sensor", "Cancel import"]
            # sensorChoice = CommandLineInput.getChoiceInput(f"No instances of class {chosenClass.name} exist. Please choose an option: ",
            #                                                sensorChoices)
            # if sensorChoice == len(sensorChoices):
            #     print("Quitting")
            #     sys.exit(1)
            # elif sensorChoice == len(sensorChoices)-1:
            #     sensorCheckOk = False
            #     while not sensorCheckOk:
            #         newSensorInput = input("Please type name of new sensor: ")
            #         sensorCheckOk = datastore.checkSensor(newSensorInput)
            #     #chosenSensor = datastore.addSensor(newClassInput)
            #     chosenSensor = newSensorInput
            #     newSensor = True

        ###### Chose Classification (aka Privacy) ######
        classificationOptions = datastore.getPrivacies()
        classificationNames = [c.name for c in classificationOptions]
        classificationNames.append("Add a new classification")
        classificationNames.append("Cancel import")
        classificationChoice = CommandLineInput.getChoiceInput("Ok, please provide classification for this platform: ",
                                                               classificationNames)

        if classificationChoice == len(classificationNames):
            print("Quitting")
            sys.exit(1)
        elif classificationChoice == len(classificationNames)-1:
            classificationCheckOk = False
            while not classificationCheckOk:
                newClassificationInput = input("Please type name of new classification: ")
                classificationCheckOk = datastore.checkPrivacy(newClassificationInput)
            chosenClassification = datastore.addPrivacy(newClassificationInput)
        else:
            chosenClassification = classificationOptions[classificationChoice-2]

        print("Input complete. About to create this platform:")
        print(f"Name: {platformName}")
        print(f"Nationality: {chosenNationality.name}")
        print(f"Class: {chosenClass.name}")
        if chosenSensor:
            print(f"Sensors: {chosenSensor.Sensor.name}")
        else:
            print("Sensors: None")
        print(f"Classification: {chosenClassification.name}")

        createChoice = CommandLineInput.getChoiceInput("Create this platform?: ",
                                                       ["Yes",
                                                        "No, make further edits",
                                                        "Cancel import"])

        if createChoice == 1:
            # TODO: pass back sensor and classification when Schema changed
            return platformName, chosenClass, chosenNationality
        elif createChoice == 2:
            return self.addPlatform(datastore, platformName)
        elif createChoice == 3:
            print("Quitting")
            sys.exit(1)

    def resolvePlatform(self, datastore, platformName):
        actionChoice = CommandLineInput.getChoiceInput(f"Platform '{platformName}' not found. Do you wish to: ",
                                                       [#"Search for synonym of this name",
                                                        f"Add a new platform, titled '{platformName}'",
                                                        "Cancel import"])

        if actionChoice == 1:
            #synSearch = self.synonymSearch(datastore, platformName)
            #print(f"Adding {synSearch} as a synonym for {platformName}")
            return self.addPlatform(datastore, platformName)
        else:
            print("Quitting")
            sys.exit(1)

    def addSensor(self, datastore, sensorName):
        ###### Chose Sensor Type ######
        print("Ok, adding new sensor.")
        sensorTypeOptions = datastore.getSensorTypes()
        sensorTypeNames = [st.name for st in sensorTypeOptions]
        sensorTypeNames.append("Add a new sensor type")
        sensorTypeNames.append("Cancel import")
        sensorTypeChoice = CommandLineInput.getChoiceInput("Please provide sensor type: ",
                                                           sensorTypeNames)
        if sensorTypeChoice == len(sensorTypeNames):
            print("Quitting")
            sys.exit(1)
        elif sensorTypeChoice == len(sensorTypeNames)-1:
            sensorTypeCheckOk = False
            while not sensorTypeCheckOk:
                sensorTypeInput = input("Please type name of new sensor type: ")
                sensorTypeCheckOk = datastore.checkSensorType(sensorTypeInput)
            chosenSensorType = datastore.addSensorType(sensorTypeInput)
        else:
            chosenSensorType = sensorTypeOptions[sensorTypeChoice-2]

        return sensorName, chosenSensorType

    def resolveSensor(self, datastore, sensorName):
        actionChoice = CommandLineInput.getChoiceInput(f"Sensor '{sensorName}' not found. Do you wish to: ",
                                                       [f"Add a new sensor, titled '{sensorName}'",
                                                        "Cancel import"])

        if actionChoice == 1:
            return self.addSensor(datastore, sensorName)
        elif actionChoice == 2:
            print("Quitting")
            sys.exit(1)

    def resolvePrivacy(self, datastore, tabletypeId, tablename):
        if tabletypeId in self.table_privacies:
            return tabletypeId, self.table_privacies[tabletypeId]

        ###### Chose Classification (aka Privacy) ######
        classificationOptions = datastore.getPrivacies()
        classificationNames = [c.name for c in classificationOptions]
        classificationNames.append("Add a new classification")
        classificationNames.append("Cancel import")
        classificationChoice = CommandLineInput.getChoiceInput(f"Ok, please provide classification for table '{tablename}': ",
                                                               classificationNames)

        if classificationChoice == len(classificationNames):
            print("Quitting")
            sys.exit(1)
        elif classificationChoice == len(classificationNames)-1:
            classificationCheckOk = False
            while not classificationCheckOk:
                newClassificationInput = input("Please type name of new classification: ")
                classificationCheckOk = datastore.checkPrivacy(newClassificationInput)
            chosenClassification = datastore.addPrivacy(newClassificationInput)
        else:
            chosenClassification = classificationOptions[classificationChoice-2]

        self.table_privacies[tabletypeId] = chosenClassification

        return tabletypeId, chosenClassification
