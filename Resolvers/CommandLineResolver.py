import sys
from Resolvers.DataResolver import DataResolver
from Resolvers import CommandLineInput


class CommandLineResolver(DataResolver):

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
        print("Ok, adding new platform.")
        nationalityOptions = datastore.getNationalities()
        nationalityNames = [n.name for n in nationalityOptions]
        nationalityNames.append("Cancel import")
        nationalityChoice = CommandLineInput.getChoiceInput("Please provide nationality: ",
                                                            nationalityNames)
        if nationalityChoice == len(nationalityNames):
            print("Quitting")
            sys.exit(1)

        chosenNationality = nationalityOptions[nationalityChoice-1]

        # TODO: confirm that "class" is referring to platform type. Assume for now that it does
        classOptions = datastore.getPlatformTypes()
        classNames = [c.name for c in classOptions]
        classNames.append("Cancel import")
        classChoice = CommandLineInput.getChoiceInput("Ok, please provide class: ",
                                                      classNames)
        if classChoice == len(classNames):
            print("Quitting")
            sys.exit(1)

        chosenClass = classOptions[classChoice-1]

        classificationOptions = datastore.getClassifications()
        classificationNames = [c.name for c in classificationOptions]
        classificationNames.append("Cancel import")
        classificationChoice = CommandLineInput.getChoiceInput("Ok, please provide classification for this platform: ",
                                                               classificationNames)

        if classificationChoice == len(classificationNames):
            print("Quitting")
            sys.exit(1)

        chosenClassification = classificationOptions[classificationChoice-1]

        print("Input complete. About to create this platform:")
        print(f"Name: {platformName}")
        print(f"Nationality: {chosenNationality.name}")
        print(f"Class: {chosenClass.name}")
        print(f"Sensors: TBD")
        print(f"Classification: {chosenClassification.name}")

        createChoice = CommandLineInput.getChoiceInput("Create this platform?: ",
                                                       ["Yes",
                                                        "No, make further edits",
                                                        "Cancel import"])

        if createChoice == 1:
            return datastore.createPlatform(platformName, chosenNationality, chosenClass, chosenClassification)
        elif createChoice == 2:
            return self.addPlatform(datastore, platformName)
        elif createChoice == 3:
            print("Quitting")
            sys.exit(1)

    def resolvePlatform(self, datastore, platformName):
        actionChoice = CommandLineInput.getChoiceInput(f"Platform '{platformName}' not found. Do you wish to: ",
                                                       ["Search for synonym of this name",
                                                        f"Add a new platform, titled '{platformName}'",
                                                        "Cancel import"])

        if actionChoice == 1:
            synSearch = self.synonymSearch(datastore, platformName)
            print(f"Adding {synSearch} as a synonym for {platformName}")
        elif actionChoice == 2:
            addedPlatform = self.addPlatform(datastore, platformName)
        elif actionChoice == 3:
            print("Quitting")
            sys.exit(1)


    def resolveSensor(self, datastore, sensorName):
        pass