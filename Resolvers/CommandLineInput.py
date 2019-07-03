
def getChoiceInput(heading, choices):
    mapChoice = False
    while 1:
        inputText = heading + "\n"
        for idx, choiceElement in enumerate(choices, 1):
            if isinstance(choiceElement, list):
                choiceString = choiceElement[0]
                mapChoice = True
            else:
                choiceString = choiceElement
            inputText += "   " + str(idx) + ") " + choiceString + "\n"
        choice = input(inputText)

        try:
            choiceVal = int(choice)
        except ValueError:
            print(choice + " wasn't a valid number, please try again")
            continue

        if choiceVal < 1 or choiceVal > len(choices):
            print(choice + " was not one of the options, please try again")
        else:
            if not mapChoice:
                return choiceVal
            else:
                return choices[choiceVal-1][1]
